import pytest

from domain.account.bic.bic import Bic
from domain.account.bic.invalid_bic_error import InvalidBicError

bic = 'CCOPFRPPXXX'
another_bic = 'CRLYFRPPTOU'


def test_should_raise_error_when__bic_missing():
    with pytest.raises(InvalidBicError) as e:
        Bic(None)
    assert e.value.message == 'cannot be empty'


def test_should_raise_error_when__bic_is_not_str():
    with pytest.raises(InvalidBicError) as e:
        Bic(12)
    assert e.value.message == 'must be a valid string'


def test_should_raise_error_when_invalid_bic_provided():
    with pytest.raises(InvalidBicError) as e:
        invalid_bic = 'invalid'
        Bic(invalid_bic)
    assert e.value.message == 'must be a valid BIC bank code'


def test_should_build_iban_correctly():
    b1 = Bic(bic)
    b2 = Bic(bic)
    assert b1 == b2
