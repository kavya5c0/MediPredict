from motor.motor_asyncio import AsyncIOMotorClient
from redis import asyncio as aioredis
from app.core.config import settings

# MongoDB Connection
client = AsyncIOMotorClient(settings.MONGODB_URI)
database = client.healthcare_db

# Collections
users_collection = database.users
medical_reports_collection = database.medical_reports
predictions_collection = database.predictions
chat_history_collection = database.chat_history

# Redis Connection
redis_client = None

async def init_redis():
    global redis_client
    redis_client = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)

async def close_redis():
    if redis_client:
        await redis_client.close()

async def get_database():
    return database

async def get_redis():
    return redis_client
