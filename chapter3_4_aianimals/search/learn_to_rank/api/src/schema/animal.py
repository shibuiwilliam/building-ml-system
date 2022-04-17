from typing import Dict, List, Optional

from pydantic import BaseModel, Extra
from src.configurations import Configurations


class AnimalRequest(BaseModel):
    ids: List[str]
    query_phrases: List[str] = []
    query_animal_category_id: Optional[int] = None
    query_animal_subcategory_id: Optional[int] = None

    class Config:
        extra = Extra.forbid


class AnimalResponse(BaseModel):
    ids: List[str]
    model_name: Optional[str] = Configurations.mlflow_run_id

    class Config:
        extra = Extra.forbid


class AnimalRequestResponse(BaseModel):
    request: Dict[str, str] = dict(
        ids="[str]",
        query_phrases="[str]",
        query_animal_category_id="Optional[int]",
        query_animal_subcategory_id="Optional[int]",
    )
    response: Dict[str, str] = dict(
        ids="[str]",
    )
