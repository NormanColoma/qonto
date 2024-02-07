from domain.account.amount.invalid_amount_error import InvalidAmountError


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
            self.__value = value
        else:
            raise InvalidAmountError('must be a valid string or integer type')

    def parse_amount(self, amount: str) -> int:
        whole_and_decimal = amount.split('.')
        if len(whole_and_decimal) == 2:
            return int(whole_and_decimal[0]) * 100 + int(whole_and_decimal[1])
        return int(whole_and_decimal[0]) * 100

    def __eq__(self, other: 'Amount') -> bool:
        return self.value == other.value
