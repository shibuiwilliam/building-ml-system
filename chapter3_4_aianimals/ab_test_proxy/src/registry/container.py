from logging import getLogger
from typing import Any, Dict, List, Optional, Tuple, Union

import yaml
from pydantic import BaseModel, create_model
from src.configurations import Configurations
from src.constants import RUN_ENVIRONMENT
from src.schema.base_schema import (
    BaseAnimalRequest,
    BaseAnimalResponse,
    BaseRandomABTestRequest,
    BaseRandomABTestResponse,
    BaseUserRequest,
    BaseUserResponse,
)
from src.service.ab_test_service import ABTestType, Endpoint
from src.service.animal_ab_test_service import AbstractAnimalTestService, AnimalIDs, AnimalTestService
from src.service.random_ab_test_service import (
    AbstractRandomABTestService,
    DistributionRate,
    RandomABTestService,
    RandomDistribution,
)
from src.service.user_ab_test_service import AbstractUserTestService, UserIDs, UserTestService

logger = getLogger(__name__)


class ABTestConfiguration(BaseModel):
    ab_test_type: ABTestType
    endpoint_a: Endpoint
    endpoint_b: Endpoint
    request: Dict[str, Tuple[type, Any]]
    response: Dict[str, Tuple[type, Any]]


class Container(object):
    def __init__(
        self,
        ab_test_configuration_path: str,
    ):
        self.ab_test_configuration_path = ab_test_configuration_path
        self.load_configuration()

    def load_configuration(self):
        with open(self.ab_test_configuration_path, "r") as f:
            d = yaml.safe_load(f)
        ab_test_type = ABTestType.value_to_key(value=d["ab_test_type"])
        self.ab_test_configuration = ABTestConfiguration(
            ab_test_type=ab_test_type,
        )

    def create_random_ab_test_request(self):
        self.RandomABTestRequest = create_model(
            "RandomABTestRequest",
            __base__=BaseRandomABTestRequest,
            **self.ab_test_configuration.request,
        )

    def create_random_ab_test_responset(self):
        self.RandomABTestResponse = create_model(
            "RandomABTestResponse",
            __base__=BaseRandomABTestResponse,
            **self.ab_test_configuration.response,
        )

    def create_user_request(self):
        self.UserRequest = create_model(
            "UserRequest",
            __base__=BaseUserRequest,
            **self.ab_test_configuration.request,
        )

    def create_user_responset(self):
        self.UserResponse = create_model(
            "UserResponse",
            __base__=BaseUserResponse,
            **self.ab_test_configuration.response,
        )

    def create_animal_request(self):
        self.AnimalRequest = create_model(
            "AnimalRequest",
            __base__=BaseAnimalRequest,
            **self.ab_test_configuration.request,
        )

    def create_animal_responset(self):
        self.AnimalResponse = create_model(
            "AnimalResponse",
            __base__=BaseAnimalResponse,
            **self.ab_test_configuration.response,
        )


container = Container(ab_test_configuration_path=Configurations.ab_test_configuration)
