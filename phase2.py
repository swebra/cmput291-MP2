from sys import argv, exit

import database as db
from logged_in import logged_in
from utils import print_user_statistics

if __name__ == '__main__':
    if (len(argv) <= 1 or len(argv) > 3):
        print("Database port argument expected and optional UID, received", len(argv) - 1)
        exit(1)

    try:
        port = int(argv[1])
    except ValueError as e:
        print("Invalid port")
        exit(1)

    is_connected = db.connect(port)


    uid = None
    if (len(argv) > 2) and is_connected:
        uid = argv[2]
        statistics = db.get_user_statistics(uid)
        if statistics is not None:
            print_user_statistics(statistics)
        else:
            print("No statistics found for uid", argv[2])

        print("")


    while (is_connected):
        logged_in(uid)
