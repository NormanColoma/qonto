from datetime import datetime

import pytest

from domain.account.account import Account
from infraestructure.persistence.mysql.mysql_account_parser import MySqlAccountParser, AccountRow

created_at = datetime.now()
iban = 'ES9121000418450200051332'
bic = 'CCOPFRPPXXX'
id = 1
balance = 20
name = 'name'


@pytest.fixture
def parser():
    parser = MySqlAccountParser()
    yield parser


def test_should_parse_domain_to_database(parser):
    account = Account.build(id, iban=iban, bic=bic, organization_name=name, balance_cents=balance,
                            created_at=created_at)

    account_row = parser.to_database(account)

    expected_database_row = AccountRow()
    expected_database_row.id = id
    expected_database_row.iban = iban
    expected_database_row.bic = bic
    expected_database_row.organization_name = name
    expected_database_row.balance_cents = balance
    expected_database_row.created_at = created_at

    assert account_row.toDict() == expected_database_row.toDict()


def test_should_parse_database_to_domain(parser):
    database_row = AccountRow()
    database_row.id = id
    database_row.iban = iban
    database_row.bic = bic
    database_row.organization_name = name
    database_row.balance_cents = balance
    database_row.created_at = created_at

    account = parser.to_domain(database_row)

    expected_account = Account.build(id, iban=iban, bic=bic, organization_name=name, balance_cents=balance,
                                     created_at=created_at)

    assert account == expected_account


def test_should_return_none_if_row_is_none(parser):
    assert parser.to_domain(None) is None
