import jwt
from passlib.context import CryptContext
from utils.time import *
from .base_security import BaseSecurity
from config import CFG_TOKEN, SECRET_KEY, ALGORITHM

class JWTSecurity(BaseSecurity):

    def __init__(self):
        self.__pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.__pwd.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        return self.__pwd.verify(password, hashed)

    def create_access_token(self, subject: str) -> str:
        expire = add_minutes(now_utc(), CFG_TOKEN["ACCESS_TOKEN_EXPIRE_MINUTES"])
        return jwt.encode({"sub": subject, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

    def create_refresh_token(self, subject: str) -> str:
        expire = add_days(now_utc(), CFG_TOKEN["REFRESH_TOKEN_EXPIRE_DAYS"])
        return jwt.encode({"sub": subject, "exp": expire, "type": "refresh"}, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
