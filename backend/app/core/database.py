import asyncpg
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL Connection
pool = None

async def init_db():
    """Initialize PostgreSQL connection pool"""
    global pool
    try:
        pool = await asyncpg.create_pool(
            settings.DATABASE_URL,
            min_size=2,
            max_size=10
        )
        logger.info("PostgreSQL connection pool created successfully")
    except Exception as e:
        logger.error(f"PostgreSQL connection failed: {e}")
        pool = None

async def close_db():
    """Close PostgreSQL connection pool"""
    global pool
    if pool:
        await pool.close()
        logger.info("PostgreSQL connection pool closed")

async def get_db():
    """Get database connection from pool"""
    if pool is None:
        raise Exception("Database not connected")
    return pool.acquire()

async def release_db(conn):
    """Release database connection back to pool"""
    if pool:
        await pool.release(conn)
