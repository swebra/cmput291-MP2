from sys import argv, exit
import re
import multiprocessing
from pymongo import MongoClient
import ijson

db_name = "291db"
buffer_size = 10000
term_pattern = re.compile("[A-Za-z0-9]{3,}")


def insert_json(collection):
    coll_name = collection.name
    with open("json/" + coll_name + ".json", "r") as f:
        docs = ijson.items(f, coll_name.lower() + ".row.item")

        doc_buffer = []
        for doc in docs:
            doc_buffer.append(doc)
            if len(doc_buffer) >= buffer_size:
                insert_doc_list(collection, doc_buffer)
                doc_buffer = []
        # "Flush" any remaining docs in buffer
        if doc_buffer:
            insert_doc_list(collection, doc_buffer)


def insert_doc_list(collection, doc_list):
    if collection.name == "Posts":
        with multiprocessing.Pool() as pool:
            doc_list = list(pool.map(add_term_list, doc_list))

    collection.insert_many(doc_list)


def add_term_list(doc):
    # String concatenation marginally faster than regex*3 and set updates
    title_body_str = doc.get("Title", "") + " " + doc.get("Body", "") \
                     + " " + doc.get("Tags", "")
    terms = set(term_pattern.findall(title_body_str))
    if terms:
        doc["Terms"] = [term.lower() for term in terms]
    return doc


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
        insert_json(db[coll])

    db.Posts.create_index("Terms")
