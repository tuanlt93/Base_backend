# mq/kafka_mq.py
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from utils.pattern import Singleton
from utils.logger import Logger
from typing import Callable, Awaitable


class KafkaMQ(metaclass=Singleton):
    def __init__(self, servers="localhost:9092", group_id="my-group"):
        self.servers = servers
        self.group_id = group_id

        self.producer: AIOKafkaProducer | None = None
        self.consumer: AIOKafkaConsumer | None = None

    # ----------------------------------------------------------------------
    async def connect_producer(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.servers)
        await self.producer.start()
        Logger().info("Kafka producer connected")

    async def connect_consumer(self, topics: list[str]):
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self.servers,
            group_id=self.group_id,
            enable_auto_commit=True
        )
        await self.consumer.start()
        Logger().info(f"Kafka consumer subscribed to {topics}")

    # ----------------------------------------------------------------------
    async def disconnect(self):
        if self.producer:
            await self.producer.stop()
        if self.consumer:
            await self.consumer.stop()
        Logger().info("KafkaMQ disconnected")

    # ----------------------------------------------------------------------
    async def publish(self, topic: str, message: str):
        await self.producer.send_and_wait(topic, message.encode())

    # ----------------------------------------------------------------------
    async def subscribe(self, callback: Callable[[str], Awaitable[None]]):
        async for msg in self.consumer:
            data = msg.value.decode()
            await callback(data)
