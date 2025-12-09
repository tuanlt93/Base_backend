# mq/redis_stream.py
from redis.asyncio import Redis
from redis.exceptions import ConnectionError
from utils.pattern import Singleton
from utils.logger import Logger
from typing import Callable, Awaitable
import asyncio


class RedisStream(metaclass=Singleton):
    def __init__(self, stream="events", group="workers", consumer="c1"):
        self.stream = stream
        self.group = group
        self.consumer = consumer
        self.redis: Redis | None = None

    # ----------------------------------------------------------------------
    async def connect(self, host="127.0.0.1", port=6379, db=0):
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)

        try:
            await self.redis.xgroup_create(
                name=self.stream,
                groupname=self.group,
                id="0-0",
                mkstream=True
            )
        except Exception:
            pass  # group already exists

        Logger().info("Redis Stream connected")

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

    # ----------------------------------------------------------------------
    async def publish(self, data: dict):
        await self.redis.xadd(self.stream, data)

    async def subscriber(...):
        while True:
            msg = await self._redis.xread(...)
            await callback(msg)

    # ----------------------------------------------------------------------
    async def worker(self, callback: Callable[[dict], Awaitable[None]]):
        """
        Worker đọc message từ Redis Stream theo group.
        """
        while True:
            events = await self.redis.xreadgroup(
                groupname=self.group,
                consumername=self.consumer,
                streams={self.stream: '>'},
                count=10,
                block=5000
            )

            if not events:
                continue

            for _, msgs in events:
                for msg_id, msg_data in msgs:
                    await callback(msg_data)

                    # ACK message
                    await self.redis.xack(self.stream, self.group, msg_id)
