from string import ascii_lowercase

ALPH_REV = dict(enumerate(ascii_lowercase))
ALPH = {char: idx for idx, char in ALPH_REV.items()}