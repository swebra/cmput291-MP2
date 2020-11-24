
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


def search_posts(keywords):
    """Searches all posts related by keywords

    Args:
        keywords([str]): The keywords to search for
    Returns:
        ([results row]): The list of matching posts
    """
    #TODO: Implement
    print("Searching posts...", keywords)
    return [1, 2 ,3]


def increment_question_view_count(post):
    #TODO: Implement
    print("Incremented question view count...")
