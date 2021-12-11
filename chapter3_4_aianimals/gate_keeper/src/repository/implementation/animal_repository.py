from typing import Dict, List, Optional, Tuple

from sqlalchemy import and_
from src.entities.animal import ANIMAL_MAPPING, ANIMAL_MAPPING_NAME, AnimalDocument, AnimalModel, AnimalQuery
from src.infrastructure.database import AbstractDatabase
from src.infrastructure.queue import AbstractQueue
from src.infrastructure.search import AbstractSearch
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.schema.animal import Animal
from src.schema.animal_category import AnimalCategory
from src.schema.animal_subcategory import AnimalSubcategory

logger = configure_logger(__name__)


class AnimalRepository(AbstractAnimalRepository):
    def __init__(
        self,
        database: AbstractDatabase,
        queue: AbstractQueue,
        search: AbstractSearch,
    ):
        super().__init__(
            database=database,
            queue=queue,
            search=search,
        )
        self.queue_name = "animal"

    def select(
        self,
        query: Optional[AnimalQuery],
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalModel]:
        session = self.database.get_session().__next__()
        filters = []
        if query is not None:
            if query.id is not None:
                filters.append(Animal.id == query.id)
            if query.name is not None:
                filters.append(Animal.name == query.name)
            if query.animal_category_id is not None:
                filters.append(Animal.animal_category_id == query.animal_category_id)
            if query.animal_subcategory_id is not None:
                filters.append(Animal.animal_subcategory_id == query.animal_subcategory_id)
            if query.user_id is not None:
                filters.append(Animal.id == query.user_id)
            if query.deactivated is not None:
                filters.append(Animal.deactivated == query.deactivated)
        results = (
            session.query(
                Animal.id.label("id"),
                AnimalCategory.id.label("animal_category_id"),
                AnimalCategory.name_en.label("animal_category_name_en"),
                AnimalCategory.name_ja.label("animal_category_name_ja"),
                AnimalSubcategory.id.label("animal_subcategory_id"),
                AnimalSubcategory.name_en.label("animal_subcategory_name_en"),
                AnimalSubcategory.name_ja.label("animal_subcategory_name_ja"),
                Animal.name.label("name"),
                Animal.description.label("description"),
                Animal.photo_url.label("photo_url"),
                Animal.deactivated.label("deactivated"),
                Animal.created_at.label("created_at"),
                Animal.updated_at.label("updated_at"),
            )
            .join(
                AnimalCategory,
                AnimalCategory.id == Animal.animal_category_id,
                isouter=True,
            )
            .join(
                AnimalSubcategory,
                AnimalSubcategory.id == Animal.animal_subcategory_id,
                isouter=True,
            )
            .filter(and_(*filters))
            .order_by(Animal.id)
            .limit(limit)
            .offset(offset)
        )
        data = [
            AnimalModel(
                id=d[0],
                animal_category_id=d[1],
                animal_category_name_en=d[2],
                animal_category_name_ja=d[3],
                animal_subcategory_id=d[4],
                animal_subcategory_name_en=d[5],
                animal_subcategory_name_ja=d[6],
                name=d[7],
                description=d[8],
                photo_url=d[9],
                deactivated=d[10],
                created_at=d[11],
                updated_at=d[12],
            )
            for d in results
        ]
        session.close()
        return data

    def dequeue(self) -> Optional[Tuple[int, str, float, bool]]:
        return self.queue.dequeue(queue_name=self.queue_name)

    def create_index(
        self,
        index: str = ANIMAL_MAPPING_NAME,
        body: Dict = ANIMAL_MAPPING,
    ):
        self.search.create_index(
            index=index,
            body=body,
        )

    def get_index(self) -> Dict:
        return self.search.get_index(index=ANIMAL_MAPPING_NAME)

    def index_exists(self) -> bool:
        return self.search.index_exists(index=ANIMAL_MAPPING_NAME)

    def create_document(
        self,
        id: str,
        document: AnimalDocument,
        index: str = ANIMAL_MAPPING_NAME,
    ):
        body = document.dict()
        self.search.create_document(
            index=index,
            id=id,
            body=body,
        )
