from abc import abstractmethod
from core.safecore.base_metaclass import SingletonABCMeta

class BaseCache(metaclass=SingletonABCMeta):

    @abstractmethod
    async def connect(self) -> bool: ...
    
    @abstractmethod
    async def disconnect(self) -> None: ...

    @abstractmethod
    async def get_redis(self) -> bool: ...

    @abstractmethod
    def get_connection(self) -> None: ...

    @abstractmethod
    async def set(self, key: str, value): ...

    @abstractmethod
    async def get(self, key: str) -> str: ...

    @abstractmethod
    async def delete(self, key): ...
