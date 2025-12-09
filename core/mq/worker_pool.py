# mq/worker_pool.py
import asyncio
from utils.pattern import Singleton
from utils.logger import Logger
from typing import Callable, Awaitable


class WorkerPool(metaclass=Singleton):
    def __init__(self, size=5):
        self.size = size
        self.queue: asyncio.Queue = asyncio.Queue()
        self.workers = []

    # ----------------------------------------------------------------------
    async def start(self, handler: Callable[[any], Awaitable[None]]):
        Logger().info(f"Worker Pool started with {self.size} workers")

        for _ in range(self.size):
            worker = asyncio.create_task(self.__worker_loop(handler))
            self.workers.append(worker)

    async def stop(self):
        for _ in range(self.size):
            await self.queue.put(None)

        await asyncio.gather(*self.workers)
        Logger().info("Worker Pool stopped")

    # ----------------------------------------------------------------------
    async def push(self, data: any):
        await self.queue.put(data)

    async def __worker_loop(self, handler):
        while True:
            task = await self.queue.get()
            if task is None:
                break

            try:
                await handler(task)
            except Exception as e:
                Logger().error(f"Worker error: {e}")
