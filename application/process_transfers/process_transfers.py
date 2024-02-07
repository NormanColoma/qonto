from application.application_service import ApplicationService
from application.process_transfers.process_transfers_command import ProcessTransfersCommand
from domain.account.account_not_found_error import AccountNotFoundError
from domain.account.account_repository import AccountRepository
from domain.account.bic.bic import Bic
from domain.account.iban.iban import Iban
from domain.common.bus.event.event_bus import EventBus


class ProcessTransfers(ApplicationService):
    def __init__(self, account_repository: AccountRepository, event_bus: EventBus):
        self.__repository = account_repository
        self.__bus = event_bus

    def execute(self, command: ProcessTransfersCommand):
        account = self.__repository.find(Iban(command.organization_iban))

        if account is None:
            raise AccountNotFoundError('There is no account with iban %s' % command.organization_iban)

        for t in command.credit_transfers:
            quantity = float(t['amount'])
            counterparty_iban = Iban(t['counterparty_iban'])
            counterparty_bic = Bic(t['counterparty_bic'])
            counterparty_name = t['counterparty_name']
            desc = t['description']
            account.do_transfer(quantity=quantity, counterparty_iban=counterparty_iban,
                                counterparty_bic=counterparty_bic, counterparty_name=counterparty_name,
                                description=desc)

        self.__repository.save(account)
        self.__bus.publish(account.pull_events())
