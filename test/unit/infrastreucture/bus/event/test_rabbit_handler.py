from unittest.mock import MagicMock

import pytest

from infraestructure.bus.event.rabbit_handler import RabbitMQHandler

config = MagicMock()
rabbit_client = MagicMock()


@pytest.fixture
def rabbit_handler():
    handler = RabbitMQHandler(config, rabbit_client)
    config.reset_mock()
    rabbit_client.reset_mock()
    yield handler


def test_should_connect(rabbit_handler):
    connection = MagicMock()
    connection.channel.return_value = {}
    rabbit_client.BlockingConnection.return_value = connection

    channel = rabbit_handler.get_channel()

    rabbit_client.BlockingConnection.assert_called_once()
    connection.channel.assert_called_once()
    assert channel == {}


def test_should_return_connection_if_exists(rabbit_handler):
    rabbit_handler.get_channel()
    rabbit_handler.get_channel()
    rabbit_client.BlockingConnection.assert_called_once()
