from enum import Enum
from copy import deepcopy


class Piece(Enum):
    EMPTY = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    BLOCK = 4


class Board:
    SIZE = 3  # Count tiles out from the centre (ignoring the centre itself)
    RAN = range(-SIZE, +SIZE+1)

    @staticmethod
    def from_json(data):
        board = Board()

        colour = {'red': Piece.RED, 'green': Piece.GREEN, 'blue': Piece.BLUE}[data['colour']]
        for piece in data['pieces']:
            board[tuple(piece)] = colour

        for block in data['blocks']:
            board[tuple(block)] = Piece.BLOCK

        return board

    def __init__(self, board=None):
        if board is None:
            self.cells = [[Piece.EMPTY for _i in range(Board.SIZE*2 + 1)] for _j in range(Board.SIZE*2 + 1)]
        else:
            self.cells = deepcopy(board.cells)

    def __getitem__(self, item):
        if not Board.on_board(item):
            raise IndexError("Location not on board")

        return self.cells[item[0] + Board.SIZE][item[1] + Board.SIZE]

    def __setitem__(self, item, value):
        if not Board.on_board(item):
            raise IndexError("Location not on board")

        self.cells[item[0] + Board.SIZE][item[1] + Board.SIZE] = value

    @staticmethod
    def on_board(loc):
        if type(loc) != tuple or len(loc) != 2:
            raise KeyError("Function requires 2-tuple")

        return loc[0] in Board.RAN and loc[1] in Board.RAN and -loc[0]-loc[1] in Board.RAN

    def get_dict(self, full=False):
        if full:
            col_list = ["", "RED", "GREEN", "BLUE", "BLOCK"]
        else:
            col_list = ["", "R", "G", "B", "W"]

        board_dict = {}

        for qr in [(q, r) for q in Board.RAN for r in Board.RAN if -q-r in Board.RAN]:
            if self[qr] != Piece.EMPTY:
                board_dict[qr] = col_list[self[qr].value]

        return board_dict
