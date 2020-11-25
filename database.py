
from pymongo import MongoClient
import datetime
import random, string

db = None


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


def generate_unique_vote_id(length):
    """Generates unique Id of a vote

    Returns:
    (string): Unique Id
    """
    while(True):
        key = ''.join(random.choice(string.digits) for _ in range(length))

        try:
            result = db.Votes.find_one({"Id": key})
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
    client = MongoClient("localhost", port)

    try:
        global db
        db = client["291db"]
    except Exception as e:
        print(e)
        return False

    return True


def get_user_statistics(uid):
    """Gets statistics about the logged in user

    Args:
        uid (str): The Id of the User to get statistics about
    Returns:
        ((int, float, int, float, int)): A tuple consisting of questionCount,
        avgQuestionScore, answerCount, avgAnswerScore, and voteCount
    """
    try:
        question_stats = list(db.Posts.aggregate([
            {"$match": {"OwnerUserId": uid, "PostTypeId": "1"}},
            {"$group": {
                "_id": "$OwnerUserId",
                "questionCount": {"$sum": 1},
                "avgScore": {"$avg": "$Score"}
            }}
        ]))

        answer_stats = list(db.Posts.aggregate([
            {"$match": {"OwnerUserId": uid, "PostTypeId": "2"}},
            {"$group": {
                "_id": "$OwnerUserId",
                "answerCount": {"$sum": 1},
                "avgScore": {"$avg": "$Score"}
            }}
        ]))

        vote_stats = list(db.Votes.aggregate([
            {"$match": {"UserId": uid}},
            {"$group": {
                "_id": "$UserId",
                "voteCount": {"$sum": 1}
            }}
        ]))


        questionCount = 0 if len(question_stats) == 0 else question_stats[0]["questionCount"]
        avgQuestionScore = 0 if len(question_stats) == 0 else question_stats[0]["avgScore"]
        answerCount = 0 if len(answer_stats) == 0 else answer_stats[0]["answerCount"]
        avgAnswerScore = 0 if len(answer_stats) == 0 else answer_stats[0]["avgScore"]
        voteCount = 0 if len(vote_stats) == 0 else vote_stats[0]["voteCount"]
        return (
            questionCount,
            avgQuestionScore,
            answerCount,
            avgAnswerScore,
            voteCount
        )

    except Exception as e:
        print(e)
        return None


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
            if len(keyword) >= 3:
                conditions.append({"Terms": keyword.lower()})
            else:
                conditions.append({"Title": {"$regex": "^.*" + keyword, "$options": "-i"}})
                conditions.append({"Body": {"$regex": "^.*" + keyword, "$options": "-i"}})
                conditions.append({"Tags": {"$regex": "^.*" + keyword, "$options": "-i"}})

        query = {
            "$and": [
                {"PostTypeId": "1"},
                {"$or": conditions}
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


def post_vote(pid, uid):
    """Posts a vote to a post

    Args:
        pid (str): the Id of the post being voted on
        uid (str): the Id of the current user
    Returns:
        (bool): True on success, False otherwise
    """
    try:
        vote = {
            "PostId": pid,
            "VoteTypeId": "2",
            "CreationDate": datetime.datetime.utcnow(),
        }

        if uid is not None:
            vote["UserId"] = uid
            result = db.Votes.find_one({"PostId": pid, "UserId": uid})
            if result is not None:
                print("You have already voted on this post!")
                return False

        vote["Id"] = generate_unique_vote_id(10)
        vote_id = db.Votes.insert_one(vote).inserted_id
        db.Posts.update_one({"Id": pid}, {"$inc": {"Score": 1}})

    except Exception as e:
        print(e)
        return False

    return True
