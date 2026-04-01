from .caesar import process_text
from utils.math import get_gcd_euclid_fast
from utils.alph import ALPH, ALPH_REV

def encrypt(plain_text, a, b, mod=26):
    """
    Encrypts text using the Affine Cipher formula: E(x) = (a * x + b) % mod.

    Args:
        plain_text (str): The text to encrypt.
        a (int): The multiplier (must be coprime to mod).
        b (int): The shift (offset).
        mod (int): The size of the alphabet.

    Returns:
        str: The encrypted cipher text.
    """

    if not plain_text:
        return None
    
    # 'a' must be coprime to the modulus for the cipher to be reversible (decipherable).
    # If they share a factor, multiple letters will map to the same cipher letter.
    if get_gcd_euclid_fast(a, mod) != 1:
        raise ValueError(f"Multiplier 'a' ({a}) must be coprime to ({mod})")
    
    if a == 1:
        return process_text(plain_text, offset=b)
    
    text = []

    for char in plain_text:
        lower_char = char.lower()
        if lower_char in ALPH:
            # Apply the affine transformation: (a * index + b) % mod
            new_idx = (a * ALPH[lower_char] + b) % mod

            new_char = ALPH_REV[new_idx]
            text.append(new_char.upper() if char.isupper() else new_char)
        else:
            text.append(char)

    cipher_text = "".join(text)

    return cipher_text

def decrypt(plain_text, a, b, mod=26):
    """
    Decrypts text using the Affine Cipher formula: D(y) = a_inv * (y - b) % mod.

    Note: a_inv must be calculated before calling this method.

    Args:
        cipher_text (str): The text to decrypt.
        a_inv (int): The modular multiplicative inverse of 'a'.
        b (int): The shift used during encryption.
        mod (int): The size of the alphabet.

    Returns:
        str: The decrypted plain text.
    """

    if a == 0:
        return process_text(plain_text, offset=b, encode=False)

    text = []

    for char in plain_text:
        lower_char = char.lower()
        if lower_char in ALPH:
            # Apply the inverse transformation: a_inv * (index - b) % mod
            new_idx = a * (ALPH[lower_char] - b) % mod
            
            new_char = ALPH_REV[new_idx]
            text.append(new_char.upper() if char.isupper() else new_char)
        else:
            text.append(char)

    decipher_text = "".join(text)

    return decipher_text