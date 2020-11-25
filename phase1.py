from sys import argv, exit
from pathlib import Path
import re
from pymongo import MongoClient
import ijson

db_name = "291db"
buffer_size = 1000
term_pattern = re.compile("[A-Za-z0-9]{3,}")


def insert_json(collection, json_dir):
    """Inserts items into the given collection read from a JSON file
    The JSON file is expected to match the collection's name, and have a list
    of data entries under the <collection name>.row field. Reading is buffered
    according to the global `buffer_size` parameter to limit memory usage.

    Args:
        collection (collection): Mongo collection to insert JSON data into
        json_dir (str): Path to directory containing the expected JSON file
    """
    coll_name = collection.name
    is_posts = coll_name == "Posts"
    json_path = Path(json_dir, coll_name + ".json")
    if not json_path.exists():
        print(json_path, "could not be found, data not read.")
        return

    with json_path.open(mode="r") as f:
        print("Parsing", str(json_path) + "...")
        docs = ijson.items(f, coll_name.lower() + ".row.item")

        doc_buffer = []
        for doc in docs:
            if is_posts:
                add_term_list(doc)

            doc_buffer.append(doc)
            if len(doc_buffer) >= buffer_size:
                collection.insert_many(doc_buffer)
                doc_buffer = []
        # "Flush" any remaining docs in buffer
        if doc_buffer:
            collection.insert_many(doc_buffer)


def add_term_list(doc):
    """Creates and adds a term list to the given document
    Title, body, and tag fields are parsed for alphanumeric substrings and the
    resulting list is added to the given document under the "Terms" field.

    Args:
        doc: Document (dictionary) to which the term list is added
    """
    # String concatenation marginally faster than regex*3 and set updates
    title_body_str = doc.get("Title", "") + " " + doc.get("Body", "") \
                     + " " + doc.get("Tags", "")
    terms = set(term_pattern.findall(title_body_str))
    if terms:
        doc["Terms"] = [term.lower() for term in terms]


if __name__ == "__main__":
    if (len(argv) <= 1):
        print("Database port expected as a command-line argument")
        exit(1)

    if (len(argv) > 3):
        print("Maximum of two command-line arguments expected (port and json",
              "directory), received", len(argv) - 1)
        exit(1)

    client = MongoClient("localhost", int(argv[1]))

    if db_name in client.list_database_names():
        client.drop_database(db_name)
    db = client[db_name]

    for coll in ["Posts", "Tags", "Votes"]:
        if coll in db.list_collection_names():
            db.drop_collection(coll)
            db = db.create_collection(coll)
        insert_json(db[coll], argv[2])

    print("Creating index...")
    db.Posts.create_index("Terms")
    print("Done")
