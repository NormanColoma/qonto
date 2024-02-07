from abc import ABC, abstractmethod

from domain.common.bus.event.domain_event import DomainEvent


class EventBus(ABC):
    @abstractmethod
    def publish(self, events: [DomainEvent]) -> None:
        raise NotImplementedError('Method publish must be implemented')

