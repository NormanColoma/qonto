from datetime import datetime

import pytest

from domain.account.transfer.invalid_transfer_error import InvalidTransferError
from domain.account.transfer.transfer import Transfer

id = 1
account_id = 1
created_at = datetime.now()
iban = 'ES9121000418450200051332'
bic = 'CCOPFRPPXXX'
another_bic = 'CCOPFRPP256'
another_iban = 'ES9121000418450200051333'
amount_cents = 10.00


def test_should_raise_error_when_account_id_missing():
    with pytest.raises(InvalidTransferError) as e:
        Transfer.build(id, account_id=None, counterparty_name=None, counterparty_bic=None, counterparty_iban=None,
                       description=None, amount_cents=0.00, created_at=created_at)
    assert e.value.message == 'Field account_id cannot be empty'


def test_should_raise_error_when_account_id_is_not_integer():
    with pytest.raises(InvalidTransferError) as e:
        Transfer.build(id, account_id='not-int', counterparty_name=None, counterparty_bic=None, counterparty_iban=None,
                       description=None, amount_cents=0.00, created_at=created_at)
    assert e.value.message == 'Field account_id must be a valid integer type'


def test_should_raise_error_when_counterparty_iban_missing():
    with pytest.raises(InvalidTransferError) as e:
        Transfer.build(id, account_id=account_id, counterparty_name='name', counterparty_bic=bic,
                       counterparty_iban=None,
                       description='desc', amount_cents=0.00, created_at=created_at)
    assert e.value.message == 'Field counterparty_iban cannot be empty'


def test_should_raise_error_when_counterparty_bic_missing():
    with pytest.raises(InvalidTransferError) as e:
        Transfer.build(id, account_id=account_id, counterparty_name='name', counterparty_bic=None,
                       counterparty_iban=iban,
                       description='desc', amount_cents=0.00, created_at=created_at)
    assert e.value.message == 'Field counterparty_bic cannot be empty'


def test_should_raise_error_when_counterparty_name_missing():
    with pytest.raises(InvalidTransferError) as e:
        Transfer.build(id, account_id=account_id, counterparty_name=None, counterparty_bic=bic,
                       counterparty_iban=iban,
                       description='desc', amount_cents=0.00, created_at=created_at)
    assert e.value.message == 'Field counterparty_name cannot be empty'


def test_should_raise_error_when_amount_cents_missing():
    with pytest.raises(InvalidTransferError) as e:
        Transfer.build(id, account_id=account_id, counterparty_name='name', counterparty_bic=bic,
                       counterparty_iban=iban,
                       description='desc', amount_cents=None, created_at=created_at)
    assert e.value.message == 'Field amount_cents cannot be empty'


def test_should_raise_error_when_amount_cents_is_not_float():
    with pytest.raises(InvalidTransferError) as e:
        Transfer.build(id, account_id=account_id, counterparty_name='name', counterparty_bic=bic,
                       counterparty_iban=iban,
                       description='desc', amount_cents=1, created_at=created_at)
    assert e.value.message == 'Field amount_cents must be a valid float number'


def test_should_raise_error_when_description_missing():
    with pytest.raises(InvalidTransferError) as e:
        Transfer.build(id, account_id=account_id, counterparty_name='name', counterparty_bic=bic,
                       counterparty_iban=iban,
                       description=None, amount_cents=1.00, created_at=created_at)
    assert e.value.message == 'Field description cannot be empty'


def test_should_raise_error_when_description_is_not_string():
    with pytest.raises(InvalidTransferError) as e:
        Transfer.build(id, account_id=account_id, counterparty_name='name', counterparty_bic=bic,
                       counterparty_iban=iban,
                       description=1, amount_cents=1.00, created_at=created_at)
    assert e.value.message == 'Field description must be a valid string'


def test_should_build_transfer():
    transfer = Transfer.build(id, account_id=account_id, counterparty_name='name', counterparty_bic=bic,
                              counterparty_iban=iban,
                              description='desc', amount_cents=amount_cents, created_at=created_at)
    expected_transfer = Transfer.build(id, account_id=account_id, counterparty_name='name', counterparty_bic=bic,
                                       counterparty_iban=iban,
                                       description='desc', amount_cents=amount_cents, created_at=created_at)

    assert transfer == expected_transfer


def test_to_dict():
    transfer = Transfer.build(id, account_id=account_id, counterparty_name='name', counterparty_bic=bic,
                              counterparty_iban=iban,
                              description='desc', amount_cents=amount_cents, created_at=created_at)

    expected_dict = {
        'id': id,
        'account_id': account_id,
        'counterparty_iban': iban,
        'counterparty_bic': bic,
        'counterparty_name': 'name',
        'amount_cents': amount_cents,
        'description': 'desc',
        'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

    assert transfer.to_dict() == expected_dict
