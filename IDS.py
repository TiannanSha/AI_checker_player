from action import *


class IterDepthSearch:

    def __init__(self, root, heur):
        self.heur = heur
        self.root = root
        self.iter_depth = None
        self.new_depth = None
        self.expanded = 0

    def start(self):
        self.new_depth = self.heur(self.root)

        path = []
        while not path:
            self.iter_depth = self.new_depth
            self.new_depth = None
            path = self.recurse(self.root, 0)
            # print(self.iter_depth, ": ", self.expanded)  # DEBUG

        return path

    def recurse(self, node, depth):
        self.expanded += 1
        h = self.heur(node)

        if h == 0:
            return []

        if depth == self.iter_depth:
            if self.new_depth is None or h+depth < self.new_depth:
                self.new_depth = h+depth
            return None

        for action in Action.get_action_list(node):
            child = action.apply_to(node)

            path = self.recurse(child, depth+1)
            if path is not None:
                path.append(action)
                return path
