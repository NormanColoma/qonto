from unittest.mock import MagicMock

import pytest

from application.process_transfers.process_transfers import ProcessTransfers
from application.process_transfers.process_transfers_command import ProcessTransfersCommand
from domain.account.account_not_found_error import AccountNotFoundError
from domain.account.amount.amount import Amount
from domain.account.bic.bic import Bic
from domain.account.iban.iban import Iban

repository = MagicMock()
event_bus = MagicMock()
iban = 'ES9121000418450200051333'
bic = 'CCOPFRPPXXX'
amount = '100.00'


@pytest.fixture
def app_service():
    process_transfers = ProcessTransfers(repository, event_bus)
    repository.reset_mock()
    event_bus.reset_mock()
    yield process_transfers


def test_should_raise_exception_if_account_not_found(app_service):
    command = ProcessTransfersCommand(iban, [])
    repository.find.return_value = None

    with pytest.raises(AccountNotFoundError) as e:
        app_service.execute(command)
    assert e.value.args[0] == 'There is no account with iban %s' % iban
    event_bus.assert_not_called()
    repository.find.assert_called_once_with(Iban(iban))


def test_should_propagate_domain_exception(app_service):
    command = ProcessTransfersCommand(iban, [])
    account_domain = MagicMock()
    repository.find.return_value = account_domain
    account_domain.do_transfer.side_effect = Exception

    with pytest.raises(Exception):
        app_service.execute(command)
        repository.find.assert_called_once_with(iban)
        account_domain.do_transfer.assert_called_once_with(amount, [])


def test_should_process_transfers(app_service):
    command = ProcessTransfersCommand(iban, [{
        'amount': amount,
        'counterparty_name': 'name',
        'counterparty_iban': iban,
        'counterparty_bic': bic,
        'description': 'desc',
        'account_id': 1,
    }])
    account_domain = MagicMock()
    repository.find.return_value = account_domain
    account_domain.pull_events.return_value = []

    app_service.execute(command)

    repository.find.assert_called_once_with(Iban(iban))
    account_domain.do_transfer.assert_called_once()
    assert account_domain.do_transfer.call_args[1]['amount'] == Amount(amount)
    assert account_domain.do_transfer.call_args[1]['counterparty_name'] == 'name'
    assert account_domain.do_transfer.call_args[1]['counterparty_iban'] == Iban(iban)
    assert account_domain.do_transfer.call_args[1]['counterparty_bic'] == Bic(bic)
    assert account_domain.do_transfer.call_args[1]['description'] == 'desc'
    account_domain.pull_events.assert_called_once()
    event_bus.publish.assert_called_once_with([])
