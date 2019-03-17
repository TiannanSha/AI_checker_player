"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
"""

import sys
import json


from action import *


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: Search for and output winning sequence of moves
    # ...

    # $$Just Testing Stuff$$
    board = Board.from_json(data)
    board.print()

    actions = Action.get_action_list(board)
    for action in actions:
        print(action)
    # $$$$$


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
