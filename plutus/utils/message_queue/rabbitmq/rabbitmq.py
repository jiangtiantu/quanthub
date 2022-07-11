# -- coding: utf-8 --
import pika


class RabbitMq:
    def __init__(
        self,
        host="localhost",
        port=5672,
        user="guest",
        password="guest",
        channel_number=1,
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.channel_number = channel_number
        credentials = pika.PlainCredentials(
            self.user, self.password, erase_on_connect=True
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials,
                heartbeat_interval=0,
                socket_timeout=5,
            )
        )

        self.channel = self.connection.channel(channel_number=self.channel_number)

    def create_exchange(self, exchange_name: str = "", exchange_type: str = "direct"):
        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type,
            passive=False,
            durable=False,
            auto_delete=False,
        )

    def create_queue(self, queue_name: str = ""):
        result = self.channel.queue_declare(
            queue=queue_name, auto_delete=True, exclusive=True
        )

        return result.method.queue

    def close(self):
        self.connection.close()

    def reconnect(self):
        try:
            self.connection.close()
        except:
            pass
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                heartbeat_interval=0,
                socket_timeout=5,
            )
        )
        self.channel = self.connection.channel(channel_number=self.channel_number)
        return self
