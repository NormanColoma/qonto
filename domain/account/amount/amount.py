import re

from domain.account.amount.invalid_amount_error import InvalidAmountError
CENT_EUROS_PATTERN = "^[0-9]*\.?([0-9]{0,2})?$"

class Amount:
    def __init__(self, value: int | str):
        self.value = value

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        if value is None:
            raise InvalidAmountError('cannot be empty')
        elif isinstance(value, str):
            self.__value = self.parse_amount(value)
        elif isinstance(value, int):
            if value < 0:
                raise InvalidAmountError('must be a positive integer')
            self.__value = value
        else:
            raise InvalidAmountError('must be a valid string or integer type')

    def parse_amount(self, amount: str) -> int:
        pattern = re.compile(CENT_EUROS_PATTERN)
        if not pattern.match(amount):
            raise InvalidAmountError('must be a positive valid numeric string with almost two decimal places')

        number = amount.split('.')
        if len(number) == 2:
            whole, decimal = number
            return int(whole) * 100 + int(decimal)
        return int(number[0]) * 100

    def __eq__(self, other: 'Amount') -> bool:
        return self.value == other.value
