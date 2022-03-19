from src.configurations import Configurations
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.job.abstract_job import AbstractJob
from src.middleware.logger import configure_logger
from src.usecase.animal_feature_usecase import AbstractAnimalFeatureUsecase

logger = configure_logger(__name__)


class AnimalFeatureRegistrationJob(AbstractJob):
    def __init__(
        self,
        animal_feature_usecase: AbstractAnimalFeatureUsecase,
        messaging: RabbitmqMessaging,
    ):
        super().__init__()
        self.animal_feature_usecase = animal_feature_usecase
        self.messaging = messaging

    def run(self):
        logger.info("run animal feature registration job")
        try:
            self.messaging.init_channel()
            self.messaging.create_queue(queue_name=Configurations.animal_feature_registry_queue)
            self.messaging.channel.basic_qos(prefetch_count=1)
            self.animal_feature_usecase.register_animal_feature()
        except Exception as e:
            logger.exception(e)
            raise e
        finally:
            self.messaging.close()
