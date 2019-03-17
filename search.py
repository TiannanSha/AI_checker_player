"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
"""

import sys
import json


from IDS import *


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    board = Board.from_json(data)

    board.print("Starting Config")

    ids = IterDepthSearch(board, heuristic)
    path = ids.start()

    for action in reversed(path):
        print(action)


def heuristic(board):
    # TODO: greatly improve the heuristic
    if board.get_locations(board.colour):
        return 1
    return 0


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
