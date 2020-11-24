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
    while (True):
        print("Enter keywords separated by a comma:")
        keywords = request_input()
        if keywords[0] == "/back":
            return None

        results = db.search_questions(keywords)
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


def question_action(post):
    """The execution loop of a user to take post actions on selected question

    Args:
        post (post_row): The post on which post_actions are being executed
    """
    db.increment_question_view_count(post)
    print_all_post_details(post)

    # Setup post action options
    pa_actions = ["Answer question", "See answers",
                  "Vote"]

    while(True):
        print_options(pa_actions)
        action = request_input()[0]

        if action == "/back":
            return
        # Post action-answer
        elif (action == "1"):
            post_answer(post)
        # Post action-see answers
        elif (action == "2"):
            answer = see_question_answers(post)
            if answer is not None:
                answer_action(answer)
        # Post action-vote
        elif (action == "3"):
            post_vote(post)
        # Invalid selection
        else:
            print_invalid_option()
        print("")


def post_answer(post):
    """ Post an answer to a question

    Args:
        post (dict): Question to post an answer to

    """
    print("Enter the body of the answer:")
    body = request_input()[0]
    post_success = db.post_answer(post["Id"], body, uid)
    if post_success:
        print("Answer successfully posted")
    else:
        print("Answer failed to post")


def see_question_answers(post):
    """Get and view answers to given question

    Args:
        post (dict): Post to view answers on
    """

    results = db.get_answers_to_question(post)

    print("Showing answers to post",)
    print("Enter the index of the post to excute an action on that post:")
    min_i, max_i = get_indices_range(results=results)
    print("")
    print_search_results(results, min_i, max_i, answer=True)

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
            print_search_results(results, min_i, max_i, answer=True)
        elif action == "/back":
            return None
        elif is_index(action, results):
            # Note: User input index starts at 1
            return results[int(action) - 1]
        else:
            print_invalid_option(max_option=len(results))


def answer_action(post):
    """The execution loop of a user to take answer actions on selected post

    Args:
        post (post_row): The post on which post_actions are being executed
    """

    # Setup post action options
    pa_actions = ["Vote"]

    while(True):
        print_options(pa_actions)
        action = request_input()[0]

        if action == "/back":
            return
        # Post action-vote
        elif (action == "1"):
            post_vote(post)
            return
        # Invalid selection
        else:
            print_invalid_option()
        print("")


def post_vote(post):
    """ Add a vote to a post

    Args:
        post (dict): Post to vote on
    """
    vote_success = db.post_vote(post["Id"], uid)
    if vote_success:
        print("Vote successfully posted")
    else:
        print("Vote failed to post")


def print_search_results(results, min_i, max_i, answer=False):
    """Prints the formatted results from a search of posts

    Args:
        results ([results row]): The list of search result rows
        min_i (int): The minimum index of the printed results range (inclusive)
        max_i (int): The maximum index of the printed results range (exclusive)
        answer(bool): Whether the results are answers or not
    """

    # Get table
    if answer:
        max_widths = {0: 80}  # body (index 0) before index
        header = ["Index", "Body", "CreationDate", "Score"]
    else:
        max_widths = {1: 30}  # title (index 2) before index
        header = ["Index", "Title", "CreationDate", "Score", "AnswerCount"]

    table, widths = get_table_info(results[min_i:max_i], header,
                                   trunc_widths=max_widths,
                                   index_start=min_i + 1, # Start indices at 1
                                   answer=answer)

    # Generate width string
    # Right-aligned index * len(header)
    width_str ="{{:{}}}  " * len(header)
    width_str = width_str.format(*widths)

    # Print the table
    print_table(table, width_str, widths)
    print("")


def print_all_post_details(post):
    """Prints the details of a post

    Args:
        post (dict): The post to be printed
    """

    print("Selected post details:")
    for k in post.keys():
        print("-----------------------")
        print(k, ": ", post[k])
    print("-----------------------")
    print("")
