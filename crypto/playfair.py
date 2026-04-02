from utils.alph import ALPH

def playfair(plain_text, key, encode=True):
    if not plain_text or not key:
        raise ValueError("Input text and key must be provided")
    
    key = key.upper().replace(" ", "").replace("W", "V")
    plain_text = plain_text.upper().replace(" ", "").replace("W", "V")

    diagram, processed_text, mapping = _prepare_input(plain_text, key)
    shift = 1 if encode else -1
    text = []

    for char1, char2 in processed_text:
        row_1, col_1 = mapping[char1]
        row_2, col_2 = mapping[char2]

        # Same row
        if row_1 == row_2:
            # Getting the new coordinates
            new_row_1, new_row_2 = row_1, row_2

            new_col_1 = (col_1 + shift) % 5
            new_col_2 = (col_2 + shift) % 5


        # Same Column
        elif col_1 == col_2:
            # Getting the new coordinates
            new_row_1 = (row_1 + shift) % 5
            new_row_2 = (row_2 + shift) % 5

            new_col_1, new_col_2 = col_1, col_2

        # Rectangel rule
        else:
            # Getting the new coordinates
            new_row_1, new_row_2 = row_1, row_2

            new_col_1, new_col_2 = col_2, col_1

        new_char_1 = diagram[new_row_1][new_col_1]
        new_char_2 = diagram[new_row_2][new_col_2]

        text.append(new_char_1)
        text.append(new_char_2)

    return "".join(text)

def _prepare_input(input_text, key):
    diagram = _build_diagram(key)
    if not diagram:
        raise ValueError(f"Something went wrong when building the Playfair diagram:\n{_display_grid(diagram)}")

    processed_text = _prepare_text(input_text)
    if not processed_text:
        raise ValueError(f"Something went wrong when preparing the text:\n{processed_text}")

    mapping = _build_mapping(diagram)
    if not mapping:
        raise ValueError("Something went wrong when mapping the Playfair grid")
    
    return diagram, processed_text, mapping

def _build_diagram(key):
    """
    Constructs a 5x5 Playfair cipher grid based on a keyword.
    Removes W
    """

    if not key:
        return None           

    alph = [char.upper() for char in ALPH.keys() if char.upper() != "W"]
    grid = []
    seen = set()

    # Process the key first, then the alphabet
    for char in (key + "".join(alph)):
        if char.isalpha() and char not in seen:
            seen.add(char)
            grid.append(char)

    # Partition the 25 letters into 5 rows of 5
    # Using list slicing: [0:5], [5:10], etc.
    grid = [grid[i: i + 5] for i in range(0, 25, 5)]

    return grid
    
def _prepare_text(text):
    """
    Prepares text for Playfair rules:
    - Uppercases and replaces W with V
    - Splits into digraphs (pairs)
    - Inserts 'X' between identical letters in a pair (e.g., 'HELLO' -> 'HE', 'LX', 'LO')
    - Pads with 'X' if the final length is odd
    """

    arr = []
    idx = 0

    while idx < len(text):
        c1 = text[idx]

        if idx + 1 < len(text):
            c2 = text[idx + 1]
            if c1 == c2:
                # Not allowing isentical letters
                filler = "Q" if c1 == "X" else "X"
                arr.append((c1, filler))
                idx += 1
            else:
                arr.append((c1, c2))
                idx += 2
        else:
            # Pad the end if there is a lone character
            filler = "Q" if c1 == "X" else "X"
            arr.append(c1, filler)
            idx += 1

    return arr

def _build_mapping(grid):
    """
    Returns a dict where keys are letters and values are (row, col) tuples.
    """

    mapping = dict()
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            mapping[char] = (r, c)
    return mapping

def _display_grid(grid):
    """
    Prints the grid in a readable 5x5 format.
    """

    for row in grid:
        print(" ".join(row))