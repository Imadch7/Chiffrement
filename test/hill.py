# s = "oh hello therexXA"
# arr = list(s)
# print(arr)

# a = [ord(x) for x in arr]
# b = [ord(x) for x in s]

# print(a, b)

from utils.file_handler import load_json_file
import numpy as np
from utils.alph import ALPH, ALPH_REV
from string import ascii_lowercase

def hill(input_text, path, encode=True):
    if not input_text or not path:
        raise ValueError("A proper input text and a proper file path must be provided")
    
    # data = load_json_file(path)
    # Example data
    data = {
        "matrix": [[9,4],[5,7]],
        "text": "hill"
    }
    if not data:
        raise ValueError("Could not fetch data from JSON file")
    
    matrix = data["matrix"]
    txt = data["text"]

    key = np.array(matrix) if encode else np.invert(np.array(matrix))
    text = _prepare_text(txt)

    size = key.shape[0]
    r = len(text) % size

    if r != 0:
        padding = size - r
        text.extend([23] * padding)

    # Reshape the flat list of numbers into block of size 'size'
    blocks = np.array(text).reshape(-1, size)

    encrypted = []
    for block in blocks:
        res = np.dot(key, block) % 26
        encrypted.extend(res.astype(int).tolist())
    

    t = _get_text(encrypted)
    print(f"t is {t}")
    return t

def _get_text(txt):
    a = []
    for num in txt:
        c = ALPH_REV[num]
        print(c)
        a.append(c)
    return "".join(a)

def _prepare_text(text):
    txt = []
    for char in text:
        num = ALPH[char]
        txt.append(num)
    return txt

print(ALPH)
print(hill("d","d"))