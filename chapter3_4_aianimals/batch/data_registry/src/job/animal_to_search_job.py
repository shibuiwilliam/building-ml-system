from time import sleep

from src.configurations import Configurations
from src.infrastructure.messaging import RabbitmqMessaging
from src.job.abstract_job import AbstractJob
from src.usecase.animal_usecase import AbstractAnimalUsecase


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
        self.logger.info("run animal to search job")
        ready = False
        while not ready:
            self.logger.info("waiting for search to be ready")
            ready = self.animal_usecase.ping_search()
            sleep(1)
        index_exists = self.animal_usecase.index_exists()
        while not index_exists:
            self.logger.info("waiting for index registration ready")
            try:
                self.animal_usecase.create_index()
            except:
                self.logger.error("failed index registration")
            finally:
                index_exists = self.animal_usecase.index_exists()
            sleep(1)
        try:
            self.messaging.init_channel()
            self.messaging.create_queue(queue_name=Configurations.animal_registry_queue)
            self.messaging.channel.basic_qos(prefetch_count=1)
            self.animal_usecase.register_document_from_queue()
        except Exception as e:
            self.logger.exception(e)
            raise e
        finally:
            self.messaging.close()
