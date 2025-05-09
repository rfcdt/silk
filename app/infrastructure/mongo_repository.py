from typing import Any

from pymongo import UpdateOne
from pymongo.collection import Collection


class MongoRepository:
    def __init__(self, collection: Collection):
        self._collection = collection

    def find_by_filter(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        return list(self._collection.find({"$or": filters}))

    def save_many(self, data: list[dict[str, Any]]):
        if not data:
            return None
        return self._collection.insert_many(data)

    def update_many(self, data: list[dict[str, Any]]):
        if not data:
            return None

        updated_data = [
            UpdateOne(
                {
                    "instance_id": item["instance_id"],
                    "hostname": item["hostname"],
                    "local_ip": item["local_ip"],
                    "public_ip": item["public_ip"],
                    "os": item["os"],
                    "platform": item["platform"],
                    "manufacturer": item["manufacturer"],
                    "model": item["model"],
                    "availability_zone": item["availability_zone"],
                },
                {"$set": item},
            )
            for item in data
        ]
        return self._collection.bulk_write(updated_data)
