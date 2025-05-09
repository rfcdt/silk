from pymongo import MongoClient


class DbConnection:
    def __init__(self, mongodb_uri, db_name):
        self._mongodb_uri = mongodb_uri
        self._db_name = db_name

        self._connection = None

    def get_connection(self) -> MongoClient:
        if not self._connection:
            self._connection = MongoClient(self._mongodb_uri)
        return self._connection
