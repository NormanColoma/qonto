from sqlalchemy import update

from domain.account.account import Account
from domain.account.account_repository import AccountRepository
from domain.account.iban.iban import Iban
from infraestructure.persistence.mysql.database_handler import SqlAlchemyHandler
from infraestructure.persistence.mysql.mysql_account_parser import MySqlAccountParser, AccountRow


class MysqlAccountRepository(AccountRepository):
    def __init__(self, database_handler: SqlAlchemyHandler, account_parser: MySqlAccountParser):
        self.__database_handler = database_handler
        self.__parser = account_parser

    def save(self, account: Account) -> None:
        conn = self.__database_handler.getConnection()
        account_row = self.__parser.toDatabase(account)
        result = conn.query(AccountRow).where(AccountRow.id == account.id).update(account_row.toDict())
        if result == 0:
            conn.add(account_row)
        transfer_rows = account_row.transfers
        conn.add_all(transfer_rows)
        conn.commit()

    def find(self, iban: Iban) -> Account:
        conn = self.__database_handler.getConnection()
        row = conn.query(AccountRow).where(AccountRow.iban == iban.value).first()
        return self.__parser.toDomain(row)
