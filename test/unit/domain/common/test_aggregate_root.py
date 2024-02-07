import uuid
from datetime import datetime
from uuid import UUID
import pytest

from domain.common.aggregate_root import AggregateRoot
from domain.common.bus.event.domain_event import DomainEvent

id = 1


class Foo(AggregateRoot):
    def __init__(self, id: int, created_at: datetime = datetime.now()):
        super().__init__(id, created_at)

    def to_dict(self) -> dict:
        pass


def test_should_raise_exception_while_instantiating_directly():
    with pytest.raises(TypeError):
        AggregateRoot()


def test_should_pull_events():
    foo = Foo(id)

    assert len(foo.pull_events()) == 0


def test_should_add_event():
    class Event(DomainEvent):

        def __init__(self):
            pass

    foo = Foo(id)
    foo.add_event(Event())
    assert len(foo.pull_events()) == 1
    assert len(foo.pull_events()) == 0
