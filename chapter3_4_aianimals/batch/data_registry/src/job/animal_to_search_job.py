from src.configurations import Configurations
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.job.abstract_job import AbstractJob
from src.middleware.logger import configure_logger
from src.usecase.animal_usecase import AbstractAnimalUsecase

logger = configure_logger(__name__)


class AnimalToSearchJob(AbstractJob):
    def __init__(
        self,
        animal_usecase: AbstractAnimalUsecase,
        messaging: RabbitmqMessaging,
    ):
        super().__init__()
        self.animal_usecase = animal_usecase
        self.messaging = messaging

    def run(self):
        logger.info("run animal to search job")
        index_exists = self.animal_usecase.index_exists()
        if not index_exists:
            logger.info("register index")
            self.animal_usecase.create_index()
        try:
            self.messaging.init_channel()
            self.messaging.create_queue(queue_name=Configurations.animal_registry_queue)
            self.messaging.channel.basic_qos(prefetch_count=1)
            self.animal_usecase.register_document_from_queue()
        except Exception as e:
            logger.exception(e)
            raise e
        finally:
            self.messaging.close()
