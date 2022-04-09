import logging
import os

import pika


class RabbitmqMessaging(object):
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

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

    def init_channel(self):
        self.connection = pika.BlockingConnection(self.__params)
        self.channel = self.connection.channel()

    def close(self):
        self.channel.close()
        self.connection.close()
