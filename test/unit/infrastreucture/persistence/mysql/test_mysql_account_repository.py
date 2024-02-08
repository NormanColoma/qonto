from unittest.mock import MagicMock

import pytest

from domain.account.iban.iban import Iban
from infraestructure.persistence.mysql.mysql_account_parser import AccountRow
from infraestructure.persistence.mysql.mysql_account_repository import MysqlAccountRepository

database_handler = MagicMock()
account_parser = MagicMock()


@pytest.fixture
def repository():
    repository = MysqlAccountRepository(database_handler, account_parser)
    database_handler.reset_mock()
    account_parser.reset_mock()
    yield repository


def test_should_find_account(repository):
    where = MagicMock()
    conn = MagicMock()
    conn.query.return_value = where
    database_handler.get_connection.return_value = conn
    account_parser.to_domain.return_value = {}

    iban = Iban('ES9121000418450200051332')
    result = repository.find(iban)

    assert result == {}
    database_handler.get_connection.assert_called_once()
    conn.query.assert_called_once_with(AccountRow)
