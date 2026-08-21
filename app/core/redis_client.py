from redis import asyncio as aioredis
from dotenv import load_dotenv
load_dotenv()
import os

class RedisManager:
    def __init__(self):
        self.client: aioredis.Redis | None = None

    async def connect(self) -> None:
        """Redis bilan aloqa o'rnatish """
        self.client = aioredis.from_url(
            os.getenv("REDIS_URL"),
            decode_responses=True
        )

    async def disconnect(self) -> None:
        """Redis bilan aloqani chiroyli tarzda yopadi"""
        if self.client:
            await self.client.close()


    async def get_client(self) -> aioredis.Redis:
        if self.client is None:
            raise RuntimeError("redis hali ulanmadi")
        return self.client


redis_manager = RedisManager()

