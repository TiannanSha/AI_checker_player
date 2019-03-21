from action import *
from heuristic import *


class IterDepthSearch:

    @staticmethod
    def start(root):
        ids = IterDepthSearch(Heuristic(root))

        ids.iter_depth = ids.heuristic(root)

        found_path = False
        while not found_path:
            ids.path = [None] * ids.iter_depth
            ids.branch = [None] * ids.iter_depth
            found_path = ids.recurse(root, 0, [0]*len(root.get_locations()))
            print("# DEBUG [Current Depth: Expanded] ", ids.iter_depth, ":", ids.expanded)  # DEBUG
            ids.iter_depth += 1

        return ids.path

    def __init__(self, heuristic):
        self.branch = []
        self.path = []
        self.heuristic = heuristic
        self.iter_depth = 0
        self.expanded = 0  # DEBUG

    def recurse(self, node, depth, piece_states):
        self.expanded += 1  # DEBUG
        h = self.heuristic(node)

        if h == 0:
            return True

        if h+depth > self.iter_depth:
            return False

        action_list = []
        for ind, piece in enumerate(node.get_locations()):
            if piece_states[ind] != 2 and piece is not None:
                action_list += Action.actions(node, piece)

        for action in action_list:
            child = action.apply_to(node)

            if child.cells in [f.cells for f in self.branch[0:depth]]:
                continue

            self.path[depth] = action
            self.branch[depth] = child

            next_states = piece_states.copy()
            for i in range(len(piece_states)):
                if next_states[i] == 1:
                    next_states[i] = 2
            next_states[action.piece_index] = 1

            if action.type == MoveType.JUMP and action.jumped_index(node) is not None:
                next_states[action.jumped_index(node)] = 0
                next_states[action.piece_index] = 0

            if self.recurse(child, depth+1, next_states):
                return True
