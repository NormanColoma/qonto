import json

from domain.common.bus.event.domain_event import DomainEvent
from domain.common.bus.event.event_bus import EventBus
from infraestructure.bus.event.rabbit_handler import RabbitMQHandler


class RabbitMqEventBus(EventBus):
    def __init__(self, rabbit_handler: RabbitMQHandler):
        self.__handler = rabbit_handler

    def publish(self, events: [DomainEvent]) -> None:
        channel = self.__handler.get_channel()
        print('publishing domain events...')
        for event in events:
            channel.exchange_declare(exchange=event.topic, durable=True)
            channel.basic_publish(exchange=event.topic, routing_key=event.name,
                                  body=json.dumps(event.to_dict()))
