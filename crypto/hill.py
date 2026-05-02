from numpy import array
from sympy import Matrix, gcd
from string import ascii_uppercase as alph

def hill_cipher(text: str, matrix: list, encode: bool, mod: int = 26):
    # Convert key to a SymPy Matrix for exact modular math
    sm_key = Matrix(matrix)
    
    if not sm_key.is_square:
        raise ValueError("Key matrix must be square")
    
    size = sm_key.shape[0]
    det = sm_key.det()
    
    # Validation
    if det == 0:
        raise ValueError("Matrix determinant is 0 and cannot be inverted")
    
    if gcd(int(det), mod) != 1:
        raise ValueError(f"Matrix determinant ({det % mod}) is not coprime with {mod}. Decryption will be impossible {"Encrypting now..." if encode else ""}")

    # Determine the actual Key Matrix to use
    sm_key = sm_key if encode else sm_key.inv_mod(mod)

    # Convert back to NumPy for fast numerical operations
    key = array(sm_key).astype(int)

    # Prepare text
    text = text.upper().replace(" ", "")
    # This replaces the old _prepare_text(text: str) function
    indices = [alph.index(c) for c in text if c in alph]

    # Padding
    padding = (size - len(indices) % size) % size
    indices.extend([alph.index('X')] * padding)

    # Process in Blocks using NumPy Matrix Multiplication
    # Reshape into (N, size) blocks
    input_blocks = array(indices).reshape(-1, size)

    # We multiply: (Block @ Key.T) % mod
    # Transposing the key is necessary if the blocks are row vectors
    res_indices = (input_blocks @ key.T) % mod

    # Convert back to text
    return "".join(alph[idx] for idx in res_indices.flatten())