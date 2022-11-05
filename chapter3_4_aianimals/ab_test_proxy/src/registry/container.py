from logging import getLogger
from typing import Optional

import yaml
from pydantic import BaseModel
from src.configurations import Configurations
from src.service.ab_test_service import AbstractTestService, ABTestType
from src.service.animal_ab_test_service import AnimalIDs, AnimalTestService
from src.service.random_ab_test_service import RandomABTestService, RandomDistribution
from src.service.user_ab_test_service import UserIDs, UserTestService

logger = getLogger(__name__)


class ABTestConfiguration(BaseModel):
    ab_test_type: ABTestType
    random_ab_test_random_distribution: Optional[RandomDistribution] = None
    user_ab_test_user_ids: Optional[UserIDs] = None
    animal_ab_test_animal_ids: Optional[AnimalIDs] = None
    timeout: float = 10.0
    retries: int = 2


class Container(object):
    def __init__(
        self,
        ab_test_configuration_path: str,
    ):
        self.ab_test_configuration_path: str = ab_test_configuration_path
        self.ab_test_configuration: Optional[ABTestConfiguration] = None
        self.test_service: Optional[AbstractTestService] = None
        self.load_configuration()
        self.initialize_test_service()

    def load_configuration(self):
        with open(self.ab_test_configuration_path, "r") as f:
            d = yaml.safe_load(f)

        _random_ab_test_random_distribution = d.get("random_ab_test_random_distribution", None)
        _user_ab_test_user_ids = d.get("user_ab_test_user_ids", None)
        _animal_ab_test_animal_ids = d.get("animal_ab_test_animal_ids", None)

        random_ab_test_random_distribution = (
            RandomDistribution(**_random_ab_test_random_distribution)
            if _random_ab_test_random_distribution is not None
            else None
        )
        user_ab_test_user_ids = UserIDs(**_user_ab_test_user_ids) if _user_ab_test_user_ids is not None else None
        animal_ab_test_animal_ids = (
            AnimalIDs(**_animal_ab_test_animal_ids) if _animal_ab_test_animal_ids is not None else None
        )

        self.ab_test_configuration = ABTestConfiguration(
            ab_test_type=ABTestType.value_to_key(value=d["ab_test_type"]),
            random_ab_test_random_distribution=random_ab_test_random_distribution,
            user_ab_test_user_ids=user_ab_test_user_ids,
            animal_ab_test_animal_ids=animal_ab_test_animal_ids,
            timeout=d.get("timeout", 10.0),
            retries=d.get("retries", 2),
        )
        logger.info(
            f"""
AB TEST CONFIGURATION
{self.ab_test_configuration}"""
        )

    def initialize_test_service(self):
        if self.ab_test_configuration is None:
            raise ValueError
        if self.ab_test_configuration.ab_test_type == ABTestType.RANDOM:
            if self.ab_test_configuration.random_ab_test_random_distribution is None:
                raise ValueError
            self.test_service = RandomABTestService(
                random_distribution=self.ab_test_configuration.random_ab_test_random_distribution,
                timeout=self.ab_test_configuration.timeout,
                retries=self.ab_test_configuration.retries,
            )
            logger.info("Initialized as RANDOM AB TEST")
        elif self.ab_test_configuration.ab_test_type == ABTestType.USER:
            if self.ab_test_configuration.user_ab_test_user_ids is None:
                raise ValueError
            self.test_service = UserTestService(
                user_ab_test_user_ids=self.ab_test_configuration.user_ab_test_user_ids,
                timeout=self.ab_test_configuration.timeout,
                retries=self.ab_test_configuration.retries,
            )
            logger.info("Initialized as USER AB TEST")
        elif self.ab_test_configuration.ab_test_type == ABTestType.ANIMAL:
            if self.ab_test_configuration.animal_ab_test_animal_ids is None:
                raise ValueError
            self.test_service = AnimalTestService(
                animal_ab_test_animal_ids=self.ab_test_configuration.animal_ab_test_animal_ids,
                timeout=self.ab_test_configuration.timeout,
                retries=self.ab_test_configuration.retries,
            )
            logger.info("Initialized as ANIMAL AB TEST")
        else:
            raise ValueError


container = Container(ab_test_configuration_path=Configurations.ab_test_configuration)
