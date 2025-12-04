from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# MongoDB client instance
client: AsyncIOMotorClient = None


def get_database():
    """Get the database instance"""
    return client[settings.MONGODB_DB_NAME]


async def connect_to_mongo():
    """Connect to MongoDB on startup"""
    global client
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    print(f"✅ Connected to MongoDB at {settings.MONGODB_URL}")
    print(f"📦 Using database: {settings.MONGODB_DB_NAME}")


async def close_mongo_connection():
    """Close MongoDB connection on shutdown"""
    global client
    if client:
        client.close()
        print("❌ Closed MongoDB connection")
