from string import ascii_uppercase as alph
from utils.alph import _get_key_frequency_analysis

def vigenere_cipher(plain_text, key, encode):
    plain_text = plain_text.upper().replace(" ", "")
    key = key.upper().replace(" ", "") if encode else _get_key_frequency_analysis(plain_text)

    key_length = len(key)

    text = []
    for idx in range(len(plain_text)):
        char_val = alph.index(plain_text[idx])
        key_char = key[idx % key_length]
        key_val = alph.index(key_char)

        if encode:
            new_val = (char_val + key_val) % 26
        else:
            new_val = (char_val - key_val) % 26

        text.append(alph[new_val])

    return "".join(text)