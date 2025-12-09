from abc import abstractmethod
from ..safecore.base_metaclass import SingletonABCMeta

class BaseSecurity(metaclass = SingletonABCMeta):
    @abstractmethod
    def hash_password(password: str) -> str: ...

    @abstractmethod
    def verify_password(password: str, hashed: str) -> bool: ...

    @abstractmethod
    def create_access_token(subject: str):
        pass

    @abstractmethod
    def create_refresh_token(subject: str):
        pass

    @abstractmethod
    def decode_token(token: str):
        pass
