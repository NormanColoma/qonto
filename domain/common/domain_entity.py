from abc import ABC, abstractmethod
from datetime import datetime


class DomainEntity(ABC):
    @abstractmethod
    def __init__(self, id: int, created_at: datetime = datetime.now()):
        self.id = id
        self.created_at = created_at

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        self.__id = id

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at: datetime) -> None:
        self.__created_at = created_at or datetime.now()

    @abstractmethod
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
