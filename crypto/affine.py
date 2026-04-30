from string import ascii_uppercase as alph
from utils.math import get_gcd_euclid_fast

def encrypt_text(plain_text, a, b, mod=26):
    text = []
    
    if get_gcd_euclid_fast(a, mod) != 1:
        raise ValueError(f"Multiplier 'a' ({a}) must be coprime to ({mod})")

    for char in plain_text:
        upper_char = char.upper()

        if upper_char in alph:
            new_char = alph[(a * alph.index(upper_char) + b) % mod]
            text.append(new_char.upper() if char.isupper() else new_char.lower())
        else:
            text.append(char)

    return "".join(text)

def decrypt_text(plain_text, a, b, mod=26):
    text = []

    for char in plain_text:
        upper_char = char.upper()

        if upper_char in alph:
            new_char = alph[a * (alph.index(upper_char) - b) % mod]
            text.append(new_char.upper() if char.isupper() else new_char.lower())
        else:
            text.append(char)

    return "".join(text)