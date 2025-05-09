from typing import Any, Dict, List, Optional

from pymongo.collection import Collection

class MongoRepository:
    def __init__(self, collection: Collection):
        self._collection = collection

    def find(self, collection: str) -> List[Dict[str, Any]]:
        return list(self._collection[collection].find())

    def find_by_filter(self, collection: str, filter_: Dict[str, Any]) -> List[Dict[str, Any]]:
        return list(self._collection[collection].find(filter_))

    def save(self, collection: str, data: Dict[str, Any]) -> Any:
        return self._collection[collection].insert_one(data).inserted_id
