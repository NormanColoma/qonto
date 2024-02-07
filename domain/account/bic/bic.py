import re

from domain.account.bic.invalid_bic_error import InvalidBicError

BIC_PATTERN = "[A-Z]{6,6}[A-Z2-9][A-NP-Z0-9]([A-Z0-9]{3,3}){0,1}"


class Bic:
    def __init__(self, value: str):
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        if value is None:
            raise InvalidBicError('cannot be empty')
        if not isinstance(value, str):
            raise InvalidBicError('must be a valid string')

        iban_pattern = re.compile(BIC_PATTERN)
        if not iban_pattern.match(value):
            raise InvalidBicError('must be a valid BIC bank code')
        self.__value = value

    def __eq__(self, other: 'Bic') -> bool:
        return self.value == other.value
