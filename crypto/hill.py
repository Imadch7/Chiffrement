import numpy as np
from utils.alph import ALPH, ALPH_REV
from utils.file_handler import load_json_file

def hill(path):
    if not path:
        raise ValueError("A proper input text and a proper file path must be provided")
    
    data = load_json_file(path)
    if not data:
        raise ValueError("Could not fetch data from JSON file")
    
    # Recover the key matrix
    matrix = data["matrix"]
    key = np.array(matrix)

    # Recover the plain text
    text = data["text"]
    text = _prepare_text(text)

    size = key.shape[0]
    r = len(text) % size

    if r != 0:
        padding = size - r
        text.extend([ALPH["X"]] * padding)

    # Reshape the flat list of numbers into block of size 'size'
    blocks = np.array(text).reshape(-1, size)

    encrypted = []
    for block in blocks:
        res = np.dot(key, block) % 26
        encrypted.extend(res.astype(int).tolist())

    encrypted_text = _get_text(encrypted)

    return encrypted_text

def _get_text(txt):
    a = []
    for num in txt:
        char = ALPH_REV[num]
        a.append(char)
    return "".join(a)

def _prepare_text(text):
    txt = []
    for char in text:
        num = ALPH[char]
        txt.append(num)
    return txt