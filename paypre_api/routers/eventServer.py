import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool
from routers.config import loop
import json
# from eventsCallback import callback
# import asyncio
from routers.config import RABBITMQ_HOST,RABBITMQ_PORT,RABBITMQ_USER,RABBITMQ_PASSWORD

async def getConnection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(host=RABBITMQ_HOST,
        port=int(RABBITMQ_PORT),
        login=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD)

connectionPool: Pool = Pool(getConnection, max_size=4 ,loop=loop)

async def getChannel() -> aio_pika.Channel:
    async with connectionPool.acquire() as connection:
        return await connection.channel()

channelPool : Pool = Pool(getChannel, max_size=10 ,loop=loop)

async def publish(queueName, message):
    async with channelPool.acquire() as channel:
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=2,
                content_type="text/plain",
                content_encoding="utf-8"
            ),
            routing_key=queueName
        )
        

        

        