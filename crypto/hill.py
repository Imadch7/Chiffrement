import numpy as np
from utils.alph import ALPH, ALPH_REV
from utils.file_handler import load_json_file
from utils.math import adjugate_matrix, get_inverse_brute_force

def hill(path, encode=True):
    if not path:
        raise ValueError("A proper input text and a proper file path must be provided")
    
    data = load_json_file(path)
    if not data:
        raise ValueError("Could not fetch data from JSON file")
    
    # Recover the plain text
    text = _prepare_text(data["text"])
    if not text:
        raise ValueError("A proper text must be provided")
        
    # Recover the key matrix
    matrix = np.array(data["matrix"])

    # Determine the key
    key = matrix if encode else _get_decryption_key(matrix)

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

    return _get_text(encrypted)

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

def _get_decryption_key(matrix, mod=26):
    det = int(round(np.linalg.det(matrix))) % mod

    det_inv = get_inverse_brute_force(det, mod)

    if det_inv is None:
        raise ValueError(f"Matrix is not invertible mod {mod}. Determinant {det} has no inverse.")
    
    adj = adjugate_matrix(matrix)

    dec_key = (det_inv * adj) % mod

    return dec_key.astype(int)