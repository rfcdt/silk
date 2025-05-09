from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Any, Dict, List, Optional


from contextlib import AbstractContextManager

from repositories.base import AbstractMongoRepository


class MongoRepository(AbstractMongoRepository, AbstractContextManager):
    def __init__(self, uri: str, db_name: str):
        self._uri = uri
        self._db_name = db_name
        self._client = None
        self._db = None

    def __enter__(self) -> "MongoRepository":
        self._client = MongoClient(self._uri)
        self._db = self._client[self._db_name]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def find(self, collection: str) -> List[Dict[str, Any]]:
        return list(self._db[collection].find())

    def find_by_filter(self, collection: str, filter_: Dict[str, Any]) -> List[Dict[str, Any]]:
        return list(self._db[collection].find(filter_))

    def save(self, collection: str, data: Dict[str, Any]) -> Any:
        return self._db[collection].insert_one(data).inserted_id

    def close(self) -> None:
        if self._client:
            self._client.close()