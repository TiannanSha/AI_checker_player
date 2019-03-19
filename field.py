from copy import deepcopy


class Field:
    SIZE = 3  # Count tiles out from the centre (ignoring the centre itself)
    RAN = range(-SIZE, +SIZE+1)
    DIRS = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]

    @staticmethod
    def is_on(loc):
        if type(loc) != tuple or len(loc) != 2:
            raise KeyError("Function requires 2-tuple")

        return loc[0] in Field.RAN and loc[1] in Field.RAN and -loc[0]-loc[1] in Field.RAN

    def __init__(self, field=None):
        if field is None:
            self.cells = [[None for _i in range(Field.SIZE*2 + 1)] for _j in range(Field.SIZE*2 + 1)]
        else:
            self.cells = deepcopy(field.cells)

    def __getitem__(self, item):
        if not Field.is_on(item):
            raise IndexError("Location not on board")

        return self.cells[item[0] + Field.SIZE][item[1] + Field.SIZE]

    def __setitem__(self, item, value):
        if not Field.is_on(item):
            raise IndexError("Location not on board")

        self.cells[item[0] + Field.SIZE][item[1] + Field.SIZE] = value

    def print(self, message="", debug=False, **kwargs):
        """
        Helper function to print a drawing of a hexagonal board's contents.

        Arguments:

        * `board_dict` -- dictionary with tuples for keys and anything printable
        for values. The tuple keys are interpreted as hexagonal coordinates (using
        the axial coordinate system outlined in the project specification) and the
        values are formatted as strings and placed in the drawing at the corres-
        ponding location (only the first 5 characters of each string are used, to
        keep the drawings small). Coordinates with missing values are left blank.

        Keyword arguments:

        * `message` -- an optional message to include on the first line of the
        drawing (above the board) -- default `""` (resulting in a blank message).
        * `debug` -- for a larger board drawing that includes the coordinates
        inside each hex, set this to `True` -- default `False`.
        * Or, any other keyword arguments! They will be forwarded to `print()`.
        """

        # Set up the board template:
        if not debug:
            # Use the normal board template (smaller, not showing coordinates)
            col_list = ["W", "R", "G", "B"]
            template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
        else:
            # Use the debug board template (larger, showing coordinates)
            col_list = ["BLOCK", "RED", "GREEN", "BLUE"]
            template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

        # prepare the provided board contents as strings, formatted to size.
        cells = []
        for qr in [(q, r) for q in Field.RAN for r in Field.RAN if -q - r in Field.RAN]:
            if type(self[qr]) == int:
                cell = str(self[qr]).center(5)
            elif self[qr] is not None:
                cell = str(col_list[self[qr].value]).center(5)
            else:
                cell = "".center(5)

            cells.append(cell)

        # fill in the template to create the board drawing, then print!
        board = template.format(message, *cells)
        print(board, **kwargs)
