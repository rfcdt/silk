import argparse
import os

from dotenv import load_dotenv
from pymongo.collection import Collection

from app.use_case.merge_hosts import MergeHostDto, MergeHostUseCase
from db import DbConnection

load_dotenv()

API_KEY = os.environ["API_KEY"]
MONGODB_URI = os.environ["MONGODB_URI"]
MONGO_INITDB_DATABASE = os.environ["MONGO_INITDB_DATABASE"]
CHOICES = ["qualys", "crowdstrike"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=CHOICES, required=True)
    args = parser.parse_args()

    source = args.source  # qualys | crodstrike
    
    collection = get_mongodb_collection()

    use_case = MergeHostUseCase()
    use_case.merge(MergeHostDto(
        source=source,
        collection=collection,
        api_key=API_KEY,
    ))


def get_mongodb_collection() -> Collection:
    print("Connection to Mongo is in progress.")
    try:
        db_connector = DbConnection(MONGODB_URI, MONGO_INITDB_DATABASE)
    except Exception as exc:
        print("Error with connection to db. ", exc)
        # log
        return

    print("Connection is ready.")
    connection = db_connector.get_connection()
    db = connection[MONGO_INITDB_DATABASE]

    collection = db["test"]

    # add indexes with asc order as we don't care of it
    fields = {
        "instance_id": 1,
        "hostname": 1,
        "local_ip": 1,
        "public_ip": 1,
        "os": 1,
        "platform": 1,
        "manufacturer": 1,
        "model": 1,
        "availability_zone": 1,
    }
    collection.create_index(fields, unique=True)

    return collection


if __name__ == "__main__":
    main()
