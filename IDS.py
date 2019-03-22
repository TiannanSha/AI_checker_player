from action import *
from heuristic import *


class States(Enum):
    STILL = 0
    MOVING = 1
    STOPPED = 2


class IterDeepSearch:

    @staticmethod
    def start(root):
        ids = IterDeepSearch(Heuristic(root))

        ids.iter_depth = ids.heuristic(root)

        found_path = False
        while not found_path:
            ids.path = [None] * ids.iter_depth
            ids.branch = [None] * ids.iter_depth
            piece_states = [States.STILL] * len(root.get_locations())

            found_path = ids.recurse(root, 0, piece_states)

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

        # Goal Reached
        if h == 0:
            return True

        # This path can't reach goal at current depth
        if h+depth > self.iter_depth:
            return False

        # Get actions for all non stopped pieces
        action_list = []
        for ind, pos in enumerate(node.get_locations()):
            if piece_states[ind] != States.STOPPED and pos is not None:
                action_list += Action.actions(node, pos)

        # Generate child for all actions
        for action in action_list:
            child = action.apply_to(node)

            # Skip children that are back tracking
            if child.pieces in (f.pieces for f in self.branch[0:depth]):
                continue

            # Track current actions taken and the boards they generate
            self.path[depth] = action
            self.branch[depth] = child

            # Keep track of piece states
            next_states = []
            for state in piece_states:
                # Set old moving piece to stopped
                if state == States.MOVING:
                    next_states.append(States.STOPPED)
                else:
                    next_states.append(state)
            # Set current moving piece
            next_states[action.piece_index] = States.MOVING

            # If it's a jumping action set the moving and jumped piece to still
            if action.jumped_index is not None:
                next_states[action.jumped_index] = States.STILL
                next_states[action.piece_index] = States.STILL

            if self.recurse(child, depth+1, next_states):
                return True
