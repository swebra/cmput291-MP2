
from pymongo import MongoClient
import datetime
import random, string


client = None
db = None

#TODO:
def generate_unique_post_id(length):
    """Generates unique Id of a post

    Returns:
    (string): Unique Id
    """
    while(True):
            key = ''.join(random.choice(string.digits) for _ in range(length))

            try:
                result = db.Posts.find_one({"Id": key})
                if result is None:
                    return key
            except Exception as e:
                print(e)


def connect(port):
    """Attempts to connect to the database
    Args:
    Returns:
        (bool): True on connection success, False otherwise
    """
    try:
        global client
        client = MongoClient('localhost', port)

        global db
        db = client['291db']
        return True
    except Exception as e:
        print(e)
        return False

    return True


def post_question(title, body, uid, tags):
    """Posts a new question

    Args:
        title (str): The title of the new question post
        body (str): The body of the new question post
        uid (str): The uid of the question's poster
        tags(list): list of tags
    Returns:
        (bool): True on success, False otherwise
    """
    try:
        post = {
            "PostTypeId": "1",
            "CreationDate": datetime.datetime.utcnow(),
            "Score": 0,
            "ViewCount": 0,
            "Body": body,
            "Title": title,
            "Tags": ",".join(tags),
            "AnswerCount": 0,
            "CommentCount": 0,
            "FavoriteCount": 0,
            "ContentLicense": "CC BY-SA 2.5"
        }

        if uid is not None:
            post["OwnerUserId"] = uid

        post["Id"] = generate_unique_post_id(10)

        post_id = db.Posts.insert_one(post).inserted_id
    except Exception as e:
        print(e)
        return False

    return True


def search_questions(keywords):
    """Searches all posts related by keywords

    Args:
        keywords([str]): The keywords to search for
    Returns:
        ([results row]): The list of matching posts
    """
    print("Searching posts...", keywords)
    try:
        conditions = []
        for keyword in keywords:
            conditions.append({"Title" : {"$regex" : ".*" + keywords[0] + ".*", "$options": "-i"}})
            conditions.append({"Body" : {"$regex" : ".*" + keywords[0] + ".*", "$options": "-i"}})
            conditions.append({"Tags" : {"$regex" : ".*" + keywords[0] + ".*", "$options": "-i"}})

        query = {
            "$and" : [
                {"PostTypeId": "1"},
                { "$or" : conditions}
            ]
        }

        return list(db.Posts.find(query))
        
    except Exception as e:
        print(e)
        return []

def get_answers_to_question(question):
    """Returns all the answers to a given question

    Args:
        question (): The question whose answers are to be returned
    Returns:
        ([results row]): The list of answers
    """
    try:
        query = {
            "$and": [
                {"PostTypeId": "2"},
                {"ParentId": question["Id"]}
            ]
        }
        return list(db.Posts.find(query))

    except Exception as e:
        print(e)
        return []

def increment_question_view_count(post):
    """Increments the view count of question's related post

    Args:
        post (): the post whose ViewCount is to be incremented
    Returns:
        (bool): True on success, False otherwise
    """
    try:
        query = {"Id": post["Id"]}
        newvalues = {"$set": {"ViewCount": (post["ViewCount"] + 1)}}
        db.Posts.update_one(query, newvalues)
    except Exception as e:
        print(e)
        return False

    print("Incremented question view count...")
    return True

def post_answer(qid, body, uid):
    """Posts an answer in response to a given question

    Args:
        qid (str): the id of the question being answer
        body (str): the body of the answer
        uid (str): the id of the poster who is answering
    Returns:
        (bool): True on success, False otherwise
    """
    try:
        post = {
            "PostTypeId": "2",
            "ParentId": qid,
            "CreationDate": datetime.datetime.utcnow(),
            "Score": 0,
            "CommentCount": 0,
            "Body": body,
            "ContentLicense": "CC BY-SA 2.5"
        }

        if uid is not None:
            post["OwnerUserId"] = uid

        post["Id"] = generate_unique_post_id(10)

        post_id = db.Posts.insert_one(post).inserted_id
    except Exception as e:
        print(e)
        return False

    return True
