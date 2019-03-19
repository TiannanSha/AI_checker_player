from enum import Enum
from field import *


class Piece(Enum):
    BLOCK = 0
    RED = 1
    GREEN = 2
    BLUE = 3


class Board(Field):

    @staticmethod
    def from_json(data):
        board = Board()

        board.colour = {'red': Piece.RED, 'green': Piece.GREEN, 'blue': Piece.BLUE}[data['colour']]
        board.exit_cells = {Piece.RED: [(3, -3), (3, -2), (3, -1), (3, 0)],
                            Piece.GREEN: [(-3, 3), (-2, 3), (-1, 3), (0, 3)],
                            Piece.BLUE: [(-3, 0), (-2, -1), (-1, -2), (0, -3)]}[board.colour]

        for piece in data['pieces']:
            board[tuple(piece)] = board.colour

        for block in data['blocks']:
            board[tuple(block)] = Piece.BLOCK

        return board

    def __init__(self, board=None):
        super().__init__(board)
        if board is not None:
            self.colour = board.colour
            self.exit_cells = board.exit_cells

    def get_locations(self, ptype):
        return [(q, r) for q in Field.RAN for r in Field.RAN if -q-r in Field.RAN and self[(q, r)] == ptype]
