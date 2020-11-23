from sys import argv, exit
from pymongo import MongoClient
import ijson

db_name = "291db"


def insertJsonRowItems(collection):
    coll_name = collection.name
    with open("json/" + coll_name + ".json", "r") as f:
        documents = ijson.items(f, coll_name.lower() + ".row.item")

        for document in documents:
            collection.insert_one(document)


if __name__ == "__main__":
    if (len(argv) <= 1 or len(argv) > 2):
        print("One database port argument expected, received", len(argv) - 1)
        exit(1)

    client = MongoClient("localhost", int(argv[1]))

    if db_name in client.list_database_names():
        client.drop_database(db_name)
    db = client[db_name]

    for coll in ["Posts", "Tags", "Votes"]:
        if coll in db.list_collection_names():
            db.drop_collection(coll)
            db = db.create_collection(coll)
        insertJsonRowItems(db[coll])
