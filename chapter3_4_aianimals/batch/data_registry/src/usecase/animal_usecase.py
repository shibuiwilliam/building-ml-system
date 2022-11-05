import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from src.configurations import Configurations
from src.entities.animal import AnimalCreate, AnimalQuery
from src.entities.animal_search import ANIMAL_MAPPING, ANIMAL_MAPPING_NAME, AnimalDocument
from src.infrastructure.cache import AbstractCache
from src.infrastructure.messaging import RabbitmqMessaging
from src.infrastructure.search import AbstractSearch
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike


class AbstractAnimalUsecase(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        like_repository: AbstractLikeRepository,
        search: AbstractSearch,
        messaging: RabbitmqMessaging,
        cache: AbstractCache,
    ):
        self.logger = logging.getLogger(__name__)
        self.animal_repository = animal_repository
        self.like_repository = like_repository
        self.search = search
        self.messaging = messaging
        self.cache = cache

    @abstractmethod
    def ping_search(self) -> bool:
        raise NotImplementedError

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


class AnimalUsecase(AbstractAnimalUsecase):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        like_repository: AbstractLikeRepository,
        search: AbstractSearch,
        messaging: RabbitmqMessaging,
        cache: AbstractCache,
    ):
        super().__init__(
            animal_repository=animal_repository,
            like_repository=like_repository,
            search=search,
            messaging=messaging,
            cache=cache,
        )

    def ping_search(self) -> bool:
        try:
            self.search.info()
            return True
        except:
            return False

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
        self.logger.info(f"register: {request}")
        exists = self.animal_repository.select(
            query=AnimalQuery(id=request.id),
        )
        if len(exists) > 0:
            response = AnimalResponse(**exists[0].dict())
            self.logger.info(f"data already exists: {response}")
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
            self.logger.info(f"done register: {response}")
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
        self.logger.info(f"animal_id: {animal_id}")
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
        self.logger.info(f"registered: {animal_id}")

    def register_document_from_queue(self):
        def callback(ch, method, properties, body):
            data = json.loads(body)
            self.logger.info(f"consumed data: {data}")
            try:
                self.register_document(animal_id=data["id"])
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                self.logger.error(f"failed to register document: {e}")
                ch.basic_reject(
                    delivery_tag=method.delivery_tag,
                    requeue=True,
                )

        self.messaging.channel.basic_consume(
            queue=Configurations.animal_registry_queue,
            on_message_callback=callback,
        )
        self.logger.info(f"Waiting for {Configurations.animal_registry_queue} queue...")
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
            self.logger.info(f"bulk register animal: {i} to {i+200}")
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
