from abc import ABC, abstractmethod
from uuid import UUID

from domain.account.account import Account
from domain.account.iban.iban import Iban


class AccountRepository(ABC):
    @abstractmethod
    def find(self, iban: Iban) -> Account: raise NotImplementedError

    @abstractmethod
    def save(self, account: Account) -> None: raise NotImplementedError
