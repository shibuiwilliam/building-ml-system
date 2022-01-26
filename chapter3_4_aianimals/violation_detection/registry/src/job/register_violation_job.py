import json

from src.infrastructure.client.rabbitmq_messaging import RabbitmqMessaging
from src.middleware.logger import configure_logger
from src.request_object.violation import ViolationCreateRequest
from src.usecase.violation_usecase import AbstractViolationUsecase

logger = configure_logger(__name__)


class RegisterViolationJob(object):
    def __init__(
        self,
        violation_usecase: AbstractViolationUsecase,
        messaging: RabbitmqMessaging,
    ):
        self.violation_usecase = violation_usecase
        self.messaging = messaging

    def run(
        self,
        queue_name: str,
    ):
        def callback(ch, method, properties, body):
            data = json.loads(body)
            logger.info(f"consumed data: {data}")
            violation = ViolationCreateRequest(**data)
            self.violation_usecase.register(request=violation)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        try:
            self.messaging.init_channel()
            self.messaging.channel.queue_declare(
                queue=queue_name,
                durable=True,
            )
            self.messaging.channel.basic_qos(prefetch_count=1)
            self.messaging.channel.basic_consume(
                queue=queue_name,
                on_message_callback=callback,
            )
            logger.info(f"Waiting for {queue_name} queue...")
            self.messaging.channel.start_consuming()
        except Exception as e:
            logger.exception(e)
            raise e
        finally:
            self.messaging.close()
