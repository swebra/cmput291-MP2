
from sys import argv, exit
from pymongo import MongoClient
import ijson

db_name = "291db"


def insertPosts(collection):
    with open("json/Posts.json", "r") as f:
        posts = ijson.items(f, "posts.row.item")
        for post in posts:
            collection.insert_one(post)


def insertTags(collection):
    with open("json/Tags.json", "r") as f:
        tags = ijson.items(f, "tags.row.item")
        for tag in tags:
            collection.insert_one(tag)


def insertVotes(collection):
    with open("json/Votes.json", "r") as f:
        votes = ijson.items(f, "votes.row.item")
        for vote in votes:
            collection.insert_one(vote)


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

    insertPosts(db.Posts)
    insertTags(db.Tags)
    insertVotes(db.Votes)
