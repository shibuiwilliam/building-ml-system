import json
from abc import ABC, abstractmethod
from typing import List

import cloudpickle
from src.configurations import Configurations
from src.entities.animal import AnimalQuery
from src.entities.animal_feature import AnimalFeatureCreate, AnimalFeatureQuery, AnimalFeatureUpdate
from src.infrastructure.cache import AbstractCache
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.middleware.logger import configure_logger
from src.repository.animal_feature_repository import AbstractAnimalFeatureRepository
from src.repository.animal_repository import AbstractAnimalRepository
from src.service.feature_processing import (
    CategoricalVectorizer,
    DescriptionTokenizer,
    DescriptionVectorizer,
    NameTokenizer,
    NameVectorizer,
)

logger = configure_logger(__name__)


class AbstractAnimalFeatureUsecase(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        animal_feature_repository: AbstractAnimalFeatureRepository,
        messaging: RabbitmqMessaging,
        cache: AbstractCache,
        animal_category_vectorizer: CategoricalVectorizer,
        animal_subcategory_vectorizer: CategoricalVectorizer,
        description_tokenizer: DescriptionTokenizer,
        name_tokenizer: NameTokenizer,
        description_vectorizer: DescriptionVectorizer,
        name_vectorizer: NameVectorizer,
    ):
        self.animal_repository = animal_repository
        self.animal_feature_repository = animal_feature_repository
        self.messaging = messaging
        self.cache = cache

        self.animal_category_vectorizer = animal_category_vectorizer
        self.animal_subcategory_vectorizer = animal_subcategory_vectorizer
        self.description_tokenizer = description_tokenizer
        self.name_tokenizer = name_tokenizer
        self.description_vectorizer = description_vectorizer
        self.name_vectorizer = name_vectorizer

    @abstractmethod
    def fit_register_animal_feature(self):
        raise NotImplementedError

    @abstractmethod
    def register_animal_feature(self):
        raise NotImplementedError


