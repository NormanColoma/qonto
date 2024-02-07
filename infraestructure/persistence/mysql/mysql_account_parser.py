from datetime import datetime
from typing import List

from sqlalchemy import String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from domain.account.account import Account


class Base(DeclarativeBase):
    pass


class AccountRow(Base):
    __tablename__ = 'bank_accounts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    iban: Mapped[str] = mapped_column(String(34), nullable=False, unique=True)
    bic: Mapped[str] = mapped_column(String(11), nullable=False)
    organization_name: Mapped[str] = mapped_column(String(255), nullable=False)
    balance_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    transfers: Mapped[List["TransferRow"]] = relationship()

    def toDict(self):
        return {
            'id': self.id,
            'iban': self.iban,
            'bic': self.bic,
            'organization_name': self.organization_name,
            'balance_cents': self.balance_cents,
            'created_at': self.created_at,
        }


class TransferRow(Base):
    __tablename__ = 'transfers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bank_account_id: Mapped[int] = mapped_column(ForeignKey("bank_accounts.id"))
    counterparty_iban: Mapped[str] = mapped_column(String(34), nullable=False, unique=True)
    counterparty_bic: Mapped[str] = mapped_column(String(11), nullable=False)
    counterparty_name: Mapped[str] = mapped_column(String(255), nullable=False)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    account: Mapped["AccountRow"] = relationship(back_populates="transfers")

    def toDict(self):
        return {
            'id': self.id,
            'bank_account_id': self.bank_account_id,
            'counterparty_iban': self.counterparty_iban,
            'counterparty_bic': self.counterparty_bic,
            'counterparty_name': self.counterparty_name,
            'amount_cents': self.amount_cents,
            'description': self.description,
            'created_at': self.created_at,
        }


class MySqlAccountParser:
    def toDatabase(self, account: Account) -> AccountRow:
        row = AccountRow()
        row.id = account.id
        row.iban = account.iban.value
        row.bic = account.bic.value
        row.organization_name = account.organization_name
        row.balance_cents = account.balance_cents.value
        row.created_at = account.created_at
        for t in account.transfers:
            t_row = TransferRow()
            t_row.bank_account_id = t.account_id
            t_row.counterparty_iban = t.counterparty_iban.value
            t_row.counterparty_bic = t.counterparty_bic.value
            t_row.counterparty_name = t.counterparty_name
            t_row.amount_cents = t.amount_cents.value
            t_row.description = t.description
            t_row.created_at = t.created_at
            row.transfers.append(t_row)
        return row

    def toDomain(self, row: AccountRow) -> Account:
        return Account.build(id=row.id, iban=row.iban, bic=row.bic,
                             organization_name=row.organization_name, balance_cents=row.balance_cents,
                             created_at=row.created_at) if row is not None else None
