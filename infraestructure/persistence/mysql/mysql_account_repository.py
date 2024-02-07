from sqlalchemy import text

from domain.account.account import Account
from domain.account.account_repository import AccountRepository
from domain.account.iban.iban import Iban
from infraestructure.persistence.mysql.database_handler import SqlAlchemyHandler


class MysqlAccountRepository(AccountRepository):
    def __init__(self, database_handler: SqlAlchemyHandler):
        self.__database_handler = database_handler

    def save(self, account: Account) -> None:
        conn = self.__database_handler.getConnection()
        primitive_values = account.to_dict()
        save_query = text(
            'INSERT into bank_accounts(organization_name, balance_cents, iban, bic, created_at) values ("%s", %s, "%s", "%s", "%s")'
            % (primitive_values['organization_name'],
               primitive_values['balance_cents'], primitive_values['iban'],
               primitive_values['bic'], primitive_values['created_at']) +
            'ON DUPLICATE KEY UPDATE balance_cents=%s, organization_name="%s", iban="%s", bic="%s"'
            % (primitive_values['balance_cents'],primitive_values['organization_name'], primitive_values['iban'],
               primitive_values['bic']))
        conn.execute(save_query)

        if len(account.transfers) > 0:
            bulk_query = ('INSERT into transfers(bank_account_id, counterparty_name,'
                          'counterparty_iban, counterparty_bic, amount_cents, description, created_at) '
                          'values')
            for t in account.transfers:
                primitive_values = t.to_dict()
                bulk_query += (' (%s, "%s", "%s", "%s", %s, "%s", "%s")' % (
                               primitive_values['account_id'], primitive_values['counterparty_name'],
                               primitive_values['counterparty_iban'], primitive_values['counterparty_bic'],
                               primitive_values['amount_cents'], primitive_values['description'],
                               primitive_values['created_at']))
                conn.execute(text(bulk_query))
        conn.commit()

    def find(self, iban: Iban) -> Account:
        conn = self.__database_handler.getConnection()
        result_set = conn.execute(text('SELECT * FROM bank_accounts where iban =  "%s"' % iban.value))
        r = result_set.first()
        return Account.build(id=r.id, iban=r.iban, bic=r.bic,
                             organization_name=r.organization_name, balance_cents=r.balance_cents,
                             created_at=r.created_at) if r is not None else None
