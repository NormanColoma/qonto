from datetime import datetime

import pytest

from domain.common.domain_entity import DomainEntity
from domain.common.invalid_domain_entity_error import InvalidDomainEntityError

id = 1
created_at = datetime.now()


class Foo(DomainEntity):
    def __init__(self, id: int, created_at: datetime):
        super().__init__(id, created_at)

    def to_dict(self) -> dict:
        return super().to_dict()


def test_should_raise_exception_while_instantiating_directly():
    with pytest.raises(TypeError):
        DomainEntity()


def test_should_build_domain_entity():
    foo = Foo(id, created_at)
    assert foo.id == id
    assert foo.created_at == created_at


def test_to_dict():
    foo = Foo(id, created_at)

    expect_dict = {
        'id': id,
        'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

    assert foo.to_dict() == expect_dict
