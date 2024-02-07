from datetime import datetime

from domain.common.bus.event.domain_event import DomainEvent
from domain.common.domain_entity import DomainEntity

id = 1
created_at = datetime.now()


class FooEntity(DomainEntity):
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'field_a': self.__field_a,
            'created_at': self.created_at,
        }

    def __init__(self):
        super().__init__(id, created_at)
        self.__field_a = 'a'


class Foo(DomainEvent):
    def __init__(self):
        data = {
            'test': 'test',
            'another-test': 1,
        }
        super().__init__(FooEntity(), 'foo-event', data)


def test_should_transform_to_dict():
    event = Foo()
    expected_dict = {
        'id': id,
        'name': 'foo-event',
        'entity': {
            'id': id,
            'field_a': 'a',
            'created_at': created_at,
        },
        'entity_name': 'FooEntity',
        'entity_id': id,
        'topic': 'bank_accounts',
        'data': {
            'test': 'test',
            'another-test': 1,
        },
        'occurred_at': created_at,
    }

    event_dict = event.to_dict()
    assert event_dict['name'] == expected_dict['name']
    assert event_dict['entity'] == expected_dict['entity']
    assert event_dict['entity_name'] == expected_dict['entity_name']
    assert event_dict['entity_id'] == expected_dict['entity_id']
    assert event_dict['topic'] == expected_dict['topic']
    assert event_dict['data'] == expected_dict['data']

    assert event_dict['id'] is not None
    assert event_dict['occurred_at'] is not None
