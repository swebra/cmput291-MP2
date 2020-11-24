import database as db

from utils import (
    request_input,
    keyword_input_validate,
    print_options,
    print_invalid_option,
    get_indices_range,
    get_table_info,
    print_table,
    is_index
)

uid = None

def logged_in(uid_param):
    """The execution loop for a user

    Args:
        uid_param (str): The uid of the user
    """
    global uid
    uid = uid_param

    print("To exit program type `/exit` at any point")
    print("In any submenu or input, type `/back` to return up a level.")
    while (True):
        print_options(["Post a question", "Search for questions"])

        action = request_input()[0]

        if action == "/back":
            print("Already at the top-level menu.")
        # Post a Question
        elif (action == "1"):
            post_question()
            print("")
        # Search for posts
        elif (action == "2"):
            post = search_select_questions()
            if post is not None:
                question_action(post)
        # Invalid selection
        else:
            print_invalid_option(max_option=2)


def post_question():
    """Allows user to post a question by inputting the required fields

    Returns:
    """
    print("Post Question")
    while (True):
        title_text = input("Enter title: ")
        to_return = keyword_input_validate(title_text)
        if to_return:
            return
        if title_text.strip() == "":
            print("\nTitle cannot be empty, please try again.")
            continue
        break

    body_text = input("Enter body: ")
    to_return = keyword_input_validate(body_text)
    if to_return:
        return

    print("Enter tags seperated by comma: ")
    tags_text = request_input()
    if tags_text[0] == "/back":
        return

    post_success = db.post_question(title_text, body_text, uid, tags_text)
    if post_success:
        print("Question successfully posted")
    else:
        print("Question failed to post")


def search_select_questions():
    """Allows user to search for questions and select one of the results

    Returns:
        post_row: Row entry of the
            selected post, or None if user exits.
    """
    # Search posts
    while (True):
        print("Enter keywords separated by a comma:")
        keywords = request_input()
        if keywords[0] == "/back":
            return None

        results = db.search_posts(keywords)
        if len(results) > 0:
            break
        print("No results found for keywords:", str(keywords), "\n")
        continue

    # List results
    print("Showing results for keywords", str(keywords))
    print("Enter the index of the post to excute an action on that post:")
    min_i, max_i = get_indices_range(results=results)
    print("")
    print_search_results(results, min_i, max_i)

    # Select posts
    while (True):
        action = request_input()[0]

        if action == "more":
            if len(results) <= max_i:
                print("No more results are available")
                continue

            # Increment the min and max
            min_i, max_i = get_indices_range(
                results=results,
                old_min=min_i,
                old_max=max_i
            )
            print_search_results(results, min_i, max_i)
        elif action == "/back":
            return None
        elif is_index(action, results):
            # Note: User input index starts at 1
            return results[int(action) - 1]
        else:
            print_invalid_option(max_option=len(results))


def print_search_results(results, min_i, max_i):
    """Prints the formatted results from a search of posts

    Args:
        results ([results row]): The list of search result rows
        min_i (int): The minimum index of the printed results range (inclusive)
        max_i (int): The maximum index of the printed results range (exclusive)
    """
    #TODO: Impelement
    print("These are the results...")
    print(results)


def question_action(post):
    """The execution loop of a user to take post actions on selected post

    Args:
        post (post_row): The post on which post_actions are being executed
    Returns:
        (bool): True if the user chooses to logout, None otherwise
    """
    db.increment_question_view_count(post)
    #TODO: Need to print all post details here

    # Setup post action options
    pa_actions = ["Answer question", "See answers",
                  "Vote"]

    while(True):
        print_options(pa_actions)
        action = request_input()[0]

        logout = None
        if action == "/back":
            return
        # Post action-answer
        elif (action == "1"):
            post_answer(post)
        # Post action-see answers
        elif (action == "3"):
            see_question_answers(post)
        # Post action-vote
        elif (action == "3"):
            post_vote(post)
        # Invalid selection
        else:
            print_invalid_option()
        print("")


def post_answer(post):
    #TODO:
    pass


def see_question_answers(post):
    #TODO:
    pass


def post_vote(post):
    #TODO:
    pass
