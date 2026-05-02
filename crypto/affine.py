from string import ascii_uppercase as alph
from sympy import mod_inverse, gcd

def affine_encrypt(text: str, a: int, b: int, mod: int = 26):    
    if gcd(a, mod) != 1:
        raise ValueError(f"Multiplier 'a' ({a}) must be coprime to ({mod})")
    
    try:
        mod_inverse(a, mod)
    except ValueError:
        print(f"No modular inverse for 'a' ({a}) mod {mod}. Decryption later is impossible. Now encrypting...")

    res = []
    for char in text:
        if char.isalpha():
            # E(x) = (ax + b) mod m
            idx = alph.index(char.upper())
            new_char = alph[(a * idx + b) % mod]
            res.append(new_char if char.isupper() else new_char.lower())
        else:
            res.append(char)

    return "".join(res)

def affine_decrypt(text: str, a: int, b: int, mod: int = 26):
    try:
        a_inv = mod_inverse(a, mod)
    except ValueError:
        raise ValueError(f"No modular inverse for 'a' ({a}) mod {mod}. Decryption impossible")
    
    res = []
    for char in text:
        if char.isalpha():
            # D(y) = a_inv * (y - b) mod m
            idx = alph.index(char.upper())
            new_char = alph[(a_inv * (idx - b)) % mod]
            res.append(new_char if char.isupper() else new_char.lower())
        else:
            res.append(char)

    return "".join(res)
