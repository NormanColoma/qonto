import re

from domain.account.iban.invalid_bic_error import InvalidIbanError

IBAN_PATTERN = "^([A-Z]{2}[ \-]?[0-9]{2})(?=(?:[ \-]?[A-Z0-9]){9,30}$)((?:[ \-]?[A-Z0-9]{3,5}){2,7})([ \-]?[A-Z0-9]{1,3})?$"


class Iban:
    def __init__(self, value: str):
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        if value is None:
            raise InvalidIbanError('cannot be empty')
        if not isinstance(value, str):
            raise InvalidIbanError('must be a valid string')

        iban_pattern = re.compile(IBAN_PATTERN)
        if not iban_pattern.match(value):
            raise InvalidIbanError('must be a valid IBAN bank account')
        self.__value = value

    def __eq__(self, other: 'Iban') -> bool:
        return self.value == other.value
