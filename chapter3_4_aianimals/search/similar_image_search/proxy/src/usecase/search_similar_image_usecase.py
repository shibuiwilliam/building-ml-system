from abc import ABC, abstractmethod
from logging import getLogger
from typing import List

from io import BytesIO
from PIL import Image
import httpx
from fastapi import BackgroundTasks
from src.service.predictor import AbstractPredictor
from src.infrastructure.cache_client import AbstractCacheClient
from src.repository.animal_repository import AnimalQuery, AnimalRepository
from src.schema.animal import AnimalRequest, AnimalResponse

logger = getLogger(__name__)


class AbstractSearchSimilarImageUsecase(ABC):
    def __init__(
        self,
        animal_repository: AnimalRepository,
        cache_client: AbstractCacheClient,
        predictor: AbstractPredictor,
        threshold: int = 100,
        timeout: float = 10.0,
        retries: int = 3,
    ):
        self.animal_repository = animal_repository
        self.cache_client = cache_client
        self.predictor = predictor
        self.threshold = threshold
        self.timeout = timeout
        self.transport = httpx.HTTPTransport(
            retries=retries,
        )

    @abstractmethod
    def search(
        self,
        request: AnimalRequest,
        background_tasks: BackgroundTasks,
    ) -> AnimalResponse:
        raise NotImplementedError


class SearchSimilarImageUsecase(AbstractSearchSimilarImageUsecase):
    def __init__(
        self,
        animal_repository: AnimalRepository,
        cache_client: AbstractCacheClient,
        predictor: AbstractPredictor,
        threshold: int = 100,
        timeout: float = 10.0,
        retries: int = 3,
    ):
        super().__init__(
            animal_repository=animal_repository,
            cache_client=cache_client,
            predictor=predictor,
            threshold=threshold,
            timeout=timeout,
            retries=retries,
        )

    def __set_prediction_cache(
        self,
        animal_id: str,
        similar_animal_ids: List[str],
    ):
        logger.info(f"register cache: {animal_id} {similar_animal_ids}")
        self.cache_client.set(
            key=animal_id,
            value=",".join(similar_animal_ids),
        )

    def search(
        self,
        request: AnimalRequest,
        background_tasks: BackgroundTasks,
    ) -> AnimalResponse:
        cache_key = f"similar_image_{request.id}"
        cached_data = self.cache_client.get(key=cache_key)
        if cached_data is not None:
            logger.info(f"cache hit: {cache_key}")
            return AnimalResponse(ids=cached_data.split(","))

        source_animals = self.animal_repository.select(
            animal_query=AnimalQuery(id=request.id),
            limit=1,
            offset=0,
        )
        if len(source_animals) != 1:
            logger.error(f"no animal found {request.id}")
            return AnimalResponse(ids=[])
        source_animal = source_animals[0]

        with httpx.Client(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            res = client.get(source_animal.photo_url)
        if res.status_code != 200:
            logger.error(f"failed to download {source_animal.id} {source_animal.photo_url}")
            return AnimalResponse(ids=[])
        img = Image.open(BytesIO(res.content))
        if img.mode == "RGBA":
            img_rgb = Image.new("RGB", (img.height, img.width), (255, 255, 255))
            img_rgb.paste(img, mask=img.split()[3])
            img = img_rgb

        prediction = self.predictor.predict(img=img)
        if prediction is None:
            logger.error(f"failed to search {source_animal.id}")
            return AnimalResponse(ids=[])
        logger.info(f"similarities: {request.id} {prediction}")

        animals_ids = [
            animal_id
            for animal_id, similarity in zip(prediction.animal_ids, prediction.similarities)
            if similarity >= self.threshold
        ]
        background_tasks.add_task(
            self.__set_prediction_cache,
            cache_key,
            animals_ids,
        )
        return AnimalResponse(ids=animals_ids)
