from redis.asyncio import Redis
from redis.exceptions import ConnectionError
from utils.logger import Logger
from typing import Callable, Awaitable
from .base_mq import BaseMQ
from config import CFG_REDIS


class RedisMQ(BaseMQ):
    def __init__(self) -> None:
        self.__host = CFG_REDIS.get('host', "192.168.240.1")
        self.__port = CFG_REDIS.get('port', 6379)
        self.__db = CFG_REDIS.get('db', 0)
        self.__decode = CFG_REDIS.get('decode_responses', True)

        self.__redis: Redis | None = None
        self.__pubsub = None

    async def connect(self) -> bool:
        """Async connect to Redis server."""
        self.__redis = Redis(
            host=self.__host,
            port=self.__port,
            db=self.__db,
            decode_responses=self.__decode
        )

        try:
            await self.__redis.ping()
            Logger().info("Connected to Redis successfully")
            return True
        except ConnectionError as e:
            Logger().error(f"Failed to connect Redis: {e}")
            return False

    async def disconnect(self):
        """Close Redis connection properly."""
        if self.__redis:
            await self.__redis.close()
            Logger().info("Redis connection closed")

    def get_connection(self) -> Redis:
        return self.__redis

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
