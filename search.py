"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors:
"""

import time
import sys
import json


from IDS import *


def main():
    DEBUG = True
    if DEBUG: st = time.time()

    # Read JSON from file and interpret data
    with open(sys.argv[1]) as file:
        data = json.load(file)
    board = Board.from_json(data)

    # Find and print path
    path = IterDeepSearch.start(board, debug=DEBUG)
    for action in path:
        print(action)

        if DEBUG: board = action.apply_to(board); board.print("DEBUG".center(43))

    if DEBUG: print("# TIME: %.4f" % (time.time() - st))


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
