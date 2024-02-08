import uuid
from datetime import datetime

from domain.account.amount.amount import Amount
from domain.account.amount.invalid_amount_error import InvalidAmountError
from domain.account.bic.bic import Bic
from domain.account.bic.invalid_bic_error import InvalidBicError
from domain.account.iban.iban import Iban
from domain.account.iban.invalid_bic_error import InvalidIbanError
from domain.account.insufficient_funds_error import InsufficientFundsError
from domain.account.invalid_account_error import InvalidAccountError
from domain.account.invalid_transfer_operation_error import InvalidTransferOperationError
from domain.account.transfer.transfer import Transfer
from domain.account.transfer_done_event import TransferDoneEvent
from domain.common.aggregate_root import AggregateRoot


class Account(AggregateRoot):
    def __init__(self, id: int, iban: str, bic: str, organization_name: str, created_at: datetime):
        super().__init__(id, created_at)
        self.balance_cents = 0
        self.iban = iban
        self.bic = bic
        self.organization_name = organization_name
        self.transfers = []

    @classmethod
    def build(cls, id: int, iban: str, bic: str, created_at: datetime, organization_name: str,
              balance_cents: int = 0) -> 'Account':
        account = cls(id, iban, bic, organization_name, created_at)
        account.balance_cents = balance_cents

        return account

    @property
    def iban(self) -> Iban:
        return self.__iban

    @iban.setter
    def iban(self, iban: str) -> None:
        try:
            self.__iban = Iban(iban)
        except InvalidIbanError as e:
            raise InvalidAccountError('Field iban %s' % e)

    @property
    def bic(self) -> Bic:
        return self.__bic

    @bic.setter
    def bic(self, bic: str) -> None:
        try:
            self.__bic = Bic(bic)
        except InvalidBicError as e:
            raise InvalidAccountError('Field bic %s' % e)

    @property
    def balance_cents(self) -> Amount:
        return self.__balance_cents

    @balance_cents.setter
    def balance_cents(self, balance_cents: int) -> None:
        try:
            self.__balance_cents = Amount(balance_cents)
        except InvalidAmountError as e:
            raise InvalidAccountError('Field balance_cents %s' % e)

    @property
    def organization_name(self) -> str:
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, organization_name) -> None:
        if organization_name is None:
            raise InvalidAccountError('Field organization_name cannot be empty')
        if not isinstance(organization_name, str):
            raise InvalidAccountError('Field organization_name must be a valid string')
        self.__organization_name = organization_name

    @property
    def transfers(self) -> [Transfer]:
        return self.__transfers

    @transfers.setter
    def transfers(self, transfers: [Transfer]):
        self.__transfers = transfers

    def do_transfer(self, amount: Amount, counterparty_iban: Iban, counterparty_bic: Bic, counterparty_name: str,
                    description: str) -> None:
        if self.iban == counterparty_iban:
            raise InvalidTransferOperationError('Cannot perform transfer to the same account')

        updated_balance = self.balance_cents.value - amount.value
        if updated_balance < 0:
            raise InsufficientFundsError('There are no sufficient funds for doing the transfer')

        self.balance_cents = updated_balance
        transfer = Transfer.build(account_id=self.id, amount_cents=amount.value,
                                  counterparty_iban=counterparty_iban.value, counterparty_bic=counterparty_bic.value,
                                  counterparty_name=counterparty_name, description=description,
                                  created_at=datetime.now(),
                                  id=None)
        self.__add_transfer(transfer)
        self.add_event(TransferDoneEvent(self, transfer))

    def __add_transfer(self, transfer: Transfer) -> None:
        self.__transfers.append(transfer)

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            'iban': self.iban.value,
            'bic': self.bic.value,
            'balance_cents': self.balance_cents.value,
            'organization_name': self.organization_name,
        }

    def __eq__(self, other: 'Account') -> bool:
        if isinstance(other, Account):
            return (self.iban == other.iban and self.bic == other.bic and self.balance_cents == other.balance_cents
                    and self.id == other.id and self.created_at == other.created_at
                    and self.organization_name == other.organization_name)
        return False
