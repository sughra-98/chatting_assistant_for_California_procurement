"""
MongoDB connection management
this module handles connecting to and disconnecting from a MongoDB database.

"""
from pymongo import MongoClient
from pymongo.database import Database
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    """MongoDB connection manager"""
    
    def __init__(self):
        self.client: MongoClient = None
        self.db: Database = None
        
    def connect(self):
        """Connect to MongoDB"""
        try:
            settings = get_settings()
            self.client = MongoClient(settings.mongodb_uri)
            self.db = self.client[settings.mongodb_database]
            
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {settings.mongodb_database}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("MongoDB disconnected")
    
    def get_collection(self, collection_name: str):
        """Get a MongoDB collection"""
        if not self.db:
            raise RuntimeError("Database not connected")
        return self.db[collection_name]


# Global MongoDB instance
mongodb = MongoDB()


def get_database() -> Database:
    """Get MongoDB database instance"""
    return mongodb.db
