import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from domain.common.domain_entity import DomainEntity


class DomainEvent(ABC):
    @abstractmethod
    def __init__(self, entity: DomainEntity, name: str, data: dict):
        self.id = uuid.uuid4()
        self.occurred_at = datetime.now()
        self.name = name
        self.entity = entity
        self.entity_name = entity.__class__.__name__
        self.entity_id = entity.id
        self.topic = 'bank_accounts'
        self.data = data

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'name': self.name,
            'entity': self.entity.to_dict(),
            'entity_name': self.entity_name,
            'entity_id': self.entity_id,
            'topic': self.topic,
            'data': self.data,
            'occurred_at': self.occurred_at.strftime('%Y-%m-%d %H:%M:%S'),
        }



