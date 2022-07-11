# -- coding: utf-8 --
from typing import Union

import pika

from plutus.utils.message_queue.rabbitmq.rabbitmq import RabbitMq


class Publisher(RabbitMq):
    def __init__(
        self,
        host="localhost",
        port=5672,
        user="guest",
        password="guest",
        channel_number=1,
        queue_name="",
        exchange_name="",
        exchange_type="fanout",
        routing_key: str = "",
    ):
        super().__init__(
            host,
            port,
            user,
            password,
            channel_number,
        )

        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        self.queue_name = self.create_queue(queue_name=queue_name)

        self.create_exchange(
            exchange_name=self.exchange_name,
            exchange_type=self.exchange_type,
        )

    def pub(self, text):

        if isinstance(text, bytes):
            content_type = "text/plain"
        elif isinstance(text, str):
            content_type = "text/plain"
        elif isinstance(text, dict):
            content_type = "application/json"
        else:
            print("请再次确认数据类型")
        try:
            self.channel.basic_publish(
                exchange=self.exchange_name,
                body=text,
                routing_key=self.routing_key,
                properties=pika.BasicProperties(
                    content_type=content_type, delivery_mode=1
                ),
            )

        except Exception as e:
            print(e)
            self.reconnect().channel.basic_publish(
                exchange=self.exchange_name,
                body=text,
                routing_key=self.routing_key,
                properties=pika.BasicProperties(
                    content_type=content_type, delivery_mode=1
                ),
            )
