import json
from unittest.mock import MagicMock

import pytest

from domain.common.bus.event.domain_event import DomainEvent
from infraestructure.bus.event.rabbitmq_event_bus import RabbitMqEventBus

rabbit_handler = MagicMock()


@pytest.fixture
def rabbit_event_bus():
    bus = RabbitMqEventBus(rabbit_handler)
    rabbit_handler.reset_mock()
    yield bus


def test_should_publish_events(rabbit_event_bus):
    class FakeDomainEvent(DomainEvent):
        def __init__(self):
            self.topic = 'topic'
            self.name = 'routing.key'

        def to_dict(self):
            return {
                'field': 2
            }
    channel = MagicMock()
    rabbit_handler.get_channel.return_value = channel

    fake_event = FakeDomainEvent()

    rabbit_event_bus.publish([fake_event])

    rabbit_handler.get_channel.assert_called_once()
    channel.exchange_declare.assert_called_once_with(exchange='topic', durable=True)
    channel.basic_publish.assert_called_once_with(exchange='topic', routing_key='routing.key',
                                                  body=json.dumps(fake_event.to_dict()))

