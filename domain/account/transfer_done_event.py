from domain.account.transfer.transfer import Transfer
from domain.common.bus.event.domain_event import DomainEvent
from domain.common.domain_entity import DomainEntity


class TransferDoneEvent(DomainEvent):
    def __init__(self, account: DomainEntity, transfer: Transfer):
        data = {
            'transfer': transfer.to_dict()
        }
        super().__init__(account, 'transfer-done', data)
