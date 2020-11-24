from sys import argv, exit
import re
from pymongo import MongoClient
import ijson

db_name = "291db"
buffer_size = 1000
term_pattern = re.compile("\w{3,}")


def insertJsonRowItems(collection):
    coll_name = collection.name
    is_posts = coll_name == "Posts"
    with open("json/" + coll_name + ".json", "r") as f:
        docs = ijson.items(f, coll_name.lower() + ".row.item")

        doc_buffer = []
        for doc in docs:
            if is_posts:
                term_list = getTermList(doc)
                if term_list:
                    doc["terms"] = term_list

            doc_buffer.append(doc)
            if len(doc_buffer) >= buffer_size:
                collection.insert_many(doc_buffer)
                doc_buffer = []
        # "Flush" any remaining docs in buffer
        if doc_buffer:
            collection.insert_many(doc_buffer)


def getTermList(doc):
    # String concatenation marginally faster than regex*2 and set union
    title_body_str = doc.get("Title", "") + " " + doc.get("Body", "")
    return list(set(map(str.lower, term_pattern.findall(title_body_str))))


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

    db.Posts.create_index("terms")
