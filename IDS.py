from action import *
from heuristic import *


class IterDepthSearch:

    @staticmethod
    def start(root):
        ids = IterDepthSearch(root, Heuristic(root))

        ids.new_depth = ids.heuristic(root)

        path = []
        while not path:
            ids.iter_depth = ids.new_depth
            ids.new_depth = float("inf")
            path = ids.recurse(root, 0)
            print("# DEBUG [Current Depth: Expanded] ", ids.iter_depth, ":", ids.expanded)  # DEBUG

        return path

    def __init__(self, root, heuristic):
        self.root = root
        self.heuristic = heuristic
        self.iter_depth = 0
        self.new_depth = float("inf")
        self.expanded = 0  # DEBUG

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
