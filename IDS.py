from action import *


class IterDepthSearch:
    heur_map = None

    @staticmethod
    def search(root):
        ids = IterDepthSearch(root)
        ids.heur_map = IterDepthSearch.heur_make(root)
        return ids.start()

    @staticmethod
    def heur_make(board):
        dirs = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
        exit_cells = {Piece.RED: [(3, -3), (3, -2), (3, -1), (3, 0)],
                      Piece.GREEN: [(-3, 3), (-2, 3), (-1, 3), (0, 3)],
                      Piece.BLUE: [(-3, 0), (-2, -1), (-1, -2), (0, -3)]}[board.colour]

        hmap = Board()

        flood_list = [(qr, 1) for qr in exit_cells]

        while flood_list:
            (top, dist) = flood_list.pop(0)

            if hmap[top] is not Piece.EMPTY or board[top] == Piece.BLOCK:
                continue

            hmap[top] = dist

            for d in dirs:
                for m in [1, 2]:
                    pos = (top[0] + m*d[0], top[1] + m*d[1])
                    if not Board.on_board(pos):
                        continue
                    if board[pos] != Piece.BLOCK:
                        flood_list.append((pos, dist+1))

        hmap.print("DEBUG [Heuristic Map]")

        return hmap

    def heuristic(self, board):
        return sum([self.heur_map[loc] for loc in board.get_locations(board.colour)])

    def __init__(self, root):
        self.root = root
        self.iter_depth = 0
        self.new_depth = float("inf")
        self.expanded = 0  # DEBUG

    def start(self):
        self.new_depth = self.heuristic(self.root)

        path = []
        while not path:
            self.iter_depth = self.new_depth
            self.new_depth = float("inf")
            path = self.recurse(self.root, 0)
            print("# DEBUG [Current Depth: Expanded] ", self.iter_depth, ":", self.expanded)  # DEBUG

        return path

    def recurse(self, node, depth):
        self.expanded += 1  # DEBUG
        h = self.heuristic(node)

        if h == 0:
            return []

        if h+depth > self.iter_depth:
            self.new_depth = min(self.new_depth, h+depth)
            return None

        for action in Action.get_action_list(node):
            child = action.apply_to(node)

            path = self.recurse(child, depth+1)
            if path is not None:
                path.append(action)
                return path
