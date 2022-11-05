from typing import Dict, Generic, List, TypeVar, Union

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class BaseRequest(BaseModel):
    request: Union[Dict, List, str, int, float, bool]


class BaseResponse(BaseModel):
    endpoint: str
    response: Union[Dict, List, str, int, float, bool]


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


class GenericRequest(GenericModel, Generic[T]):
    request: T


class Request(GenericRequest[T], Generic[T]):
    pass


class GenericResponse(GenericModel, Generic[T]):
    response: T


class Response(GenericResponse[T], Generic[T]):
    pass
