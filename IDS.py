from action import *
from heuristic import *


class IterDepthSearch:

    @staticmethod
    def start(root):
        ids = IterDepthSearch(Heuristic(root))

        ids.new_depth = ids.heuristic(root)

        path = []
        while not path:
            ids.iter_depth = ids.new_depth
            ids.new_depth = float("inf")
            path = ids.recurse(root, 0, [0]*len(root.get_locations()))
            print("# DEBUG [Current Depth: Expanded] ", ids.iter_depth, ":", ids.expanded)  # DEBUG

        return path

    def __init__(self, heuristic):
        self.heuristic = heuristic
        self.iter_depth = 0
        self.new_depth = float("inf")
        self.expanded = 0  # DEBUG

    def recurse(self, node, depth, piece_states):
        self.expanded += 1  # DEBUG
        h = self.heuristic(node)

        if h == 0:
            return []

        if h+depth > self.iter_depth:
            self.new_depth = min(self.new_depth, h+depth)
            return None

        action_list = []
        for ind, piece in enumerate(node.get_locations()):
            if piece_states[ind] != 2 and piece is not None:
                action_list += Action.actions(node, piece)

        for action in action_list:
            child = action.apply_to(node)

            next_states = [s for s in piece_states]
            if action.type == MoveType.JUMP and action.jumped_index(node) is not None:
                next_states[action.jumped_index(node)] = 0
                next_states[action.piece_index] = 0
            else:
                for i in range(len(piece_states)):
                    if next_states[i] == 1:
                        next_states[i] = 2
                next_states[action.piece_index] = 1

            path = self.recurse(child, depth+1, next_states)
            if path is not None:
                path.append(action)
                return path
