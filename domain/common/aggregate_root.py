from abc import abstractmethod
from datetime import datetime

from domain.common.bus.event.domain_event import DomainEvent
from domain.common.domain_entity import DomainEntity


class AggregateRoot(DomainEntity):
    @abstractmethod
    def __init__(self, id: int, created_at: datetime = datetime.now()):
        super().__init__(id, created_at)
        self.__events = []

    def pull_events(self) -> [DomainEvent]:
        events = self.__events
        self.__events = []
        return events

    def add_event(self, event: DomainEvent) -> None:
        if isinstance(event, DomainEvent):
            self.__events.append(event)
