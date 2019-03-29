from action import *
from heuristic import *
from heapq import *


class InformedUniformAlt:

    @staticmethod
    def start(root, debug=False):
        # Init IU
        iu = InformedUniformAlt(Heuristic(root))
        if debug:
            Field.print(iu.heuristic.map, "DEBUG [Heuristic Map]")
            Field.print(iu.heuristic.over_map, "DEBUG [Over Heuristic]")

        # Main Loop
        node = None
        heappush(iu.heap, iu.node_tuple(root, 0, None, None))
        while len(iu.heap):
            node = heappop(iu.heap)
            if iu.add_children(node):
                break

        # Extract path
        path = []
        par, act = node[4:6]
        while par is not None:
            path.append(act)
            par, act = iu.history[par]

        if debug:
            print("# DEBUG [Length: Exp|Gen] {}: {}|{}".format(len(path), iu.expanded, iu.generated))

        return reversed(path)

    def __init__(self, heuristic):
        self.history = {}
        self.heap = []
        self.heuristic = heuristic
        self.generated = 0
        self.expanded = 0

    def add_children(self, node):
        _f, _o, _g, depth, parent, action, board = node
        board_id = frozenset(board.pieces)

        # Goal Reached
        h = self.heuristic(board)
        if h == 0:
            return True

        # Check if node already expanded
        if board_id in self.history:
            return False

        # Track boards expanded
        self.expanded += 1
        self.history[board_id] = (parent, action)

        # Get actions
        action_list = []
        for pos in board.pieces:
            if pos is not None:
                action_list += Action.actions(board, pos)

        # Generate child for all actions
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
            heappush(self.heap, self.node_tuple(child, depth+1, board_id, action))

    def node_tuple(self, board, g, par, act):
        f = self.heuristic(board) + g
        over_h = self.heuristic.over_estimate(board)
        return f, over_h, -self.generated, g, par, act, board
