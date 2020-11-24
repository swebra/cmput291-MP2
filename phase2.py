from sys import argv, exit

import database as db
from logged_in import logged_in

if __name__ == '__main__':
    if (len(argv) <= 1 or len(argv) > 3):
        print("Database port argument expected and optional UID, received", len(argv) - 1)
        exit(1)

    try:
        port = int(argv[1])
    except ValueError as e:
        print("Invali port")
        exit(1)

    is_connected = db.connect(port)


    uid = None
    if (len(argv) > 2):
        uid = argv[2]
        #TODO: Show report based on UID


    while (is_connected):
        logged_in(uid)
