from ..interfaces.handler import MqHandler
import pika


class RabbitMQHandler(MqHandler):
    def __init__(self, host=None, exchange=None, exchange_type=None, username=None, password=None, port=5672, vault_secret_name=None):
        self.host = host
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        if self.username is None and self.password is None:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(self.host))
        else:
            self.connection = pika.BlockingConnection(pika.URLParameters(
                "amqp://{username}:{password}@{host}:{port}/%2F".format(
                    username=self.username, password=self.password, host=self.host, port=self.port)))

        if self.connection is not None:
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange=self.exchange, exchange_type=self.exchange_type)

    def publish_results(self, jsonResults, exchange=None):
        if exchange is None:
            exchange = self.exchange
        self.channel.basic_publish(
            exchange=exchange, routing_key='', body=jsonResults)

    def close_connection(self):
        self.connection.close()
