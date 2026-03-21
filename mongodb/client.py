import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None

    @classmethod
    async def connect_to_mongo(cls):
        """Підключення до MongoDB"""
        if cls.client is None:
            mongo_url = os.getenv("MONGODB_URL", "mongodb://mongo_admin:password@mongodb:27017/library_db")
            cls.client = AsyncIOMotorClient(mongo_url)
            cls.database = cls.client.library_db
            print("✅ Підключено до MongoDB")

    @classmethod
    async def close_mongo_connection(cls):
        """Закриття з'єднання з MongoDB"""
        if cls.client is not None:
            cls.client.close()
            print("✅ З'єднання з MongoDB закрито")

    @classmethod
    def get_database(cls):
        """Отримати базу даних"""
        if cls.database is None:
            raise RuntimeError("MongoDB не підключено. Викличте connect_to_mongo()")
        return cls.database
