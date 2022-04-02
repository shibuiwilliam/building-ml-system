import json
from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from src.configurations import Configurations
from src.constants import CONSTANTS
from src.entities.animal import (
    ANIMAL_INDEX,
    AnimalCreate,
    AnimalIDs,
    AnimalQuery,
    AnimalSearchQuery,
    AnimalSearchSortKey,
)
from src.infrastructure.cache import AbstractCache
from src.infrastructure.messaging import AbstractMessaging
from src.infrastructure.search import AbstractSearch
from src.infrastructure.storage import AbstractStorage
from src.middleware.json import json_serial
from src.middleware.strings import get_uuid
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.like_repository import AbstractLikeRepository
from src.request_object.animal import (
    AnimalCreateRequest,
    AnimalRequest,
    AnimalSearchRequest,
    SimilarAnimalSearchRequest,
)
from src.response_object.animal import (
    AnimalResponse,
    AnimalSearchResponse,
    AnimalSearchResponses,
    SimilarAnimalSearchResponse,
    SimilarAnimalSearchResponses,
)
from src.response_object.user import UserResponse
from src.service.learn_to_rank import AbstractLearnToRankService, LearnToRankRequest
from src.service.local_cache import AbstractLocalCache
from src.service.similar_image_search import AbstractSimilarImageSearchService, SimilarImageSearchRequest

logger = getLogger(__name__)


class AbstractAnimalUsecase(ABC):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        like_repository: AbstractLikeRepository,
        learn_to_rank: AbstractLearnToRankService,
        similar_image_search: AbstractSimilarImageSearchService,
        storage_client: AbstractStorage,
        cache: AbstractCache,
        search_client: AbstractSearch,
        messaging: AbstractMessaging,
        local_cache: AbstractLocalCache,
    ):
        self.animal_repository = animal_repository
        self.like_repository = like_repository
        self.learn_to_rank = learn_to_rank
        self.similar_image_search = similar_image_search
        self.storage_client = storage_client
        self.cache = cache
        self.search_client = search_client
        self.messaging = messaging
        self.local_cache = local_cache

    @abstractmethod
    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalRequest] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AnimalResponse]:
        raise NotImplementedError

    @abstractmethod
    def liked_by(
        self,
        session: Session,
        animal_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        session: Session,
        request: AnimalCreateRequest,
        local_file_path: str,
        background_tasks: BackgroundTasks,
    ) -> Optional[AnimalResponse]:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        request: AnimalSearchRequest,
        background_tasks: BackgroundTasks,
        limit: int = 100,
        offset: int = 0,
    ) -> AnimalSearchResponses:
        raise NotImplementedError

    @abstractmethod
    def search_similar_image(
        self,
        session: Session,
        request: SimilarAnimalSearchRequest,
    ) -> SimilarAnimalSearchResponses:
        raise NotImplementedError


class AnimalUsecase(AbstractAnimalUsecase):
    def __init__(
        self,
        animal_repository: AbstractAnimalRepository,
        like_repository: AbstractLikeRepository,
        learn_to_rank: AbstractLearnToRankService,
        similar_image_search: AbstractSimilarImageSearchService,
        storage_client: AbstractStorage,
        cache: AbstractCache,
        search_client: AbstractSearch,
        messaging: AbstractMessaging,
        local_cache: AbstractLocalCache,
    ):
        super().__init__(
            animal_repository=animal_repository,
            like_repository=like_repository,
            learn_to_rank=learn_to_rank,
            similar_image_search=similar_image_search,
            storage_client=storage_client,
            cache=cache,
            search_client=search_client,
            messaging=messaging,
            local_cache=local_cache,
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
            for q in Configurations.animal_violation_queues:
                background_tasks.add_task(
                    self.messaging.publish,
                    q,
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
        key += f"{'_'.join(sorted(query.phrases))}_"
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
        self.cache.set(
            key=key,
            value=json.dumps(result.dict(), default=json_serial),
            expire_second=60 * 10,
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
        cached = self.cache.get(key=key)
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
        if query.sort_by == AnimalSearchSortKey.LEARN_TO_RANK:
            _ids = {r.id: r for r in results.results}
            learn_to_rank_request = LearnToRankRequest(
                ids=list(_ids.keys()),
                query_phrases=query.phrases,
            )
            if query.animal_category_name_en is not None:
                animal_category_id = self.local_cache.get_animal_category_id_by_name(name=query.animal_category_name_en)
                learn_to_rank_request.query_animal_category_id = animal_category_id
            if query.animal_category_name_ja is not None:
                animal_category_id = self.local_cache.get_animal_category_id_by_name(name=query.animal_category_name_ja)
                learn_to_rank_request.query_animal_category_id = animal_category_id
            if query.animal_subcategory_name_en is not None:
                animal_subcategory_id = self.local_cache.get_animal_subcategory_id_by_name(
                    name=query.animal_subcategory_name_en
                )
                learn_to_rank_request.query_animal_subcategory_id = animal_subcategory_id
            if query.animal_subcategory_name_ja is not None:
                animal_subcategory_id = self.local_cache.get_animal_subcategory_id_by_name(
                    name=query.animal_subcategory_name_ja
                )
                learn_to_rank_request.query_animal_subcategory_id = animal_subcategory_id
            ranked_ids = self.learn_to_rank.reorder(request=learn_to_rank_request)
            _results = [_ids[i] for i in ranked_ids.ids]
            results.results = _results

        searched = AnimalSearchResponses(
            hits=results.hits,
            max_score=results.max_score,
            results=[AnimalSearchResponse(**r.dict()) for r in results.results],
            offset=results.offset,
        )
        if query.sort_by != AnimalSearchSortKey.LEARN_TO_RANK:
            background_tasks.add_task(
                self.__set_search_cache,
                key,
                searched,
            )
        return searched

    def search_similar_image(
        self,
        session: Session,
        request: SimilarAnimalSearchRequest,
    ) -> SimilarAnimalSearchResponses:
        search_request = SimilarImageSearchRequest(id=request.id)
        response = self.similar_image_search.search(request=search_request)
        query = AnimalIDs(ids=response.ids)
        animals = self.animal_repository.select_by_ids(
            session=session,
            query=query,
        )
        likes = self.like_repository.count(
            session=session,
            animal_ids=[a.id for a in animals],
        )
        responses = [
            SimilarAnimalSearchResponse(
                id=a.id,
                name=a.name,
                description=a.description,
                photo_url=a.photo_url,
                animal_category_name_en=a.animal_category_name_en,
                animal_category_name_ja=a.animal_category_name_ja,
                animal_subcategory_name_en=a.animal_subcategory_name_en,
                animal_subcategory_name_ja=a.animal_subcategory_name_ja,
                user_handle_name=a.user_handle_name,
                like=likes[a.id].count,
                created_at=a.created_at,
            )
            for a in animals
        ]
        return SimilarAnimalSearchResponses(results=responses)
