from string import ascii_uppercase
from utils.alph import ALPH
from crypto.playfair import playfair
# d = []
# for _ in range(5):
#     d.append([0] * 5)

# print(d)

# key="testplayfair"
# hashMap = [0]*26
# for idx in range(len(key)):
#         if key[idx] != "j":
#             hashMap[ord(key[idx]) - 97] = 2

# hashMap[ord("j") - 97] = 1

# print(hashMap)

# alph = ascii_uppercase.replace("W", "")
# key = key.upper().replace("J", "I")
# grid = []
# seen = set()

# for char in (key + alph):
#     if char.isalpha() and char not in seen:
#         seen.add(char)
#         grid.append(char)

# grid = [grid[i: i + 5] for i in range(0, 25, 5)]

# print(grid,end="\n\n\n")
# for row in grid:
#     print(" ".join(row))

# def _build_diagram(key):
#     """
#     Constructs a 5x5 Playfair cipher grid based on a keyword.
#     Removes W
#     """

#     if not key:
#         return None           

#     alph = [char.upper() for char in ALPH.keys() if char.upper() != "W"]
#     grid = []
#     seen = set()

#     # Process the key first, then the alphabet
#     for char in (key + "".join(alph)):
#         if char.isalpha() and char not in seen:
#             seen.add(char)
#             grid.append(char)

#     # Partition the 25 letters into 5 rows of 5
#     # Using list slicing: [0:5], [5:10], etc.
#     grid = [grid[i: i + 5] for i in range(0, 25, 5)]

#     return grid
    
# def _prepare_text(text):
#     """
#     Prepares text for Playfair rules:
#     - Uppercases and replaces W with V
#     - Splits into digraphs (pairs)
#     - Inserts 'X' between identical letters in a pair (e.g., 'HELLO' -> 'HE', 'LX', 'LO')
#     - Pads with 'X' if the final length is odd
#     """

#     processed = []
#     idx = 0

#     while idx < len(text):
#         c1 = text[idx]

#         if idx + 1 < len(text):
#             c2 = text[idx + 1]
#             if c1 == c2:
#                 # Not allowing isentical letters
#                 filler = "Q" if c1 == "X" else "X"
#                 processed.append((c1, filler))
#                 idx += 1
#             else:
#                 processed.append((c1, c2))
#                 idx += 2
#         else:
#             # Pad the end if there is a lone character
#             filler = "Q" if c1 == "X" else "X"
#             processed.append((c1, filler))
#             idx += 1

#     return processed

# key = "test playfair".upper().replace(" ", "").replace("W", "")
# print(_build_diagram(key))
# text = "FOX"
# print(_prepare_text(text))
a = playfair("Hide the gold under the carpet", "neso academy")
b = playfair("ODZFQSEZSONTSW", "neso APP", False)
print(a, b)