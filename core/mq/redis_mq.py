from redis.asyncio import Redis
from redis.exceptions import ConnectionError
from utils.logger import Logger
from typing import Callable, Awaitable
from .base_mq import BaseMQ
from core.cache.redis_cache import RedisCache


class RedisMQ(BaseMQ):
    def __init__(self, cache: RedisCache) -> None:
        self.__redis_cache = cache
        self.__redis: Redis = self.__redis_cache.get_redis()
        self.__pubsub = None

        self.__is_connected = self.__redis_cache.get_connection()
        

    async def connect(self) -> None:
        """Async connect to Redis server."""
        try:
            await self.__redis.ping()
            self.__is_connected = True
            Logger().info("Connected to Redis successfully")
            
        except ConnectionError as e:
            self.__is_connected = False
            Logger().error(f"Failed to connect Redis: {e}")
            

    async def disconnect(self):
        """Close Redis connection properly."""
        if self.__redis and not self.__redis_cache.get_connection():
            await self.__redis.close()
            Logger().info("Redis connection closed")

    def get_connection(self) -> bool:
        return self.__is_connected

    async def publisher(self, topic: str, message: str):
        """Async publish message to a topic."""
        if not self.__redis:
            Logger().error("Redis not connected")
            return

        await self.__redis.publish(topic, message)

    async def subscriber(self, topic: str, callback: Callable[[str], Awaitable[None]]):
        """
        Async subscriber.
        - topic: Redis channel
        - callback: async function(message: str)
        """
        if not self.__redis:
            Logger().error("Redis not connected")
            return

        self.__pubsub = self.__redis.pubsub()
        await self.__pubsub.subscribe(topic)
        Logger().info(f"Subscribed to Redis topic: {topic}")

        async for message in self.__pubsub.listen():
            # Redis sends messages for "subscribe", "psubscribe", etc.
            if message["type"] == "message":
                data = message["data"]
                await callback(data)
