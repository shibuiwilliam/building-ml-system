import json
from abc import ABC, abstractmethod
from typing import List, Optional

import cloudpickle
from src.configurations import Configurations
from src.entities.animal import AnimalQuery
from src.entities.animal_feature import AnimalFeatureCreate, AnimalFeatureQuery, AnimalFeatureUpdate
from src.infrastructure.cache import AbstractCache
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.middleware.logger import configure_logger
from src.middleware.strings import get_uuid
from src.repository.animal_feature_repository import AbstractAnimalFeatureRepository
from src.repository.animal_repository import AbstractAnimalRepository
from src.request_object.animal_feature import AnimalFeatureInitializeRequest, AnimalFeatureRegistrationRequest
from src.response_object.animal_feature import AnimalFeatureInitializeResponse
from src.service.feature_processing import (
    CategoricalVectorizer,
    DescriptionTokenizer,
    DescriptionVectorizer,
    NameTokenizer,
    NameVectorizer,
)

logger = configure_logger(__name__)


class AbstractAnimalFeatureUsecase(ABC):
    PREFIX = "animal_feature"

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
    def fit_register_animal_feature(
        self,
        request: AnimalFeatureInitializeRequest,
    ) -> Optional[AnimalFeatureInitializeResponse]:
        raise NotImplementedError

    @abstractmethod
    def register_animal_feature(
        self,
        request: AnimalFeatureRegistrationRequest,
    ):
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

    def make_cache_key(
        self,
        animal_id: str,
        mlflow_experiment_id: int,
        mlflow_run_id: str,
    ) -> str:
        return f"{self.PREFIX}_{animal_id}_{mlflow_experiment_id}_{mlflow_run_id}"

    def fit_register_animal_feature(
        self,
        request: AnimalFeatureInitializeRequest,
    ) -> Optional[AnimalFeatureInitializeResponse]:
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
            return None

        animal_ids = [a.id for a in animals]

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
        tokenized_description = self.description_tokenizer.transform(
            X=[a.description for a in animals],
        ).tolist()
        logger.info("tokenize name")
        tokenized_name = self.name_tokenizer.transform(
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
            animal_ids=animal_ids,
            mlflow_experiment_id=request.mlflow_experiment_id,
            mlflow_run_id=request.mlflow_run_id,
            vectorized_animal_categories=vectorized_animal_category,
            vectorized_animal_subcategories=vectorized_animal_subcategory,
            tokenized_descriptions=tokenized_description,
            tokenized_names=tokenized_name,
            vectorized_descriptions=vectorized_description,
            vectorized_names=vectorized_name,
            update=True,
        )
        return AnimalFeatureInitializeResponse(
            animal_category_vectorizer_file=Configurations.animal_category_vectorizer_file,
            animal_subcategory_vectorizer_file=Configurations.animal_subcategory_vectorizer_file,
            description_vectorizer_file=Configurations.description_vectorizer_file,
            name_vectorizer_file=Configurations.name_vectorizer_file,
            animal_ids=animal_ids,
        )

    def register_animal_feature(
        self,
        request: AnimalFeatureRegistrationRequest,
    ):
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
            animal_ids = [a.id for a in animals]

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
                animal_ids=animal_ids,
                mlflow_experiment_id=request.mlflow_experiment_id,
                mlflow_run_id=request.mlflow_run_id,
                vectorized_animal_categories=vectorized_animal_category,
                vectorized_animal_subcategories=vectorized_animal_subcategory,
                tokenized_descriptions=tokenized_description,
                tokenized_names=tokenized_name,
                vectorized_descriptions=vectorized_description,
                vectorized_names=vectorized_name,
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
        animal_ids: List[str],
        mlflow_experiment_id: int,
        mlflow_run_id: str,
        vectorized_animal_categories: List[List[int]],
        vectorized_animal_subcategories: List[List[int]],
        tokenized_descriptions: List[str],
        tokenized_names: List[str],
        vectorized_descriptions: List[List[float]],
        vectorized_names: List[List[float]],
        update: bool = True,
    ):
        for i, (
            animal_id,
            animal_category_vector,
            animal_subcategory_vector,
            description_words,
            name_words,
            description_vector,
            name_vector,
        ) in enumerate(
            zip(
                animal_ids,
                vectorized_animal_categories,
                vectorized_animal_subcategories,
                tokenized_descriptions,
                tokenized_names,
                vectorized_descriptions,
                vectorized_names,
            )
        ):
            _cache = update
            existing_feature = self.animal_feature_repository.select(
                query=AnimalFeatureQuery(
                    animal_id=animal_id,
                    mlflow_experiment_id=mlflow_experiment_id,
                    mlflow_run_id=mlflow_run_id,
                )
            )
            data = dict(
                animal_category_vector=animal_category_vector,
                animal_subcategory_vector=animal_subcategory_vector,
                description_words=description_words.split(" "),
                name_words=name_words.split(" "),
                name_vector=name_vector,
                description_vector=description_vector,
            )
            if len(existing_feature) > 0:
                if update:
                    self.animal_feature_repository.update(
                        record=AnimalFeatureUpdate(
                            id=existing_feature[0].id,
                            **data,
                        )
                    )
                    _cache = True
                else:
                    _cache = False
            else:
                create_record = AnimalFeatureCreate(
                    id=get_uuid(),
                    animal_id=animal_id,
                    mlflow_experiment_id=mlflow_experiment_id,
                    mlflow_run_id=mlflow_run_id,
                    **data,
                )
                self.animal_feature_repository.insert(record=create_record)
                _cache = True

            if _cache:
                key = self.make_cache_key(
                    animal_id=animal_id,
                    mlflow_experiment_id=mlflow_experiment_id,
                    mlflow_run_id=mlflow_run_id,
                )
                self.cache.set(
                    key=key,
                    value=json.dumps(data),
                    expire_second=Configurations.feature_cache_ttl,
                )
            if i % 1000 == 0:
                logger.info(f"registered: {i} animal features")
