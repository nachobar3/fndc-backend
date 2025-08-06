from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def get_db() -> AsyncIOMotorClient:
    """Get the database instance"""
    return db.client.fndc


async def connect_to_mongo():
    # Simple configuration that works with MongoDB Atlas
    db.client = AsyncIOMotorClient(settings.MONGO_URI)
    print("✅ Connected to MongoDB.")
    return db.client


async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB.") 