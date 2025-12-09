from abc import abstractmethod
from typing import Callable
from ..safecore.base_metaclass import SingletonABCMeta

class BaseMQ(metaclass = SingletonABCMeta):

    @abstractmethod
    async def connect(self) -> bool: ...
    
    @abstractmethod
    async def disconnect(self) -> None: ...

    @abstractmethod
    def get_connection(self) -> bool: ...

    @abstractmethod
    async def publisher(self, topic: str, message: str):
        pass

    @abstractmethod
    async def subscriber(self, topic: str, func: Callable):
        pass
