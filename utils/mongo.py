import pymongo
from pymongo.database import Database
import motor.motor_asyncio as async_client
import beanie

from models.user import User

models = [User]


class MongoManager:
    client: pymongo.MongoClient = None
    """The connected pymongo client"""

    async_client: pymongo.MongoClient = None
    """The connected async pymongo client"""

    db: Database = None
    """The default pymongo database"""

    async_db: Database = None
    """The default pymongo database"""

    async def connect(self, db_url: str, db_name: str):
        """
        Initialize MongoDB connections. Creates async and sync MongoDB
        clients/DBs

        Args:
            - `db_url`: MongoDB URI
            - `db_name`: Default database name (created if does not exist)
        """
        self.uri = db_url
        self.db_name = db_name

        self.async_client = async_client.AsyncIOMotorClient(
            db_url, maxPoolSize=10, minPoolSize=10
        )

        self.client = pymongo.MongoClient(db_url)
        self.db = self.client[db_name]

        self.async_db = self.async_client[db_name]

    async def init_beanie(self, db_name: str):
        """
        Initialize Beanie models

        Args:
            - `db_name`: Database name (must exist)
        """
        await beanie.init_beanie(
            database=self.async_client[db_name], document_models=models
        )

    async def close(self):
        """Close database connection"""

        self.async_client.close()


manager = MongoManager()


async def get_database() -> MongoManager:
    """Get database manager instance"""

    return manager
