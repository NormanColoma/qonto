import pytest

from domain.account.iban.iban import Iban
from domain.account.iban.invalid_bic_error import InvalidIbanError

iban = 'ES9121000418450200051332'
another_iban = 'FR10474608000002006107XXXXX'


def test_should_raise_error_when_iban_missing():
    with pytest.raises(InvalidIbanError) as e:
        Iban(None)
    assert e.value.message == 'cannot be empty'


def test_should_raise_error_when_invalid_iban_is_not_str():
    with pytest.raises(InvalidIbanError) as e:
        Iban(12)
    assert e.value.message == 'must be a valid string'


def test_should_raise_error_when_invalid_iban_provided():
    with pytest.raises(InvalidIbanError) as e:
        invalid_iban = 'invalid'
        Iban(invalid_iban)
    assert e.value.message == 'must be a valid IBAN bank account'


def test_should_build_iban_correctly():
    assert Iban(iban).value == iban
    assert Iban(another_iban).value == another_iban
