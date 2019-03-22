"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors:
"""

import sys
import json


from IDS import *


def main():
    # Read JSON from file
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # Get board from JSON data
    board = Board.from_json(data)

    # Find path
    path = IterDeepSearch.start(board)

    # Print FULL
    board.print("START")
    for action in path:
        board = action.apply_to(board)
        print(action)
        board.print()


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
