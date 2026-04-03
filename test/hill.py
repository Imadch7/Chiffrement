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
from utils.math import adjugate_matrix, get_inverse_brute_force

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

K = np.array([[9, 4], [5, 7]])

def _get_decryption_key(matrix, mod=26):
    # 1. Calculate the determinant
    # We use round() because np.linalg.det returns a float
    det = int(round(np.linalg.det(matrix))) % mod
    
    # 2. Find the modular inverse of the determinant
    # This is the "x" where (det * x) % 26 == 1
    det_inv = get_inverse_brute_force(det, mod)
    
    if det_inv is None:
        raise ValueError(f"Matrix is not invertible mod {mod}. Determinant {det} has no inverse.")

    # 3. Get the adjugate matrix (Transpose of the Cofactor matrix)
    # Your adjugate_matrix(matrix) already calls cofactor(matrix).T
    adj = adjugate_matrix(matrix)
    
    # 4. Multiply the adjugate by the modular inverse of the determinant
    # Then apply modulo 26 to every element
    dec_key = (det_inv * adj) % mod
    
    # Convert to standard integers so we don't have numpy types lurking
    return dec_key.astype(int)

J = _get_decryption_key(K)
print(J)