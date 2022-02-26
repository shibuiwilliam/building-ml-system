from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Extra


class AnimalFeatureQuery(BaseModel):
    ids: List[str]

    class Config:
        extra = Extra.forbid


class AnimalFeatureCreate(BaseModel):
    id: str
    name_words: Union[Dict, List]
    name_vector: Union[Dict, List]
    description_words: Union[Dict, List]
    description_vector: Union[Dict, List]
    deactivated: bool = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        extra = Extra.forbid


class AnimalFeatureUpdate(BaseModel):
    id: str
    name_words: Optional[Union[Dict, List]]
    name_vector: Optional[Union[Dict, List]]
    description_words: Optional[Union[Dict, List]]
    description_vector: Optional[Union[Dict, List]]
    deactivated: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalFeatureModel(BaseModel):
    id: str
    name_words: Union[Dict, List]
    name_vector: Union[Dict, List]
    description_words: Union[Dict, List]
    description_vector: Union[Dict, List]
    deactivated: bool = False
    created_at: datetime
    updated_at: datetime
