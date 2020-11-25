# CMPUT 291 Mini Project 2
Group Members:

- Mitchell Adam - `mbadam`
- Nayan Prakash - `nayan`
- Eric Claerhout - `claerhou`

## System Overview
The system was implemented in Python and uses a CLI interface for user interaction.

### General, high-level flow:
#### For Phase 1:
```
1. phase1 -> phase1.insertJsonRowItems()
2. phase1.insertJsonRowItems() -> phase1.addTermList()
```
#### For Phase 2:
```
1. phase2 -> logged_in.logged_in()
2a. logged_in.logged_in() -> logged_in.post_question()
2b. logged_in.logged_in() <-> logged_in.search_select_posts()
    3. logged_in.logged_in() -> logged_in.question_action()
    4a. logged_in.question_action() -> logged_in.post_answer()
    4b. logged_in.question_action() -> logged_in.post_vote()
    4c. logged_in.question_action() <-> logged_in.see_question_answers()
        5. logged_in.question_action() -> logged_in.answer_action()
        6. logged_in.answer_action() -> logged_in.post_vote()
```

### User Guide
#### For Phase 1:
1. Initialize the database with `python3 phase1.py $PORT $DIR` where $PORT is the port number on which MongoDB is running and $DIR is the directory which contains Posts.json, Tags.json and Votes.json.
2. This will read the Posts.json, Tags.json, and Votes.json files listed under the $DIR directory and populate the MongoDB database `291db`.

#### For Phase 2:
1. After Phase 1 has completed, Run phase 2 with `python3 phase2.py $PORT $UID` where $PORT is the port number on which MongoDB is running and $UID is an optional parameter to specify the User Id which is logging into the system
2. From here, the program will prompt the user for input, allowing the user to execute the desired functionality of the program. Any changes made to the database through the program will be reflected in the `291db` Mongo database
3. At any point in the program's execution where input is requested, `/exit` can be used to quit the program and `/back` can be used to return to the previous menu.

## Software Design
#### For Phase 1:
`phase2.py` handles the CLI arguments and has the following responsibilities: Initialize the database connection (via `database.py`), read json entries from the Posts.json, Tags.json and Votes.json files within the provided directory and insert the documents into the `291db` database.

#### For Phase 2:
`phase1.py` handles the CLI arguments and has only three responsibilities: Initialize the database connection (via `database.py`), display statistics about the current user if a UID is provided, and pass the user information to the main execution loop of `logged_in.py`.

`logged_in.py` contains the code for the main execution loop of the program. `logged_in()` is the highest level function that prompts the user to either post a question or search for a question and calls their respective subfunctions (`post_question()` and `search_select_questions()`). After a question is posted, the user is returned to this top-level menu, but after a successful search and selection, the selected question pid is passed to the `question_action()` function. This function allows the user to select question-actions, namely, answering the selected question, listing all the answers of the selected question and selecting one of the answers, and voting on the question. Each of these question-actions also have their own subfunctions. The subfunction for listing and selecting answers, `see_question_answers()`, passes the selection answer pid to `answer_action()` which allows users to vote on the selected answer. This nesting subfunction structure follows what would be expected from a menu structure for this program, and thus it facilitates allowing the code to move back up the menu tree. Each of the subfunctions within `logged_in.py` interact with the database through related functions within `database.py`.

`database.py` is somewhat standalone in contrast. It contains and abstracts away all of the MongoDB interaction code, and is thus referenced at all levels of the program. For the most part, the functions defined in this file have equivalents in `logged_in.py`; While those handle user input, errors, printing, and the navigation structure, the equivalents in `database.py` contain strictly the MongoDB calls, with some of the error handling being passed back up to the calling function.

`utils.py` is the only other python file, and contains helper utility functions. These functions are used for tasks such as input parsing, error messaging and print formatting. This allows easy reuse of common functionality, keeping other files clean.

## Testing Strategy
Two primary testing strategies were employed. Firstly, manually testing was done of UI and functionality. Each requirements were tested by simulating the actions described on the rubric. Correctness was checked by
using the mongo terminal and ensuring that expected results were there. UI/control functionality was also tested during this time. Secondly, to test the speed, shell scripts were created to time performance, specifically in phase 1. From this, we were able to increase performance of phase 1 by analyzing the time increase/decrease of specific changes. We also manually tested the timing of actions, such as search to ensure they were "instant".

## Group Work Strategy
Our group began work on the project ~1 week before the deadline. At this time, each member of the team began to familiarize themselves with the project and began to understand what was required. Because this project was structurally similar to the Mini-Project 1, members already were fairly familiar with the requirements of the project. As members began to work, they would update the other members on what had been accomplished and what was the next item on the TODO list as well as any bugs or issues that they had encountered. Group members would consistently keep a tally of what work was completed and what work was still required to implement and group members were able to choose tasks to whittle down the necessary work.

As our group was not able to meet in person to work on this project, we had a group chat made to ensure constant communication between members. Members were able to keep each other up-to-date on what had been completed and what was still left to be done. Members were could also consult the group when they found a task to be difficult and needed assistance. This allowed members to work individually, but collaborate if needed. As well, it ensured that the program that was developed matched the requirements and expectations of each member.

In order to ensure all requirements were met, lists of tasks were made by directly consulting the requirements. This allowed us to stay organized and address the needed features of the projects. In order to not miss any clarifications, we also copied all the clarifications into our todo list so that we could change our previous work if needed and could easily see the clarifications for new work.

Overall, our group maintained good communication throughout the project with members volunteering on what aspects they wanted to work on. All members were eager to contribute and the dynamics of the team were positive.

### Member estimates and tasks
The full commit log can be viewed [here](https://github.com/imswebra/cmput291MP2/commits/master).

#### Mitchell

Time Estimate: 8 hours

Tasks:

- implement database functionality including:
    - connection
    - post question
- implement control of CLI
    - create function outlines
    - establish utility functions
    - implement doc strings
    - code cleanup
- testing
    - thoroughly test program according to rubric
    - identify key bugs
- additions to import

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
- Addition of docstrings to the implemented functions listed above
- Execution of manual testing
- Additions to report
- Various bug fixes across codebase
- Implemented several util functions

#### Eric

Time Estimate:

Tasks:

- Example task, delete me
