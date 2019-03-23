"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors:
"""

import time
import sys
import json
# from IDS import *
from informed_uniform import *


def main():
    debug = True
    st = time.time()

    # Read JSON from file and interpret data
    with open(sys.argv[1]) as file:
        data = json.load(file)
    board = Board.from_json(data)

    # Find and print path
    path = InformedUniform.start(board, debug=debug)

    if debug:
        board.print("START".center(43))
    for action in path:
        print(action)
        if debug:
            board = action.apply_to(board)
            board.print("DEBUG".center(43))

    if debug:
        print("# TIME: %.4f" % (time.time() - st))


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
