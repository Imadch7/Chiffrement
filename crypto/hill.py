import numpy as np
from string import ascii_uppercase as alph
from utils.math.operations import get_gcd_euclid_fast
from utils.math import adjugate_matrix, get_inverse_brute_force

def hill_cipher(plain_text, matrix, encode):
    plain_text = _prepare_text(plain_text)
    matrix = np.array(matrix)
    
    if np.linalg.det(matrix) == 0:
        raise ValueError("Matrix must be invertible")
    
    if get_gcd_euclid_fast(np.linalg.det(matrix), 26) != 1:
        raise ValueError("Wrong marix entered")

    key = matrix if encode else _get_decryption_key(matrix)

    size = key.shape[0]
    r = len(plain_text) % size

    if r != 0:
        padding = size - r
        plain_text.extend([alph.index("X")] * padding)

    blocks = np.array(plain_text).reshape(-1, size)

    encrypted = []
    for block in blocks:
        res = np.dot(key, block) % 26
        encrypted.extend(res.astype(int).tolist())

    return _get_text(encrypted)

def _get_text(text):
    a = []
    for num in text:
        char = alph[num]
        a.append(char)
    return "".join(a)

def _prepare_text(text):
    txt = []
    for char in text:
        num = alph.index(char)
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