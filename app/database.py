from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import ssl


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def get_db() -> AsyncIOMotorClient:
    """Get the database instance"""
    return db.client.fndc


async def connect_to_mongo():
    # Configuración optimizada para MongoDB Atlas
    client_options = {
        "serverSelectionTimeoutMS": 5000,
        "connectTimeoutMS": 10000,
        "socketTimeoutMS": 20000,
        "maxPoolSize": 10,
        "minPoolSize": 1,
        "maxIdleTimeMS": 30000,
        "retryWrites": True,
        "retryReads": True,
        "tlsAllowInvalidCertificates": True,
        "tlsAllowInvalidHostnames": True,
    }
    
    try:
        db.client = AsyncIOMotorClient(settings.MONGO_URI, **client_options)
        # Test the connection
        await db.client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully")
        return db.client
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        # Fallback configuration without SSL options
        try:
            db.client = AsyncIOMotorClient(settings.MONGO_URI)
            await db.client.admin.command('ping')
            print("✅ Connected to MongoDB with fallback configuration")
            return db.client
        except Exception as e2:
            print(f"❌ Fallback connection also failed: {e2}")
            raise


async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB.") 