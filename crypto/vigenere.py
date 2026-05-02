from numpy import array, tile
from string import ascii_uppercase as alph

def vigenere_cipher(text: str, key: str, encode: bool):
    text = "".join([char for char in text.upper() if char.isalpha()])
    key = "".join([char for char in key if char.isalpha()])

    if not key:
        raise ValueError("Keu must contain at least one alphabetic character")
    
    text_arr = array([alph.index(char) for char in text])
    key_arr = array([alph.index(char) for char in key])

    key_stream = tile(key_arr, (len(text_arr) // len(key_arr)) + 1)[:len(text_arr)]

    multiplier = 1 if encode else -1
    res_indices = (text_arr + (multiplier * key_stream)) % 26

    return "".join(alph[idx] for idx in res_indices)