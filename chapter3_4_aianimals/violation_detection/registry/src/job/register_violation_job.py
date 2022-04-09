import json
import logging

from src.infrastructure.messaging import RabbitmqMessaging
from src.request_object.violation import ViolationCreateRequest
from src.usecase.violation_usecase import AbstractViolationUsecase


class RegisterViolationJob(object):
    def __init__(
        self,
        violation_usecase: AbstractViolationUsecase,
        messaging: RabbitmqMessaging,
    ):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.violation_usecase = violation_usecase
        self.messaging = messaging

    def run(
        self,
        queue_name: str,
    ):
        def callback(ch, method, properties, body):
            data = json.loads(body)
            self.logger.info(f"consumed data: {data}")
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
            self.logger.info(f"Waiting for {queue_name} queue...")
            self.messaging.channel.start_consuming()
        except Exception as e:
            self.logger.exception(e)
            raise e
        finally:
            self.messaging.close()
