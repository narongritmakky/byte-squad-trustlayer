from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import List, Dict, Any, Optional
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class MongoDBConnector(BaseConnector):
    def __init__(self, uri: str, database: str, collection: str,
                 query: Optional[Dict] = None, **kwargs):
        super().__init__(**kwargs)
        self.uri = uri
        self.database = database
        self.collection = collection
        self.query = query or {}

    def extract(self) -> List[Dict[str, Any]]:
        client = MongoClient(self.uri, serverSelectionTimeoutMS=10000)
        try:
            db = client[self.database]
            docs = list(db[self.collection].find(self.query))
            for doc in docs:
                doc["_id"] = str(doc["_id"])
            return docs
        except PyMongoError as exc:
            raise ConnectorError(f"MongoDB query failed: {exc}") from exc
        finally:
            client.close()
