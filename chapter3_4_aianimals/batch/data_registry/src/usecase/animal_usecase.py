import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

import cloudpickle
from src.configurations import Configurations
from src.service.text_processing import DescriptionTokenizer, DescriptionVectorizer, NameTokenizer, NameVectorizer
from src.entities.animal import AnimalCreate, AnimalQuery
from src.entities.animal_feature import AnimalFeatureCreate, AnimalFeatureQuery, AnimalFeatureUpdate
from src.entities.animal_search import ANIMAL_MAPPING, ANIMAL_MAPPING_NAME, AnimalDocument
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.infrastructure.search import AbstractSearch
from src.middleware.logger import configure_logger
from src.repository.animal_feature_repository import AbstractAnimalFeatureRepository
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike

logger = configure_logger(__name__)


class AbstractAnimalUsecase(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        like_repository: AbstractLikeRepository,
        animal_feature_repository: AbstractAnimalFeatureRepository,
        search: AbstractSearch,
        messaging: RabbitmqMessaging,
        description_tokenizer: DescriptionTokenizer,
        name_tokenizer: NameTokenizer,
        description_vectorizer: DescriptionVectorizer,
        name_vectorizer: NameVectorizer,
    ):
        self.animal_repository = animal_repository
        self.like_repository = like_repository
        self.animal_feature_repository = animal_feature_repository
        self.search = search
        self.messaging = messaging

        self.description_tokenizer = description_tokenizer
        self.name_tokenizer = name_tokenizer
        self.description_vectorizer = description_vectorizer
        self.name_vectorizer = name_vectorizer

    @abstractmethod
    def retrieve(
        self,
        request: Optional[AnimalRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalResponseWithLike]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        request: AnimalCreateRequest,
    ) -> Optional[AnimalResponse]:
        raise NotImplementedError

    @abstractmethod
    def create_index(self):
        raise NotImplementedError

    @abstractmethod
    def get_index(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def index_exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def register_document(
        self,
        animal_id: str,
    ):
        raise NotImplementedError

    @abstractmethod
    def register_document_from_queue(self):
        raise NotImplementedError

    @abstractmethod
    def bulk_register(
        self,
        requests: List[AnimalCreateRequest],
    ):
        raise NotImplementedError

    @abstractmethod
    def fit_register_animal_feature(self):
        raise NotImplementedError

    @abstractmethod
    def register_animal_feature(self):
        raise NotImplementedError


class AnimalUsecase(AbstractAnimalUsecase):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        like_repository: AbstractLikeRepository,
        animal_feature_repository: AbstractAnimalFeatureRepository,
        search: AbstractSearch,
        messaging: RabbitmqMessaging,
        description_tokenizer: DescriptionTokenizer,
        name_tokenizer: NameTokenizer,
        description_vectorizer: DescriptionVectorizer,
        name_vectorizer: NameVectorizer,
    ):
        super().__init__(
            animal_repository=animal_repository,
            like_repository=like_repository,
            animal_feature_repository=animal_feature_repository,
            search=search,
            messaging=messaging,
            description_tokenizer=description_tokenizer,
            name_tokenizer=name_tokenizer,
            description_vectorizer=description_vectorizer,
            name_vectorizer=name_vectorizer,
        )

    def retrieve(
        self,
        request: Optional[AnimalRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalResponseWithLike]:
        if limit > 200:
            raise ValueError
        query: Optional[AnimalQuery] = None
        if request is not None:
            query = AnimalQuery(**request.dict())
        data = self.animal_repository.select(
            query=query,
            limit=limit,
            offset=offset,
        )
        response = [AnimalResponseWithLike(**d.dict()) for d in data]
        return response

    def register(
        self,
        request: AnimalCreateRequest,
    ) -> Optional[AnimalResponse]:
        logger.info(f"register: {request}")
        exists = self.animal_repository.select(
            query=AnimalQuery(id=request.id),
        )
        if len(exists) > 0:
            response = AnimalResponse(**exists[0].dict())
            logger.info(f"data already exists: {response}")
            return response

        record = AnimalCreate(
            id=request.id,
            animal_category_id=request.animal_category_id,
            animal_subcategory_id=request.animal_subcategory_id,
            user_id=request.user_id,
            name=request.name,
            description=request.description,
            photo_url=request.photo_url,
            created_at=request.created_at,
        )
        data = self.animal_repository.insert(
            record=record,
            commit=True,
        )
        if data is not None:
            response = AnimalResponse(**data.dict())
            self.messaging.publish(
                queue_name=Configurations.animal_registry_queue,
                body={"id": data.id},
            )
            for q in Configurations.animal_violation_queues:
                self.messaging.publish(
                    queue_name=q,
                    body={"id": data.id},
                )
            logger.info(f"done register: {response}")
            return response
        return None

    def create_index(self):
        self.search.create_index(
            index=ANIMAL_MAPPING_NAME,
            body=ANIMAL_MAPPING,
        )

    def get_index(self) -> Dict:
        return self.search.get_index(index=ANIMAL_MAPPING_NAME)

    def index_exists(self) -> bool:
        return self.search.index_exists(index=ANIMAL_MAPPING_NAME)

    def register_document(
        self,
        animal_id: str,
    ):
        logger.info(f"animal_id: {animal_id}")
        query = AnimalQuery(
            id=animal_id,
            deactivated=False,
        )
        animals = self.animal_repository.select(
            query=query,
            limit=1,
            offset=0,
        )
        if len(animals) == 0:
            return
        animal = animals[0]

        like = self.like_repository.count(animal_ids=[animal.id])

        document = AnimalDocument(
            name=animal.name,
            description=animal.description,
            animal_category_name_en=animal.animal_category_name_en,
            animal_category_name_ja=animal.animal_category_name_ja,
            animal_subcategory_name_en=animal.animal_subcategory_name_en,
            animal_subcategory_name_ja=animal.animal_subcategory_name_ja,
            photo_url=animal.photo_url,
            user_handle_name=animal.user_handle_name,
            like=like[animal.id].count,
            created_at=animal.created_at,
        )
        if self.search.is_document_exist(
            index=ANIMAL_MAPPING_NAME,
            id=animal.id,
        ):
            self.search.update_document(
                index=ANIMAL_MAPPING_NAME,
                id=animal.id,
                doc=document.dict(),
            )
        else:
            self.search.create_document(
                index=ANIMAL_MAPPING_NAME,
                id=animal.id,
                body=document.dict(),
            )
        logger.info(f"registered: {animal_id}")

    def register_document_from_queue(self):
        def callback(ch, method, properties, body):
            data = json.loads(body)
            logger.info(f"consumed data: {data}")
            self.register_document(animal_id=data["id"])
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.messaging.channel.basic_consume(
            queue=Configurations.animal_registry_queue,
            on_message_callback=callback,
        )
        logger.info(f"Waiting for {Configurations.animal_registry_queue} queue...")
        self.messaging.channel.start_consuming()

    def bulk_register(
        self,
        requests: List[AnimalCreateRequest],
    ):
        records = [
            AnimalCreate(
                id=request.id,
                animal_category_id=request.animal_category_id,
                animal_subcategory_id=request.animal_subcategory_id,
                user_id=request.user_id,
                name=request.name,
                description=request.description,
                photo_url=request.photo_url,
                created_at=request.created_at,
                updated_at=datetime.now(),
            )
            for request in requests
        ]
        for i in range(0, len(records), 200):
            _records = records[i : i + 200]
            self.animal_repository.bulk_insert(
                records=_records,
                commit=True,
            )
            logger.info(f"bulk register animal: {i} to {i+200}")
            for r in _records:
                self.messaging.publish(
                    queue_name=Configurations.animal_registry_queue,
                    body={"id": r.id},
                )
                for q in Configurations.animal_violation_queues:
                    self.messaging.publish(
                        queue_name=q,
                        body={"id": r.id},
                    )

    def fit_register_animal_feature(self):
        limit = 100
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
        descriptions = [a.description for a in animals]
        names = [a.name for a in animals]

        logger.info("tokenize description")
        tokenized_description = self.description_tokenizer.fit_transform(X=descriptions).tolist()
        logger.info("tokenize name")
        tokenized_name = self.name_tokenizer.fit_transform(X=names).tolist()

        logger.info("vectorize description")
        vectorized_description = self.description_vectorizer.fit_transform(X=tokenized_description).toarray().tolist()
        logger.info("vectorize name")
        vectorized_name = self.name_vectorizer.fit_transform(X=tokenized_name).toarray().tolist()

        with open(Configurations.description_vectorizer_file, "wb") as f:
            cloudpickle.dump(self.description_vectorizer, f)
        with open(Configurations.name_vectorizer_file, "wb") as f:
            cloudpickle.dump(self.name_vectorizer, f)

        self.__register_animal_features(
            ids=ids,
            tokenized_description=tokenized_description,
            tokenized_name=tokenized_name,
            vectorized_description=vectorized_description,
            vectorized_name=vectorized_name,
            update=True,
        )

    def register_animal_feature(self):
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
            descriptions = [a.description for a in animals]
            names = [a.name for a in animals]

            tokenized_description = self.description_tokenizer.transform(X=descriptions).tolist()
            tokenized_name = self.name_tokenizer.transform(X=names).tolist()

            vectorized_description = self.description_vectorizer.transform(X=tokenized_description).toarray().tolist()
            vectorized_name = self.name_vectorizer.transform(X=tokenized_name).toarray().tolist()

            self.__register_animal_features(
                ids=ids,
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
        tokenized_description: List[str],
        tokenized_name: List[str],
        vectorized_description: List[List[float]],
        vectorized_name: List[List[float]],
        update: bool = True,
    ):
        data = [
            dict(
                id=id,
                description_words=td.split(" "),
                name_words=tn.split(" "),
                description_vector=vd,
                name_vector=vn,
            )
            for id, td, tn, vd, vn in zip(
                ids,
                tokenized_description,
                tokenized_name,
                vectorized_description,
                vectorized_name,
            )
        ]

        for i in range(0, len(data), 100):
            target_data = data[i : i + 100]
            existing_features = self.animal_feature_repository.select(
                query=AnimalFeatureQuery(ids=[d["id"] for d in target_data])
            )
            existing_ids = [f.id for f in existing_features]
            for d in target_data:
                logger.info(f"AAAAAAAAAAAAAAAAA {d}")
                if d["id"] in existing_ids:
                    if update:
                        self.animal_feature_repository.update(record=AnimalFeatureUpdate(**d))
                else:
                    self.animal_feature_repository.insert(record=AnimalFeatureCreate(**d))
            logger.info(f"registered: {i} animal features")
