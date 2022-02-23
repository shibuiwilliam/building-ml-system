import json

from src.entities.animal import AnimalQuery
from src.entities.violation_type import ViolationTypeQuery
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository

logger = configure_logger(__name__)


class ViolationDetectionJob(object):
    def __init__(
        self,
        messaging: RabbitmqMessaging,
        animal_repository: AbstractAnimalRepository,
        violation_type_repository: AbstractViolationTypeRepository,
    ):
        self.messaging = messaging
        self.animal_repository = animal_repository
        self.violation_type_repository = violation_type_repository

        _v = self.violation_type_repository.select(query=ViolationTypeQuery(name="no_animal_violation"))
        self.violation_type_id = _v[0].id

    def detect_violation(self):
        pass

    def run(
        self,
        consuming_queue: str,
        registration_queue: str,
    ):
        def callback(ch, method, properties, body):
            data = json.loads(body)
            logger.info(f"consumed data: {data}")
            animal = self.animal_repository.select(
                query=AnimalQuery(id=data["id"]),
                limit=1,
                offset=0,
            )
            if len(animal) > 0:
                # TODO: fix to actually predict by no animal violation ml serving
                self.messaging.publish(
                    queue_name=registration_queue,
                    body={
                        "animal_id": animal[0].id,
                        "violation_type_id": self.violation_type_id,
                        "probability": 0.95,
                        "judge": "administrator",
                        "is_effective": True,
                    },
                )
            ch.basic_ack(delivery_tag=method.delivery_tag)

        try:
            self.messaging.init_channel()
            self.messaging.channel.queue_declare(
                queue=consuming_queue,
                durable=True,
            )
            self.messaging.channel.queue_declare(
                queue=registration_queue,
                durable=True,
            )
            self.messaging.channel.basic_qos(prefetch_count=1)
            self.messaging.channel.basic_consume(
                queue=consuming_queue,
                on_message_callback=callback,
            )
            logger.info(f"Waiting for {consuming_queue} queue...")
            self.messaging.channel.start_consuming()

        except Exception as e:
            logger.exception(e)
            raise e
        finally:
            self.messaging.close()
