import json
from typing import Dict, Optional
import httpx
from io import BytesIO
from PIL import Image
from src.entities.animal import AnimalQuery, AnimalModel
from src.entities.violation_type import ViolationTypeQuery
from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.middleware.logger import configure_logger
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.violation_type_repository import AbstractViolationTypeRepository
from src.configurations import Configurations

logger = configure_logger(__name__)


class ViolationDetectionJob(object):
    def __init__(
        self,
        messaging: RabbitmqMessaging,
        animal_repository: AbstractAnimalRepository,
        violation_type_repository: AbstractViolationTypeRepository,
        timeout: float = 10.0,
        retries: int = 3,
    ):
        self.messaging = messaging
        self.animal_repository = animal_repository
        self.violation_type_repository = violation_type_repository

        _v = self.violation_type_repository.select(query=ViolationTypeQuery(name="no_animal_violation"))
        self.violation_type_id = _v[0].id
        self.timeout = timeout
        self.transport = httpx.HTTPTransport(
            retries=retries,
        )

    def detect_violation(
        self,
        animal: AnimalModel,
    ) -> Optional[Dict]:
        with httpx.Client(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            res = client.get(animal.photo_url)
        if res.status_code != 200:
            logger.error(f"failed to download {animal.id} {animal.photo_url}")
            return None
        img = Image.open(BytesIO(res.content))
        if img.mode == "RGBA":
            img_rgb = Image.new("RGB", (img.height, img.width), (255, 255, 255))
            img_rgb.paste(img, mask=img.split()[3])
            img = img_rgb

    def pseudo_detect_violation(
        self,
        animal: AnimalModel,
    ) -> Optional[Dict]:
        return {
            "animal_id": animal.id,
            "violation_type_id": self.violation_type_id,
            "probability": 0.05,
            "judge": "administrator",
            "is_effective": True,
        }

    def run(
        self,
        consuming_queue: str,
        registration_queue: str,
    ):
        def callback(ch, method, properties, body):
            data = json.loads(body)
            logger.info(f"consumed data: {data}")
            animals = self.animal_repository.select(
                query=AnimalQuery(id=data["id"]),
                limit=1,
                offset=0,
            )

            if len(animals) != 1:
                logger.info(f"cannot ack {method.delivery_tag}")

            animal = animals[0]
            if Configurations.pseudo_prediction:
                violation = self.pseudo_detect_violation(animal=animal)
            else:
                violation = self.detect_violation(animal=animal)

            if violation is None:
                logger.info(f"cannot ack {method.delivery_tag}")

            self.messaging.publish(
                queue_name=registration_queue,
                body=violation,
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
