from abc import abstractmethod, ABC


class ApplicationCommand(ABC):
    @abstractmethod
    def __init__(self): raise NotImplementedError
