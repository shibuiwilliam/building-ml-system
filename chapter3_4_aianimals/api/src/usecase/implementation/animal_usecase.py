import json
from logging import getLogger
from typing import List, Optional

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from src.configurations import Configurations
from src.constants import CONSTANTS
from src.entities.animal import ANIMAL_INDEX, AnimalCreate, AnimalQuery, AnimalSearchQuery, AnimalSearchSortKey
from src.infrastructure.messaging import AbstractMessaging
from src.infrastructure.queue import AbstractQueue
from src.infrastructure.search import AbstractSearch
from src.infrastructure.storage import AbstractStorage
from src.middleware.json import json_serial
from src.middleware.strings import get_uuid
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest, AnimalSearchRequest
from src.response_object.animal import AnimalResponse, AnimalSearchResponse, AnimalSearchResponses
from src.response_object.user import UserResponse
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = getLogger(__name__)


class AnimalUsecase(AbstractAnimalUsecase):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        like_repository: AbstractLikeRepository,
        storage_client: AbstractStorage,
        queue: AbstractQueue,
        search_client: AbstractSearch,
        messaging: AbstractMessaging,
    ):
        super().__init__(
            animal_repository=animal_repository,
            like_repository=like_repository,
            storage_client=storage_client,
            queue=queue,
            search_client=search_client,
            messaging=messaging,
        )

    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalResponse]:
        if limit > 200:
            raise ValueError
        query: Optional[AnimalQuery] = None
        if request is not None:
            query = AnimalQuery(**request.dict())
        data = self.animal_repository.select(
            session=session,
            query=query,
            limit=limit,
            offset=offset,
        )
        like = self.like_repository.count(
            session=session,
            animal_ids=[a.id for a in data],
        )
        response = [AnimalResponse(like=like[d.id].count, **d.dict()) for d in data]
        return response

    def liked_by(
        self,
        session: Session,
        animal_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[UserResponse]:
        if limit > 200:
            raise ValueError
        data = self.animal_repository.liked_by(
            session=session,
            animal_id=animal_id,
            limit=limit,
            offset=offset,
        )
        response = [UserResponse(**d.dict()) for d in data]
        return response

    def register(
        self,
        session: Session,
        request: AnimalCreateRequest,
        local_file_path: str,
        background_tasks: BackgroundTasks,
    ) -> Optional[AnimalResponse]:
        id = get_uuid()
        photo_url = self.storage_client.make_photo_url(uuid=id)
        background_tasks.add_task(
            self.storage_client.upload_image,
            id,
            local_file_path,
        )
        logger.info(f"uploaded image to {photo_url}")
        record = AnimalCreate(
            id=id,
            animal_category_id=request.animal_category_id,
            animal_subcategory_id=request.animal_subcategory_id,
            user_id=request.user_id,
            name=request.name,
            description=request.description,
            photo_url=photo_url,
        )
        data = self.animal_repository.insert(
            session=session,
            record=record,
            commit=True,
        )
        if data is not None:
            response = AnimalResponse(**data.dict())
            background_tasks.add_task(
                self.messaging.publish,
                Configurations.no_animal_violation_queue,
                {"id": data.id},
            )
            return response
        return None

    def __make_search_key(
        self,
        query: AnimalSearchQuery,
        limit: int = 100,
        offset: int = 0,
    ) -> str:
        key = f"{CONSTANTS.ANIMAL_SEARCH_CACHE_PREFIX}_"
        key += f"{query.user_id}_"
        key += f"{query.animal_category_name_en}_"
        key += f"{query.animal_category_name_ja}_"
        key += f"{query.animal_subcategory_name_en}_"
        key += f"{query.animal_subcategory_name_ja}_"
        key += f"{'_'.join(query.phrases)}_"
        key += f"{limit}_"
        key += f"{offset}_"
        key += query.sort_by.value
        return key

    def __set_search_cache(
        self,
        key: str,
        result: AnimalSearchResponses,
    ):
        logger.info(f"save cache: {key}")
        self.queue.set(
            key=key,
            value=json.dumps(result.dict(), default=json_serial),
        )

    def search(
        self,
        request: AnimalSearchRequest,
        background_tasks: BackgroundTasks,
        limit: int = 100,
        offset: int = 0,
    ) -> AnimalSearchResponses:
        sort_by = AnimalSearchSortKey.value_to_key(value=request.sort_by)
        query = AnimalSearchQuery(
            user_id=request.user_id,
            animal_category_name_en=request.animal_category_name_en,
            animal_category_name_ja=request.animal_category_name_ja,
            animal_subcategory_name_en=request.animal_subcategory_name_en,
            animal_subcategory_name_ja=request.animal_subcategory_name_ja,
            phrases=request.phrases,
            sort_by=sort_by,
        )
        logger.info(f"search query: {query}")
        key = self.__make_search_key(
            query=query,
            limit=limit,
            offset=offset,
        )
        cached = self.queue.get(key=key)
        if cached is not None and isinstance(cached, str):
            cache = json.loads(cached)
            logger.info(f"hit cache: {key}")
            searched = AnimalSearchResponses(**cache)
            return searched
        results = self.search_client.search(
            index=ANIMAL_INDEX,
            query=query,
            from_=offset,
            size=limit,
        )
        searched = AnimalSearchResponses(
            hits=results.hits,
            max_score=results.max_score,
            results=[AnimalSearchResponse(**r.dict()) for r in results.results],
            offset=results.offset,
        )
        background_tasks.add_task(
            self.__set_search_cache,
            key,
            searched,
        )
        return searched
