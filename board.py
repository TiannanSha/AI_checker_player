from enum import Enum


class Piece(Enum):
    EMPTY = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    BLOCK = 4


class Board:
    size = 3  # Count tiles out from the centre (ignoring the centre itself)
    ran = range(-size, +size+1)

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
            self.cells = [[Piece.EMPTY for _i in range(Board.size*2 + 1)] for _j in range(Board.size*2 + 1)]
        else:
            self.cells = board.cells.deepcopy()

    def __getitem__(self, item):
        if type(item) != tuple or len(item) != 2:
            raise KeyError("Function requires 2-tuple")

        if -item[0]-item[1] not in Board.ran:
            raise IndexError("Location not on board")

        return self.cells[item[0] + Board.size][item[1] + Board.size]

    def __setitem__(self, item, value):
        if type(item) != tuple or len(item) != 2:
            raise KeyError("Function requires 2-tuple")

        if -item[0]-item[1] not in Board.ran:
            raise IndexError("Location not on board")

        self.cells[item[0] + Board.size][item[1] + Board.size] = value

    def get_dict(self, full=False):
        if full:
            col_list = ["", "RED", "GREEN", "BLUE", "BLOCK"]
        else:
            col_list = ["", "R", "G", "B", "W"]

        board_dict = {}

        for qr in [(q, r) for q in Board.ran for r in Board.ran if -q-r in Board.ran]:
            if self[qr] != Piece.EMPTY:
                board_dict[qr] = col_list[self[qr].value]

        return board_dict
