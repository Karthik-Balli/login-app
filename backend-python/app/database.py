from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI
import asyncio

client = AsyncIOMotorClient(MONGO_URI)
db = client["test"]
users_collection = db["users"]

async def test_connection():
    print(">> Connecting to MongoDB...")
    user = await users_collection.find_one({})
    if user:
        print("✅ Connection successful! Sample user document:")
        print(user)
    else:
        print("⚠️ Connected, but no user data found in collection.")

# Run only when executed directly
if __name__ == "__main__":
    asyncio.run(test_connection())
