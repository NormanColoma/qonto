from datetime import datetime

import pytest

from domain.account.account import Account
from domain.account.amount.amount import Amount
from domain.account.bic.bic import Bic
from domain.account.iban.iban import Iban
from domain.account.insufficient_funds_error import InsufficientFundsError
from domain.account.invalid_account_error import InvalidAccountError
from domain.account.invalid_transfer_operation_error import InvalidTransferOperationError
from domain.account.transfer_done_event import TransferDoneEvent

id = 1
created_at = datetime.now()
iban = 'ES9121000418450200051332'
bic = 'CCOPFRPPXXX'
another_bic = 'CCOPFRPP256'
another_iban = 'ES9121000418450200051333'


def test_should_raise_error_when_iban_error():
    with pytest.raises(InvalidAccountError) as e:
        Account.build(id, iban=None, bic=None, organization_name=None, balance_cents=None, created_at=created_at)
    assert e.value.message == 'Field iban cannot be empty'


def test_should_raise_error_when_bic_error():
    with pytest.raises(InvalidAccountError) as e:
        Account.build(id, iban=iban, bic=None, organization_name=None, balance_cents=None, created_at=created_at)
    assert e.value.message == 'Field bic cannot be empty'


def test_should_raise_error_when_invalid_amount_error():
    with pytest.raises(InvalidAccountError) as e:
        Account.build(id, iban=iban, bic=bic, organization_name='name', balance_cents=None, created_at=created_at)
    assert e.value.message == 'Field balance_cents cannot be empty'


def test_should_raise_error_when_organization_name_missing_provided():
    with pytest.raises(InvalidAccountError) as e:
        Account.build(id, iban=iban, bic=bic, organization_name=None, balance_cents=100.00, created_at=created_at)
    assert e.value.message == 'Field organization_name cannot be empty'


def test_should_raise_error_when_invalid_organization_name():
    with pytest.raises(InvalidAccountError) as e:
        Account.build(id, iban=iban, bic=bic, organization_name=2, balance_cents=100, created_at=created_at)
    assert e.value.message == 'Field organization_name must be a valid string'


def test_should_build_account_correctly():
    account = Account.build(id, iban=iban, bic=bic, organization_name='name', balance_cents=100,
                            created_at=created_at)

    assert account == Account.build(id, iban=iban, bic=bic, organization_name='name', balance_cents=100,
                                    created_at=created_at)


def test_should_raise_error_when_insufficient_funds():
    with pytest.raises(InsufficientFundsError) as e:
        account = Account.build(id, iban=another_iban, bic=another_bic, organization_name='name', created_at=created_at)
        account.do_transfer(counterparty_name='name', counterparty_iban=Iban(iban),
                            counterparty_bic=Bic(bic), amount=Amount(10), description='description')

    assert e.value.message == 'There are no sufficient funds for doing the transfer'


def test_should_raise_error_when_doing_transfer_to_same_account():
    with pytest.raises(InvalidTransferOperationError) as e:
        account = Account.build(id, iban=iban, bic=bic, organization_name='name', balance_cents=20,
                                created_at=created_at)
        account.do_transfer(counterparty_name='name', counterparty_iban=Iban(iban),
                            counterparty_bic=Bic(bic), amount=Amount(10), description='description')

    assert e.value.message == 'Cannot perform transfer to the same account'


def test_should_do_transfer_and_add_event():
    account = Account.build(id, iban=iban, bic=bic, organization_name='name', balance_cents=20,
                            created_at=created_at)
    account.do_transfer(counterparty_name='name', counterparty_iban=Iban(another_iban),
                        counterparty_bic=Bic(another_bic), amount=Amount(10), description='description')

    assert account.balance_cents.value == 10
    events = account.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], TransferDoneEvent)
    transfer_done_event = events[0].to_dict()
    assert transfer_done_event['data']['transfer']['account_id'] == id
    assert transfer_done_event['data']['transfer']['counterparty_name'] == 'name'
    assert transfer_done_event['data']['transfer']['counterparty_iban'] == another_iban
    assert transfer_done_event['data']['transfer']['counterparty_bic'] == another_bic
    assert transfer_done_event['data']['transfer']['amount_cents'] == 10
    assert transfer_done_event['data']['transfer']['description'] == 'description'


def test_to_dict():
    account = Account.build(id, iban=iban, bic=bic, organization_name='name', balance_cents=20,
                            created_at=created_at)

    expected_dict = {
        'id': id,
        'iban': iban,
        'bic': bic,
        'balance_cents': 20,
        'organization_name': 'name',
        'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

    assert account.to_dict() == expected_dict
