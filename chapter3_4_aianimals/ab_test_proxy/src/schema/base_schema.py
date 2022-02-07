from typing import Dict, Generic, List, TypeVar, Union

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class BaseRequest(BaseModel):
    request: Union[Dict, List]


class BaseResponse(BaseModel):
    endpoint: str
    response: Union[Dict, List]


class BaseRandomABTestRequest(BaseRequest):
    pass


class BaseRandomABTestResponse(BaseResponse):
    pass


class BaseUserRequest(BaseRequest):
    user_id: str


class BaseUserResponse(BaseResponse):
    pass


class BaseAnimalRequest(BaseRequest):
    animal_id: str


class BaseAnimalResponse(BaseResponse):
    pass
