# CMPUT 291 Mini Project 2
Group Members:

- Mitchell Adam - `mbadam`
- Nayan Prakash - `nayan`
- Eric Claerhout - `claerhou`

## System Overview
The system was implemented in Python and uses a CLI interface for user interaction.

General, high-level flow:
```
For Phase 1:

For Phase 2:
```

### User Guide
#### For Phase 1:
1. Initialize the database with `python3 phase1.py $PORT` where $PORT is the port number on which MongoDB is running
2. This will read the Posts.json, Tags.json, and Votes.json files listed under the json/ directory and populate the MongoDB database `291db`
#### For Phase 2:
1. After Phase 1 has completed, Run phase 2 with `python3 phase2.py $PORT $UID` where $PORT is the port number on which MongoDB is running and $UID is an optional parameter to specify the User Id which is logging into the system
2. From here, the program will prompt the user for input, allowing the user to execute the desired functionality of the program. Any changes made to the database through the program will be reflected in the `291db` Mongo database
3. At any point in the program's execution where input is requested, `/exit` can be used to quit the program and `/back` can be used to return to the previous menu.

## Software Design
#### For Phase 1:

#### For Phase 2:
`phase1.py` handles the CLI arguments and has only three responsibilities: Initialize the database connection (via `database.py`), display statistics about the current user if a UID is provided, and pass the user information to the main execution loop of `logged_in.py`.

`logged_in.py` contains the code for the main execution loop of the program. `logged_in()` is the highest level function that prompts the user to either post a question or search for a question and calls their respective subfunctions (`post_question()` and `search_select_questions()`). After a question is posted, the user is returned to this top-level menu, but after a successful search and selection, the selected question pid is passed to the `question_action()` function. This function allows the user to select question-actions, namely, answering the selected question, listing all the answers of the selected question and selecting one of the answers, and voting on the question. Each of these question-actions also have their own subfunctions. The subfunction for listing and selecting answers, `see_question_answers()`, passes the selection answer pid to `answer_action()` which allows users to vote on the selected answer. This nesting subfunction structure follows what would be expected from a menu structure for this program, and thus it facilitates allowing the code to move back up the menu tree. Each of the subfunctions within `logged_in.py` interact with the database through related functions within `database.py`.

`database.py` is somewhat standalone in contrast. It contains and abstracts away all of the MongoDB interaction code, and is thus referenced at all levels of the program. For the most part, the functions defined in this file have equivalents in `logged_in.py`; While those handle user input, errors, printing, and the navigation structure, the equivalents in `database.py` contain strictly the MongoDB calls, with some of the error handling being passed back up to the calling function.

`utils.py` is the only other python file, and contains helper utility functions. These functions are used for tasks such as input parsing, error messaging and print formatting. This allows easy reuse of common functionality, keeping other files clean. 

## Testing Strategy
> General strategy discussion, coverage

## Group Work Strategy
> Strategy overview,

### Member estimates and tasks
The full commit log can be viewed [here](https://github.com/imswebra/cmput291MP2/commits/master).

#### Mitchell

Time Estimate:

Tasks:

- Example task, delete me

#### Nayan

Time Estimate:

Tasks:

- implement database functionality including:
    - get_user_statistics()
    - get_answers_to_question()
    - increment_question_view_count()
    - post_answer()
    - search_questions()
    - post_vote()

#### Eric

Time Estimate:

Tasks:

- Example task, delete me
