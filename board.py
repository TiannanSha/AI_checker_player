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

        board.pieces = []
        for piece in data['pieces']:
            board[tuple(piece)] = board.colour
            board.pieces.append(tuple(piece))

        for block in data['blocks']:
            board[tuple(block)] = Piece.BLOCK

        return board

    def __init__(self, board=None):
        # Copy board properties if given
        super().__init__(board)
        if board is not None:
            self.colour = board.colour
            self.exit_cells = board.exit_cells
            self.pieces = board.pieces.copy()

    def get_locations(self):
        # Return location of pieces
        return self.pieces.copy()
