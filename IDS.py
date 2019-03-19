from action import *
from heuristic import *


class IterDepthSearch:

    @staticmethod
    def search(root):
        ids = IterDepthSearch(root, Heuristic(root))
        return ids.start()

    def __init__(self, root, heuristic):
        self.root = root
        self.heuristic = heuristic
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
