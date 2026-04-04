from utils.file_handler import load_json_file
from utils.alph import ALPH, ALPH_REV

def vigenere(path, encode=True):
    if not path:
        raise ValueError("A proper input text and a proper file path must be provided")
    
    data = load_json_file(path)
    if not data:
        raise ValueError("Could not fetch data from JSON file")
    
    # Recover the plain text
    text = data["text"].upper().replace(" ", "")

    # Recover the key
    key = data["key"].upper().replace(" ", "")
    key_length = len(key)

    txt = []
    for idx in range(len(text)):
        char_val = ALPH[text[idx]]
        key_char = key[idx % key_length]
        key_val = ALPH[key_char]

        if encode:
            new_val = (char_val + key_val) % 26
        else:
            new_val = (char_val - key_val) % 26

        txt.append(ALPH_REV[new_val])

    return "".join(txt)