from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as aioredis
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB Connection
# Motor connections are lazy - they connect on first operation
# Don't use synchronous ping() at import time as it will block startup
try:
    client = AsyncIOMotorClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
    database = client.healthcare_db
    logger.info("MongoDB client initialized (connection will be established on first use)")
except Exception as e:
    logger.warning(f"MongoDB client initialization failed: {e}. Running without database.")
    client = None
    database = None

# Collections
if database is not None:
    users_collection = database.users
    medical_reports_collection = database.medical_reports
    predictions_collection = database.predictions
    chat_history_collection = database.chat_history
else:
    users_collection = None
    medical_reports_collection = None
    predictions_collection = None
    chat_history_collection = None

# Redis Connection
redis_client = None

async def init_redis():
    global redis_client
    try:
        redis_client = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        await redis_client.ping()
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}. Running without cache.")
        redis_client = None

async def close_redis():
    if redis_client:
        try:
            await redis_client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.warning(f"Redis close failed: {e}")

async def get_database():
    return database

async def get_redis():
    return redis_client
