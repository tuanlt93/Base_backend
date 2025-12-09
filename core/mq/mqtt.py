# mq/mqtt_mq.py
from asyncio_mqtt import Client, MqttError
from utils.pattern import Singleton
from utils.logger import Logger
from typing import Callable, Awaitable


class MQTTMQ(metaclass=Singleton):
    def __init__(self, host="localhost"):
        self.host = host
        self.client: Client | None = None

    # ----------------------------------------------------------------------
    async def connect(self):
        self.client = Client(self.host)
        await self.client.connect()
        Logger().info("MQTT connected")

    async def disconnect(self):
        if self.client:
            await self.client.disconnect()
            Logger().info("MQTT disconnected")

    # ----------------------------------------------------------------------
    async def publish(self, topic: str, message: str):
        await self.client.publish(topic, message)

    # ----------------------------------------------------------------------
    async def subscribe(self, topic: str, callback: Callable[[str], Awaitable[None]]):
        async with self.client.unfiltered_messages() as messages:
            await self.client.subscribe(topic)
            Logger().info(f"MQTT subscribed to {topic}")

            async for msg in messages:
                await callback(msg.payload.decode())
