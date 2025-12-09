from abc import abstractmethod
from safecore.base_metaclass import SingletonABCMeta

class BaseCache(metaclass = SingletonABCMeta):

    @abstractmethod
    async def start_up(self) -> None: ...
    
    @abstractmethod
    async def stop_db(self) -> None: ...

    @abstractmethod
    async def get_write_db(self):
        pass

    @abstractmethod
    async def get_read_db(self):
        pass
