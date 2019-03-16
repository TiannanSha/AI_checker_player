from enum import Enum


class MoveType(Enum):
    MOVE = 0
    JUMP = 1
    EXIT = 2


class Action:

    def __init__(self, from_loc, to_loc=None):
        self.from_loc = from_loc
        self.to_loc = to_loc
        self.type = None

        if to_loc is None:
            self.type = MoveType.EXIT
        elif abs(from_loc[0] - to_loc[0]) == 1 or abs(from_loc[1] - to_loc[1]):
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