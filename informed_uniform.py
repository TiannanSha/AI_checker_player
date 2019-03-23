from action import *
from heuristic import *
from heapq import *


class HeapNode:

    def __init__(self, board, h, g, parent, action):
        self.board = board
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.par = parent
        self.act = action

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f


class InformedUniform:

    @staticmethod
    def start(root, debug=False):
        # Init IU
        iu = InformedUniform(Heuristic(root))
        heappush(iu.heap, HeapNode(root, iu.heuristic(root), 0, None, None))

        # Main Loop
        n = None
        while len(iu.heap):
            n = heappop(iu.heap)
            if iu.add_children(n):
                break

        # Extract path
        path = []
        while n.par is not None:
            path.append(n.act)
            n = n.par

        if debug:
            print("# DEBUG [Length: Exp|Gen] {}: {}|{}".format(len(path), iu.expanded, iu.generated))
            print("# DEBUG [HeapSize] {}".format(len(iu.heap)))

        return reversed(path)

    def __init__(self, heuristic):
        self.history = set()
        self.heap = []
        self.heuristic = heuristic
        self.generated = 0  # DEBUG
        self.expanded = 0  # DEBUG

    def add_children(self, node):
        board = node.board

        # Goal Reached
        h = self.heuristic(board)
        if h == 0:
            return True

        # Track boards gone through in this branch
        self.history.add(tuple(sorted(board.pieces, key=lambda x: (x is None, x))))

        # Get actions
        action_list = []
        for pos in board.get_locations():
            if pos is not None:
                action_list += Action.actions(board, pos)

        # Generate child for all actions
        self.expanded += 1  # DEBUG
        for action in action_list:
            child = action.apply_to(board)

            # Check if node already generated
            if tuple(sorted(child.pieces, key=lambda x: (x is None, x))) in self.history:
                continue

            self.generated += 1  # DEBUG
            heappush(self.heap, HeapNode(child, self.heuristic(child), node.g+1, node, action))
