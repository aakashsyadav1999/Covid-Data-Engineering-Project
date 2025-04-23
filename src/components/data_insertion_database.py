import os
import pandas as pd
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables from .env file
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")


class MongoDBHandler:
    
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data: List[Dict[str, Any]]) -> None:
        """Insert data into the MongoDB collection."""
        if data:
            self.collection.insert_many(data)

    def close(self) -> None:
        """Close the MongoDB connection."""
        self.client.close()