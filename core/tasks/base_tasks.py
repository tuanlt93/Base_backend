from abc import abstractmethod
from ..safecore.base_metaclass import SingletonABCMeta

class BaseTasks(metaclass = SingletonABCMeta):
    @abstractmethod
    async def start_task(self) -> None: ...
    
    @abstractmethod
    async def start_tasks(self) -> None: ...
    
    @abstractmethod
    async def stop_task(self) -> None: ...

    @abstractmethod
    async def stop_tasks(self) -> None: ...