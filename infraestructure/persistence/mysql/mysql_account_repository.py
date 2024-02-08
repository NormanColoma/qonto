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
        with self.__database_handler.get_connection() as conn:
            account_row = self.__parser.to_database(account)
            result = conn.query(AccountRow).where(AccountRow.id == account.id).update(account_row.toDict())
            if result == 0:
                conn.add(account_row)
            transfer_rows = account_row.transfers
            conn.add_all(transfer_rows)
            raise Exception

    def find(self, iban: Iban) -> Account:
        with self.__database_handler.get_connection() as conn:
            row = conn.query(AccountRow).where(AccountRow.iban == iban.value).first()
            return self.__parser.to_domain(row)
