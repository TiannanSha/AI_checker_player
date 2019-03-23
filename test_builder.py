def run(field, file_name=None):
    print(field)

    line_field = field.replace(" ", "").replace("\n", "")
    print(line_field + "\n")

    ran = range(-3, 4)
    lookup = [[q, r] for r in ran for q in ran if -q-r in ran]

    blocks = []
    pieces = []
    colour = ""
    for ind, val in enumerate(line_field):
        if val == "-":
            continue
        elif val == "X":
            blocks.append(lookup[ind])
        elif val in "RGB":
            pieces.append(lookup[ind])
            colour = {"R": "red", "G": "green", "B": "blue"}[val]

    output = "\n".join(['{',
                        '\t"colour": "{}",'.format(colour),
                        '\t"pieces": {},'.format(str(pieces).replace(" ", "")),
                        '\t"blocks": {}'.format(str(blocks).replace(" ", "")),
                        '}'])

    print(output)
    if file_name is not None:
        with open(file_name, "w") as f:
            f.write(output)


if __name__ == "__main__":
    # MODIFY THIS
    # - is Empty, X is Block, R G B are the Pieces respectively
    board = """
       - - - -
      - - - - -
     - - - - - -
    - - - - - - -
     - - - - - -
      - - - - -
       - - - -
    """

    run(board, None)
