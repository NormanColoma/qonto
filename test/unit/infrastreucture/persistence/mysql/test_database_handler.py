from unittest.mock import MagicMock

import pytest

from infraestructure.config.config import Config
from infraestructure.persistence.mysql.database_handler import SqlAlchemyHandler


class FakeConfig(Config):
    MYSQL_URI = 'fake_uri'


config = FakeConfig()
client = MagicMock()


@pytest.fixture
def database_handler():
    handler = SqlAlchemyHandler(config, client)
    client.reset_mock()
    yield handler


def test_should_return_a_new_session(database_handler):
    session = MagicMock()
    client.create_engine.return_value = {}
    client.orm.Session.return_value = session

    with database_handler.get_connection() as conn:
        assert conn == session

    client.create_engine.assert_called_once_with('fake_uri', isolation_level='READ COMMITTED')
    client.orm.Session.assert_called_once_with({})
    session.commit.assert_called_once()
