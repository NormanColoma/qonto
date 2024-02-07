from datetime import datetime

from domain.account.amount.amount import Amount
from domain.account.amount.invalid_amount_error import InvalidAmountError
from domain.account.bic.bic import Bic
from domain.account.bic.invalid_bic_error import InvalidBicError
from domain.account.iban.iban import Iban
from domain.account.iban.invalid_bic_error import InvalidIbanError
from domain.account.transfer.invalid_transfer_error import InvalidTransferError
from domain.common.domain_entity import DomainEntity


class Transfer(DomainEntity):
    def __init__(self, id: int, account_id: int, created_at: datetime, amount_cents: int, counterparty_name: str,
                 counterparty_iban: str, counterparty_bic: str, description: str):
        super().__init__(id, created_at)
        self.account_id = account_id
        self.counterparty_iban = counterparty_iban
        self.counterparty_bic = counterparty_bic
        self.amount_cents = amount_cents
        self.counterparty_name = counterparty_name
        self.description = description

    @classmethod
    def build(cls, id: int, account_id: int, created_at: datetime, amount_cents: int, counterparty_name: str,
              counterparty_iban: str, counterparty_bic: str, description: str) -> 'Transfer':
        return cls(id, account_id, created_at, amount_cents, counterparty_name, counterparty_iban, counterparty_bic,
                   description)

    @property
    def account_id(self) -> int:
        return self.__account_id

    @account_id.setter
    def account_id(self, account_id: int) -> None:
        if account_id is None:
            raise InvalidTransferError('Field account_id cannot be empty')
        if not isinstance(account_id, int):
            raise InvalidTransferError('Field account_id must be a valid integer type')
        self.__account_id = account_id

    @property
    def counterparty_iban(self) -> Iban:
        return self.__counterparty_iban

    @counterparty_iban.setter
    def counterparty_iban(self, counterparty_iban: str) -> None:
        try:
            self.__counterparty_iban = Iban(counterparty_iban)
        except InvalidIbanError as e:
            raise InvalidTransferError('Field counterparty_iban %s' % e)

    @property
    def counterparty_bic(self) -> Bic:
        return self.__counterparty_bic

    @counterparty_bic.setter
    def counterparty_bic(self, counterparty_bic: str) -> None:
        try:
            self.__counterparty_bic = Bic(counterparty_bic)
        except InvalidBicError as e:
            raise InvalidTransferError('Field counterparty_bic %s' % e)

    @property
    def counterparty_name(self) -> str:
        return self.__counterparty_name

    @counterparty_name.setter
    def counterparty_name(self, counterparty_name) -> None:
        if counterparty_name is None:
            raise InvalidTransferError('Field counterparty_name cannot be empty')
        if not isinstance(counterparty_name, str):
            raise InvalidTransferError('Field counterparty_name must be a valid string')
        self.__counterparty_name = counterparty_name

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description) -> None:
        if description is None:
            raise InvalidTransferError('Field description cannot be empty')
        if not isinstance(description, str):
            raise InvalidTransferError('Field description must be a valid string')
        self.__description = description

    @property
    def amount_cents(self) -> Amount:
        return self.__amount_cents

    @amount_cents.setter
    def amount_cents(self, amount_cents: int) -> None:
        try:
            self.__amount_cents = Amount(amount_cents)
        except InvalidAmountError as e:
            raise InvalidTransferError('Field amount_cents %s' % e)

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            'account_id': self.account_id,
            'counterparty_name': self.counterparty_name,
            'counterparty_iban': self.counterparty_iban.value,
            'counterparty_bic': self.counterparty_bic.value,
            'amount_cents': self.amount_cents.value,
            'description': self.description,
        }

    def __eq__(self, other: 'Transfer') -> bool:
        return (self.id == other.id and self.created_at == other.created_at
                and self.counterparty_name == other.counterparty_name
                and self.counterparty_iban == other.counterparty_iban
                and self.counterparty_bic == other.counterparty_bic
                and self.amount_cents.value == other.amount_cents.value and self.account_id == other.account_id
                and self.description == other.description)
