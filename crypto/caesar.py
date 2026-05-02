from string import ascii_uppercase as alph

def caesar_cipher(text: str, key: int, encode: bool, mod: int = 26):    
    direction = 1 if encode else -1
    shift = (key * direction) % mod
    res = []

    for char in text:
        if char.isalpha():
            idx = alph.index(char.upper())
            new_char = alph[(idx + shift) % mod]
            res.append(new_char if char.isupper() else new_char.lower())
        else:
            res.append(char)

    return "".join(res)