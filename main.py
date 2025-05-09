import argparse
import os
from itertools import chain

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from clients import ClientFactory

load_dotenv()


API_KEY = os.environ['API_KEY']

# MONGODB_URI = os.environ["MONGODB_URI"]
# MONGO_INITDB_DATABASE = os.environ["MONGO_INITDB_DATABASE"]



CHOICES = ["qualys", "crowdstrike"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=CHOICES)
    args = parser.parse_args()


    return

    client = MongoClient(MONGODB_URI)
    db = client[MONGO_INITDB_DATABASE]
    collection = db['test']

    client = ClientFactory.get_client('crowdstrike', API_KEY)
    crowdstrike_data = client.fetch_hosts()

    client = ClientFactory.get_client('qualys', API_KEY)
    qualys_data = client.fetch_hosts()

    merged_data = chain(crowdstrike_data, qualys_data)
    
    i = 0
    for item in merged_data:
        i+=1

        t = collection.find_one({"hostname": item.hostname})
        print(t)
        if not t:
            x = collection.insert_one(item)
        else:
            pass
        print(i)


if __name__ == "__main__":
    main()
