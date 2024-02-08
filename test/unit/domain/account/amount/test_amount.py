import pytest

from domain.account.amount.amount import Amount
from domain.account.amount.invalid_amount_error import InvalidAmountError


def test_should_raise_error_when_amount_missing():
    with pytest.raises(InvalidAmountError) as e:
        Amount(None)
    assert e.value.message == 'cannot be empty'


def test_should_raise_error_when_amount_is_negative():
    with pytest.raises(InvalidAmountError) as e:
        Amount(-1)
    assert e.value.message == 'must be a positive integer'


def test_should_raise_error_when_amount_is_neither_str_nor_int():
    with pytest.raises(InvalidAmountError) as e:
        Amount(12.00)
    assert e.value.message == 'must be a valid string or integer type'


def test_should_raise_error_when_amount_is_not_valid_numeric_str():
    with pytest.raises(InvalidAmountError) as e:
        Amount("12.345")
    assert e.value.message == 'must be a positive valid numeric string with almost two decimal places'


def test_should_build_iban_correctly():
    a1 = Amount("12.50")
    assert a1.value == 1250
    a2 = Amount("10")
    assert a2.value == 1000
    a3 = Amount(100)
    assert a3.value == 100
