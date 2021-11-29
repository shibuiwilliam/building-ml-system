from typing import Optional

from src.schema.abstract_schema import AbstractCreate, AbstractModel, AbstractQuery


class AnimalCategoryQuery(AbstractQuery):
    id: Optional[str]
    name: Optional[str]


class AnimalCategoryCreate(AbstractCreate):
    id: str
    name: str


class AnimalCategoryModel(AbstractModel):
    id: str
    name: str
