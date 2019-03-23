from board import *


class Heuristic:

    def __init__(self, board):
        """
        Returns a field where each cell represents the minimum amount of moves
        required for a piece on that cell to exit the board, by assuming it can
        jump over empty cells (a piece might move there)
        """
        self.map = Field()

        # Flood fill backwards from exit_cells (Which have known heuristic of 1)
        flood_list = [(qr, 1) for qr in board.exit_cells]
        while flood_list:
            (top, dist) = flood_list.pop(0)

            # Don't put values in cells with blocks or reassign values to cells already given
            if self.map[top] is not None or board[top] == Piece.BLOCK:
                continue

            # Assign heuristic
            self.map[top] = dist

            # Add all directions from cell to fill
            for d in Field.DIRS:
                for m in [1, 2]:  # Moves/Jumps
                    pos = (top[0] + m*d[0], top[1] + m*d[1])
                    if not Field.is_on(pos):
                        continue
                    flood_list.append((pos, dist+1))

    def __call__(self, board):
        """returns the heuristic which is the sum of individual heuristic of all pieces"""
        return sum([self.map[loc] for loc in board.get_locations() if loc is not None])
