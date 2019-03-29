from enum import Enum
from field import *


class Piece(Enum):
    BLOCK = 0
    RED = 1
    GREEN = 2
    BLUE = 3


class Board:

    @staticmethod
    def from_json(data):
        board = Board()

        board.colour = {'red': Piece.RED, 'green': Piece.GREEN, 'blue': Piece.BLUE}[data['colour']]
        board.exit_cells = tuple({Piece.RED: [(3, -3), (3, -2), (3, -1), (3, 0)],
                                  Piece.GREEN: [(-3, 3), (-2, 3), (-1, 3), (0, 3)],
                                  Piece.BLUE: [(-3, 0), (-2, -1), (-1, -2), (0, -3)]}[board.colour])

        board.pieces = tuple((tuple(piece) for piece in data['pieces']))
        board.blocks = tuple((tuple(block) for block in data['blocks']))

        return board

    def __init__(self, board=None):
        # Copy board properties if given
        if board is not None:
            self.colour = board.colour
            self.exit_cells = board.exit_cells
            self.pieces = board.pieces
            self.blocks = board.blocks

    def __getitem__(self, item):
        """Returns cell value at (q, r)"""
        if not Field.is_on(item):
            raise IndexError("Location not on board")

        if item in self.pieces:
            return self.colour
        elif item in self.blocks:
            return Piece.BLOCK
        return None

    def move(self, index, to_loc):
        new_board = Board(self)
        new_board.pieces = self.pieces[:index] + (to_loc,) + self.pieces[index+1:]
        return new_board
