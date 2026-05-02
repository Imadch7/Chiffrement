from numpy import array
from string import ascii_uppercase as alph

def playfair_cipher(text: str, key: str, encode: bool):
    key = (key + alph).upper().replace("J", "I").replace(" ", "")
    unique_chars = list(dict.fromkeys([c for c in key if c.isalpha()]))
    diagram = array(unique_chars[:25]).reshape(5, 5)

    mapping = {char: (r, c) for r, row in enumerate(diagram) for c, char in enumerate(row)}

    text = text.upper().replace("J", "I").replace(" ", "")
    clean_text = "".join([c for c in text if c.isalpha()])

    pairs = []
    idx = 0
    while idx < len(clean_text):
        char_1 = clean_text[idx]
        if idx + 1 < len(clean_text):
            char_2 = clean_text[idx + 1]
            if char_1 == char_2:
                pairs.append((char_1, "X" if char_1 != "X" else "Q"))
                idx += 1
            else:
                pairs.append((char_1, char_2))
        else:
            pairs.append((char_1, "X" if char_1 != "X" else "Q"))
            idx += 1

    shift = 1 if encode else -1
    res = []

    for char_1, char_2 in pairs:
        row_1, col_1 = mapping[char_1]
        row_2, col_2 = mapping[char_2]

        # Same row
        if row_1 == row_2:
            res.append(diagram[row_1, (col_1 + shift) % 5])
            res.append(diagram[row_2, (col_2 + shift) % 5])
        # Same Column
        elif col_1 == col_2:
            res.append(diagram[(row_1 + shift) % 5, col_1])
            res.append(diagram[(row_2 + shift) % 5, col_2])

        # Rectangel rule
        else:
            res.append(diagram[row_1, col_2])
            res.append(diagram[row_2, col_1])

    return "".join(res)