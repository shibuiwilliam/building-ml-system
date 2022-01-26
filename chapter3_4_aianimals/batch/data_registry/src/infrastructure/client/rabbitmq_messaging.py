import json
import os
from logging import getLogger
from typing import Dict

import pika

logger = getLogger(__name__)


class RabbitmqMessaging(object):
    def __init__(self):
        super().__init__()
        self.__rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        self.__rebbitmq_user = os.environ["RABBITMQ_USER"]
        self.__rabbitmq_password = os.environ["RABBITMQ_PASSWORD"]

        self.__rabbitmq_credential = pika.PlainCredentials(
            self.__rebbitmq_user,
            self.__rabbitmq_password,
        )
        self.__params = pika.ConnectionParameters(
            self.__rabbitmq_host,
            credentials=self.__rabbitmq_credential,
        )
        self.properties = pika.BasicProperties(content_type="application/json")

    def init_channel(self):
        self.connection = pika.BlockingConnection(self.__params)
        self.channel = self.connection.channel()

    def create_queue(
        self,
        queue_name: str,
    ):
        self.channel.queue_declare(
            queue=queue_name,
            durable=True,
        )

    def close(self):
        self.channel.close()
        self.connection.close()

    def publish(
        self,
        queue_name: str,
        body: Dict,
    ):
        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(body),
            properties=self.properties,
        )
