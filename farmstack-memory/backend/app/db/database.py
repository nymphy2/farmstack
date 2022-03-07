import motor.motor_asyncio

from core.config import settings


client = motor.motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
db = client.memories
