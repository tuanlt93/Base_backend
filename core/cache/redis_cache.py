from config import CFG_REDIS
from .base_cache import BaseCache
from utils.logger import Logger
from redis.asyncio import Redis
import json

class RedisCache(BaseCache):
    def __init__(self) -> None:
        self.__host = CFG_REDIS.get('host', "192.168.240.1")
        self.__port = CFG_REDIS.get('port', 6379)
        self.__db = CFG_REDIS.get('db', 0)
        self.__decode = CFG_REDIS.get('decode_responses', True)

        self.__redis: Redis | None = None
        self.__is_connected = False
        

    async def connect(self):
        """Async connect to Redis server."""
        self.__redis = Redis(
            host=self.__host,
            port=self.__port,
            db=self.__db,
            decode_responses=self.__decode
        )

        try:
            await self.__redis.ping()
            self.__is_connected = True
            Logger().info("Connected to Redis successfully")

        except ConnectionError as e:
            self.__is_connected = False
            Logger().error(f"Failed to connect Redis: {e}")


    async def disconnect(self):
        """Close Redis connection properly."""
        if self.__redis:
            await self.__redis.close()
            Logger().info("Redis connection closed")

    async def get_redis(self) -> Redis:
        return self.__redis

    def get_connection(self) -> bool:
        return self.__is_connected
    
    async def set(self, key: str, value: any):
        """
        Args:
            value: is converting to string
        """
        return await self.__redis.set(key, json.dumps(value), ex= 600)
    
    async def delete(self, key: str):
        return await self.__redis.delete(key)
    
    async def get(self, key: str) -> any:
        rs = await self.__redis.get(key)
        if not rs:
            return None
        return json.loads(rs)
    
    