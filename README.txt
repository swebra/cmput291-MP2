CMPUT 291 Mini Project 2

Mitchell Adam - mbadam
Nayan Prakash - nayan
Eric Claerhout - claerhou

We did not collaborate with anyone

Source material:
No notable sources besides the Python 3.5.2 documentation

Instructions to install dependencies:
After activating a virtual environment, run `pip install -r requirements.txt`.
On the lab machine, a virtual environment can easily be created and activated
via virtualenvwrapper by running `mkvirtualenv --python=$(which python3)
[virtual env name]`. See the virtualenvwrapper docs for more details regarding
virtualenv management.
https://virtualenvwrapper.readthedocs.io/en/latest/

Instructions to run:
1. Initialize the database with `python3 phase1.py $PORT $DIR` where $PORT is
   the port number on which MongoDB is running and $DIR is an optional parameter
   to specify the directory to look for Posts.json, Tags.json and Votes.json.
   If $DIR is not specified, the current working directory will be used.
2. After Phase 1 has completed, run phase 2 can be ran with
   `python3 phase2.py $PORT $UID` where $PORT is the port number on which
   MongoDB is running and $UID is an optional parameter to specify the User Id
   which is logging into the system.

