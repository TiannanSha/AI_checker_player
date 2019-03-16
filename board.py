from enum import Enum


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

        colour = {'red': Piece.RED, 'blue': Piece.BLUE, 'green': Piece.GREEN}[data['colour']]
        for piece in data['pieces']:
            board[tuple(piece)] = colour

        for block in data['blocks']:
            board[tuple(block)] = Piece.BLOCK

        return board

    def __init__(self, board=None):
        if board is None:
            self.cells = [[Piece.EMPTY for _i in range(Board.SIZE*2 + 1)] for _j in range(Board.SIZE*2 + 1)]
        else:
            self.cells = board.cells.deepcopy()

    def __getitem__(self, item):
        if type(item) != tuple or len(item) != 2:
            raise KeyError("Function requires 2-tuple")

        if -item[0]-item[1] not in Board.RAN:
            raise IndexError("Location not on board")

        return self.cells[item[0] + Board.SIZE][item[1] + Board.SIZE]

    def __setitem__(self, item, value):
        if type(item) != tuple or len(item) != 2:
            raise KeyError("Function requires 2-tuple")

        if -item[0]-item[1] not in Board.RAN:
            raise IndexError("Location not on board")

        self.cells[item[0] + Board.SIZE][item[1] + Board.SIZE] = value

    def apply(self, action):
        # No safety checks!!!
        if action.to_loc is not None:
            self[action.to_loc] = self[action.from_loc]

        self[(action.from_loc)] = Piece.EMPTY

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
