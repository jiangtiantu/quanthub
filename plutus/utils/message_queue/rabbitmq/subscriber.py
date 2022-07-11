# -- coding: utf-8 --

from typing import Union

from plutus.utils.message_queue.rabbitmq.rabbitmq import RabbitMq


class Subscriber(RabbitMq):
    def __init__(
        self,
        host="localhost",
        port=5672,
        user="guest",
        password="guest",
        exchange_name: str = "",
        queue_name: str = "",
        routing_key: str= "",
    ):
        super().__init__(
            host=host,
            port=port,
            user=user,
            password=password,
        )
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.queue_name = self.create_queue(queue_name=queue_name)
        self.channel.queue_bind(
            queue=self.queue_name,
            exchange=self.exchange_name,
            routing_key=self.routing_key,
        )

    def subscribe(self, func):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=func, auto_ack=True
        )
        self.channel.start_consuming()

    def start(self, func):
        try:
            self.subscribe(func)
        except Exception as e:
            print(e)
            self.start(func)
