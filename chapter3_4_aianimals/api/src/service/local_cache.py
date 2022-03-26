from abc import ABC, abstractmethod
from logging import getLogger
from typing import Dict, Optional, Union

from src.infrastructure.database import AbstractDatabase
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository

logger = getLogger(__name__)


class AbstractLocalCache(ABC):
    def __init__(
        self,
        animal_category_repository: AbstractAnimalCategoryRepository,
        animal_subcategory_repository: AbstractAnimalSubcategoryRepository,
        database=AbstractDatabase,
    ):
        self.animal_category_repository = animal_category_repository
        self.animal_subcategory_repository = animal_subcategory_repository
        self.database = database
        self.cache: Dict[str, Union[str, Dict]] = {}

    @abstractmethod
    def get(
        self,
        key: str,
    ) -> Optional[Union[str, int, Dict]]:
        raise NotImplementedError

    @abstractmethod
    def get_animal_category_id_by_name(
        self,
        name: str,
    ) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    def get_animal_subcategory_id_by_name(
        self,
        name: str,
    ) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    def get_animal_category_by_id(
        self,
        id: int,
    ) -> Optional[Dict]:
        raise NotImplementedError

    @abstractmethod
    def get_animal_subcategory_by_id(
        self,
        id: int,
    ) -> Optional[Dict]:
        raise NotImplementedError


class LocalCache(AbstractLocalCache):
    def __init__(
        self,
        animal_category_repository: AbstractAnimalCategoryRepository,
        animal_subcategory_repository: AbstractAnimalSubcategoryRepository,
        database=AbstractDatabase,
    ):
        super().__init__(
            animal_category_repository=animal_category_repository,
            animal_subcategory_repository=animal_subcategory_repository,
            database=database,
        )
        self.initialize()

    def initialize(self):
        session = self.database.get_session().__next__()
        try:
            animal_categories = self.animal_category_repository.select(session=session)
            for animal_category in animal_categories:
                if not animal_category.is_deleted:
                    key = self.make_animal_category_key(subkey=animal_category.name_en)
                    self.cache[key] = animal_category.id
                    key = self.make_animal_category_key(subkey=animal_category.name_ja)
                    self.cache[key] = animal_category.id
                    key = self.make_animal_category_key(subkey=animal_category.id)
                    self.cache[key] = animal_category.dict()
                logger.info(f"cached animal category: {animal_category.id}")
            animal_subcategories = self.animal_subcategory_repository.select(session=session)
            for animal_subcategory in animal_subcategories:
                if not animal_subcategory.is_deleted:
                    key = self.make_animal_subcategory_key(subkey=animal_subcategory.name_en)
                    self.cache[key] = animal_subcategory.id
                    key = self.make_animal_subcategory_key(subkey=animal_subcategory.name_ja)
                    self.cache[key] = animal_subcategory.id
                    key = self.make_animal_subcategory_key(subkey=animal_subcategory.id)
                    self.cache[key] = animal_subcategory.dict()
                logger.info(f"cached animal subcategory: {animal_subcategory.id}")
        except Exception as e:
            raise e
        finally:
            session.close()

    def make_animal_category_key(
        self,
        subkey: Union[int, str],
    ) -> str:
        return f"animal_category_{subkey}"

    def make_animal_subcategory_key(
        self,
        subkey: Union[int, str],
    ) -> str:
        return f"animal_subcategory_{subkey}"

    def get(
        self,
        key: str,
    ) -> Optional[Union[str, Dict]]:
        return self.cache.get(key, None)

    def get_animal_category_id_by_name(
        self,
        name: str,
    ) -> Optional[int]:
        key = self.make_animal_category_key(subkey=name)
        value = self.get(key=key)
        if isinstance(value, int):
            return value
        return None

    def get_animal_subcategory_id_by_name(
        self,
        name: str,
    ) -> Optional[int]:
        key = self.make_animal_subcategory_key(subkey=name)
        value = self.get(key=key)
        if isinstance(value, int):
            return value
        return None

    def get_animal_category_by_id(
        self,
        id: int,
    ) -> Optional[Dict]:
        key = self.make_animal_category_key(subkey=id)
        value = self.get(key=key)
        if isinstance(value, Dict):
            return value
        return None

    def get_animal_subcategory_by_id(
        self,
        id: int,
    ) -> Optional[Dict]:
        key = self.make_animal_subcategory_key(subkey=id)
        value = self.get(key=key)
        if isinstance(value, Dict):
            return value
        return None
