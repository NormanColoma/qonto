import pika

from infraestructure.config.config import Config


class RabbitMQHandler:
    def __init__(self, config: Config, rabbit_client):
        self.__channel = None
        self.__config = config
        self.__client = rabbit_client

    def __connectAndCreateChannel(self):
        connection = self.__client.BlockingConnection(self.__client.URLParameters(self.__config.RABBITMQ_URI))
        self.__channel = connection.channel()

    def getChannel(self):
        if self.__channel is None:
            self.__connectAndCreateChannel()
        return self.__channel
