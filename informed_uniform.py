from action import *
from heuristic import *
from heapq import *


class HeapNode:

    def __init__(self, board, heuristic, depth, parent, action):
        self.board = board
        self.h = heuristic
        self.g = depth
        self.f = self.g + self.h(board)
        self.par = parent
        self.act = action

    def __lt__(self, other):
        if self.f == other.f:
            return self.h.over_estimate(self.board) < self.h.over_estimate(other.board)
        return self.f < other.f


class InformedUniform:

    @staticmethod
    def start(root, debug=False):
        # Init IU
        iu = InformedUniform(Heuristic(root))
        if debug:
            Field.print(iu.heuristic.map, "DEBUG [Heuristic Map]")
            Field.print(iu.heuristic.over_map, "DEBUG [Over Heuristic]")

        # Main Loop
        node = None
        heappush(iu.heap, HeapNode(root, iu.heuristic, 0, None, None))
        while len(iu.heap):
            node = heappop(iu.heap)
            if iu.add_children(node):
                break

        # Extract path
        path = []
        while node.par is not None:
            path.append(node.act)
            node = node.par

        if debug:
            print("# DEBUG [Length: Exp|Gen] {}: {}|{}".format(len(path), iu.expanded, iu.generated))

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

        if frozenset(board.pieces) in self.history:
            return False

        # Track boards gone through in this branch
        self.history.add(frozenset(board.pieces))

        # Get actions
        action_list = []
        for pos in board.pieces:
            if pos is not None:
                action_list += Action.actions(board, pos)

        # Generate child for all actions
        self.expanded += 1  # DEBUG
        for action in action_list:
            # Pieces never move backwards in optimal solutions
            if action.type != MoveType.EXIT:
                if self.heuristic.over_map[action.from_loc] < self.heuristic.over_map[action.to_loc]:
                    continue

            child = action.apply_to(board)
            # Check if node already generated
            if frozenset(child.pieces) in self.history:
                continue

            self.generated += 1  # DEBUG
            heappush(self.heap, HeapNode(child, self.heuristic, node.g+1, node, action))
