from action import *
from heuristic import *


class States(Enum):
    STILL = 0
    MOVING = 1
    STOPPED = 2


class IterDeepSearch:

    @staticmethod
    def start(root, debug=False):
        # Init IDS
        ids = IterDeepSearch(Heuristic(root))
        if debug:
            ids.heuristic.map.print("DEBUG [Heuristic Map]")

        # Initial max depth set to heuristic of root
        ids.iter_depth = ids.heuristic(root)

        found_path = False
        while not found_path:
            # Clean variables to store path (actions and states)
            ids.path = [None] * ids.iter_depth
            ids.branch = [None] * ids.iter_depth

            # Clean variable used for branch culling
            piece_states = [States.STILL] * len(root.get_locations())

            # Search
            found_path = ids.recurse(root, 0, piece_states)

            if debug:
                print("# DEBUG [Depth: Exp/Gen] {}: {}/{}".format(ids.iter_depth, ids.expanded, ids.generated))

            # Increment max depth to search
            ids.iter_depth += 1

        return ids.path

    def __init__(self, heuristic):
        self.path = []  # Store actions
        self.branch = []  # Store states
        self.heuristic = heuristic  # Heuristic function
        self.iter_depth = 0  # Max depth to search
        self.generated = 0  # DEBUG
        self.expanded = 0  # DEBUG

    def recurse(self, node, depth, piece_states):
        self.generated += 1  # DEBUG

        h = self.heuristic(node)
        # Goal Reached
        if h == 0:
            return True
        # This path can't reach goal at current depth
        if h+depth > self.iter_depth:
            return False

        # Track boards gone through in this branch
        self.branch[depth] = node

        # Get actions for all non stopped pieces
        action_list = []
        for ind, pos in enumerate(node.get_locations()):
            if piece_states[ind] != States.STOPPED and pos is not None:
                action_list += Action.actions(node, pos)

        # Generate child for all actions
        self.expanded += 1  # DEBUG
        for action in action_list:
            child = action.apply_to(node)

            # Skip children that are back tracking
            if child.pieces in (f.pieces for f in self.branch[0:depth]):
                continue

            # Track current actions taken
            self.path[depth] = action

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

            # Recurse on child
            if self.recurse(child, depth+1, next_states):
                return True
