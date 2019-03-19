from board import *


class Heuristic:

    def __init__(self, board):
        self.map = Field()

        flood_list = [(qr, 1) for qr in board.exit_cells]

        while flood_list:
            (top, dist) = flood_list.pop(0)

            if self.map[top] is not None or board[top] == Piece.BLOCK:
                continue

            self.map[top] = dist

            for d in Field.DIRS:
                for m in [1, 2]:
                    pos = (top[0] + m*d[0], top[1] + m*d[1])
                    if not Field.is_on(pos):
                        continue
                    if board[pos] != Piece.BLOCK:
                        flood_list.append((pos, dist+1))

        self.map.print("DEBUG [Heuristic Map]")

    def __call__(self, board):
        return sum([self.map[loc] for loc in board.get_locations(board.colour)])
