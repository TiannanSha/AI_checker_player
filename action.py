from board import *


class MoveType(Enum):
    MOVE = 0
    JUMP = 1
    EXIT = 2


class Action:

    @staticmethod
    def get_action_list(board):
        actions = []
        for piece in board.get_locations(board.colour):
            # Exits
            if piece in board.exit_cells:
                actions.append(Action(piece))

            for d in Field.DIRS:
                # Moves
                pos = (piece[0] + d[0], piece[1] + d[1])
                if not Board.is_on(pos):
                    continue
                if board[pos] is None:
                    actions.append(Action(piece, pos))
                    continue

                # Jumps
                pos = (piece[0] + 2*d[0], piece[1] + 2*d[1])
                if not Board.is_on(pos):
                    continue
                if board[pos] is None:
                    actions.append(Action(piece, pos))
                    continue

        return actions

    def __init__(self, from_loc, to_loc=None):
        self.from_loc = from_loc
        self.to_loc = to_loc

        if to_loc is None:
            self.type = MoveType.EXIT
        elif abs(from_loc[0] - to_loc[0]) == 1 or abs(from_loc[1] - to_loc[1]) == 1:
            self.type = MoveType.MOVE
        else:
            self.type = MoveType.JUMP

    def __str__(self):
        if self.type == MoveType.MOVE:
            return "MOVE from {} to {}.".format(self.from_loc, self.to_loc)
        elif self.type == MoveType.JUMP:
            return "JUMP from {} to {}.".format(self.from_loc, self.to_loc)
        else:
            return "EXIT from {}.".format(self.from_loc)

    def apply_to(self, board):
        # Leaves the original board unmodified and returns a modified version after applying the action
        new_board = Board(board)

        if self.to_loc is not None:
            new_board[self.to_loc] = new_board[self.from_loc]
        new_board[self.from_loc] = None

        return new_board
