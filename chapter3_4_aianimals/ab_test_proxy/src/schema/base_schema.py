from typing import Dict, List, Union

from pydantic import BaseModel, create_model


class BaseRequest(BaseModel):
    pass


class BaseResponse(BaseModel):
    endpoint: str
    pass


class BaseRandomABTestRequest(BaseRequest):
    pass


class BaseRandomABTestResponse(BaseResponse):
    pass


class BaseUserRequest(BaseRequest):
    user_id: str


class BaseUserResponse(BaseResponse):
    pass


# UserRequest = create_model(
#     "UserRequest",
#     __base__=__UserRequest,
# )

# UserResponse = create_model(
#     "UserResponse",
#     __base__=__UserResponse,
# )


class BaseAnimalRequest(BaseRequest):
    animal_id: str


class BaseAnimalResponse(BaseResponse):
    pass


# AnimalRequest = create_model(
#     "AnimalRequest",
#     __base__=__AnimalRequest,
# )

# AnimalResponse = create_model(
#     "AnimalResponse",
#     __base__=__AnimalResponse,
# )
