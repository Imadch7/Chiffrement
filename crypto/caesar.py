from string import ascii_uppercase as alph

def process_text(plain_text, offset, encode, mod=26):
    if (not encode and offset > 0) or (encode and offset < 0):
        raise ValueError("Illogical arguments passed")
    
    text = []

    for char in plain_text:
        upper_char = char.upper()

        if upper_char.isalpha():
            new_char = alph[(alph.index(upper_char) + offset) % mod]
            text.append(new_char.upper() if char.isupper() else new_char.lower())
        else:
            text.append(char)

    return "".join(text)