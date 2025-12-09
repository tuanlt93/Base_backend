from abc import abstractmethod
from ..safecore.base_metaclass import SingletonABCMeta

class BaseDB(metaclass=SingletonABCMeta):

    @property
    def Base(self):
        raise NotImplemented

    @abstractmethod
    async def start_db(self) -> None: ...
    
    @abstractmethod
    async def stop_db(self) -> None: ...

    @abstractmethod
    async def get_write_session(self):
        raise NotImplemented

    @abstractmethod
    async def get_read_session(self):
        raise NotImplemented
    
    @abstractmethod
    async def get_session(self):
        raise NotImplemented
