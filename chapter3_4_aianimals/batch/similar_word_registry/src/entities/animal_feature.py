from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Extra


class AnimalFeatureQuery(BaseModel):
    id: Optional[str] = None
    animal_id: Optional[str] = None
    mlflow_experiment_id: Optional[int] = None
    mlflow_run_id: Optional[str] = None

    class Config:
        extra = Extra.forbid


class AnimalFeatureCreate(BaseModel):
    id: str
    animal_id: str
    mlflow_experiment_id: int
    mlflow_run_id: str
    animal_category_vector: Union[Dict, List]
    animal_subcategory_vector: Union[Dict, List]
    name_words: List[str]
    name_vector: List[float]
    description_words: List[str]
    description_vector: List[float]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        extra = Extra.forbid


class AnimalFeatureUpdate(BaseModel):
    id: str
    animal_category_vector: Optional[Union[Dict, List]]
    animal_subcategory_vector: Optional[Union[Dict, List]]
    name_words: Optional[List[str]]
    name_vector: Optional[List[float]]
    description_words: Optional[List[str]]
    description_vector: Optional[List[float]]

    class Config:
        extra = Extra.forbid


class AnimalFeatureModel(BaseModel):
    id: str
    animal_id: str
    mlflow_experiment_id: int
    mlflow_run_id: str
    animal_category_vector: Union[Dict, List]
    animal_subcategory_vector: Union[Dict, List]
    name_words: List[str]
    name_vector: List[float]
    description_words: List[str]
    description_vector: List[float]
    created_at: datetime
    updated_at: datetime