class AnimalFeatureUsecase(AbstractAnimalFeatureUsecase):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        animal_feature_repository: AbstractAnimalFeatureRepository,
        messaging: RabbitmqMessaging,
        cache: AbstractCache,
        animal_category_vectorizer: CategoricalVectorizer,
        animal_subcategory_vectorizer: CategoricalVectorizer,
        description_tokenizer: DescriptionTokenizer,
        name_tokenizer: NameTokenizer,
        description_vectorizer: DescriptionVectorizer,
        name_vectorizer: NameVectorizer,
    ):
        super().__init__(
            animal_repository=animal_repository,
            animal_feature_repository=animal_feature_repository,
            messaging=messaging,
            cache=cache,
            animal_category_vectorizer=animal_category_vectorizer,
            animal_subcategory_vectorizer=animal_subcategory_vectorizer,
            description_tokenizer=description_tokenizer,
            name_tokenizer=name_tokenizer,
            description_vectorizer=description_vectorizer,
            name_vectorizer=name_vectorizer,
        )

    def fit_register_animal_feature(self):
        limit = 1000
        offset = 0
        animals = []
        while True:
            _animals = self.animal_repository.select(
                query=AnimalQuery(deactivated=False),
                limit=limit,
                offset=offset,
            )
            if len(_animals) == 0:
                break
            animals.extend(_animals)
            offset += limit
            logger.info(f"retrieved {len(animals)} data")
        logger.info(f"data size: {len(animals)}")
        if len(animals) == 0:
            logger.info("no data to fit and register")
            return

        ids = [a.id for a in animals]

        logger.info("vectorize animal_category")
        vectorized_animal_category = (
            self.animal_category_vectorizer.fit_transform(
                x=[[a.animal_category_id] for a in animals],
            )
            .toarray()
            .tolist()
        )
        logger.info("vectorize animal_subcategory")
        vectorized_animal_subcategory = (
            self.animal_subcategory_vectorizer.fit_transform(
                x=[[a.animal_subcategory_id] for a in animals],
            )
            .toarray()
            .tolist()
        )

        logger.info("tokenize description")
        tokenized_description = self.description_tokenizer.fit_transform(
            X=[a.description for a in animals],
        ).tolist()
        logger.info("tokenize name")
        tokenized_name = self.name_tokenizer.fit_transform(
            X=[a.name for a in animals],
        ).tolist()

        logger.info("vectorize description")
        vectorized_description = (
            self.description_vectorizer.fit_transform(
                X=tokenized_description,
            )
            .toarray()
            .tolist()
        )
        logger.info("vectorize name")
        vectorized_name = (
            self.name_vectorizer.fit_transform(
                X=tokenized_name,
            )
            .toarray()
            .tolist()
        )

        with open(Configurations.animal_category_vectorizer_file, "wb") as f:
            cloudpickle.dump(self.animal_category_vectorizer, f)
        with open(Configurations.animal_subcategory_vectorizer_file, "wb") as f:
            cloudpickle.dump(self.animal_subcategory_vectorizer, f)
        with open(Configurations.description_vectorizer_file, "wb") as f:
            cloudpickle.dump(self.description_vectorizer, f)
        with open(Configurations.name_vectorizer_file, "wb") as f:
            cloudpickle.dump(self.name_vectorizer, f)

        self.__register_animal_features(
            ids=ids,
            vectorized_animal_category=vectorized_animal_category,
            vectorized_animal_subcategory=vectorized_animal_subcategory,
            tokenized_description=tokenized_description,
            tokenized_name=tokenized_name,
            vectorized_description=vectorized_description,
            vectorized_name=vectorized_name,
            update=True,
        )

    def register_animal_feature(self):
        with open(Configurations.animal_category_vectorizer_file, "rb") as f:
            self.animal_category_vectorizer = cloudpickle.load(f)
        with open(Configurations.animal_subcategory_vectorizer_file, "rb") as f:
            self.animal_subcategory_vectorizer = cloudpickle.load(f)
        with open(Configurations.description_vectorizer_file, "rb") as f:
            self.description_vectorizer = cloudpickle.load(f)
        with open(Configurations.name_vectorizer_file, "rb") as f:
            self.name_vectorizer = cloudpickle.load(f)

        def callback(ch, method, properties, body):
            data = json.loads(body)
            logger.info(f"consumed data: {data}")
            animals = self.animal_repository.select(
                query=AnimalQuery(
                    id=id,
                    deactivated=False,
                ),
                limit=1,
                offset=0,
            )
            if len(animals) == 0:
                return
            ids = [a.id for a in animals]

            vectorized_animal_category = (
                self.animal_category_vectorizer.transform(
                    x=[[a.animal_category_id] for a in animals],
                )
                .toarray()
                .tolist()
            )
            vectorized_animal_subcategory = (
                self.animal_subcategory_vectorizer.transform(
                    x=[[a.animal_subcategory_id] for a in animals],
                )
                .toarray()
                .tolist()
            )

            tokenized_description = self.description_tokenizer.transform(
                X=[a.description for a in animals],
            ).tolist()
            tokenized_name = self.name_tokenizer.transform(
                X=[a.name for a in animals],
            ).tolist()

            vectorized_description = self.description_vectorizer.transform(X=tokenized_description).toarray().tolist()
            vectorized_name = self.name_vectorizer.transform(X=tokenized_name).toarray().tolist()

            self.__register_animal_features(
                ids=ids,
                vectorized_animal_category=vectorized_animal_category,
                vectorized_animal_subcategory=vectorized_animal_subcategory,
                tokenized_description=tokenized_description,
                tokenized_name=tokenized_name,
                vectorized_description=vectorized_description,
                vectorized_name=vectorized_name,
                update=False,
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.messaging.channel.basic_consume(
            queue=Configurations.animal_feature_registry_queue,
            on_message_callback=callback,
        )
        logger.info(f"Waiting for {Configurations.animal_feature_registry_queue} queue...")
        self.messaging.channel.start_consuming()

    def __register_animal_features(
        self,
        ids: List[str],
        vectorized_animal_category: List[List[int]],
        vectorized_animal_subcategory: List[List[int]],
        tokenized_description: List[str],
        tokenized_name: List[str],
        vectorized_description: List[List[float]],
        vectorized_name: List[List[float]],
        update: bool = True,
    ):
        data = [
            dict(
                id=id,
                animal_category_vector=vac,
                animal_subcategory_vector=vas,
                description_words=td.split(" "),
                name_words=tn.split(" "),
                description_vector=vd,
                name_vector=vn,
            )
            for id, vac, vas, td, tn, vd, vn in zip(
                ids,
                vectorized_animal_category,
                vectorized_animal_subcategory,
                tokenized_description,
                tokenized_name,
                vectorized_description,
                vectorized_name,
            )
        ]

        for i in range(0, len(data), 1000):
            target_data = data[i : i + 1000]
            existing_features = self.animal_feature_repository.select(
                query=AnimalFeatureQuery(ids=[d["id"] for d in target_data])
            )
            existing_ids = [f.id for f in existing_features]
            for d in target_data:
                if d["id"] in existing_ids:
                    if update:
                        self.animal_feature_repository.update(record=AnimalFeatureUpdate(**d))
                else:
                    self.animal_feature_repository.insert(record=AnimalFeatureCreate(**d))
                integrated = []
                integrated.extend(d["animal_category_vector"])
                integrated.extend(d["animal_subcategory_vector"])
                integrated.extend(d["description_vector"])
                integrated.extend(d["name_vector"])
                self.cache.set(
                    key=f"{d['id']}_feature",
                    value=json.dumps(integrated),
                    expire_second=60 * 60 * 24 * 30,
                )
            logger.info(f"registered: {i} animal features")
