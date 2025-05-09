from typing import Any, Dict, List, Optional

from pymongo.collection import Collection

class MongoRepository:
    def __init__(self, collection: Collection):
        self._collection = collection

    def find_by_filter(self, filter_: Dict[str, Any]) -> List[Dict[str, Any]]:
        data = self._collection.find(filter_)
        print("-------------")
        print("repository")
        print(data)
        return list(self._collection.find(filter_))

    def save_many(self, data: List[Dict[str, Any]]) -> Any:
        return self._collection.insert_many(data)
