from string import ascii_uppercase
from random import sample

# Alphabet mapping
# ALPH = {"a": 0, "b": 1, ...}
# ALPH_REV = {0: "a", 1: "b", ...}
ALPH_REV = dict(enumerate(ascii_uppercase))
ALPH = {char: idx for idx, char in ALPH_REV.items()}

def generate_random_monoalphabet():
    """
    Generates a random substitution alphabet (Monoalphabetic Cipher).
    
    Returns:
        tuple: Two dictionaries (encryption_map, decryption_map).
    """

    # Create a shuffled list of all 26 letters
    shuffled = sample(ascii_uppercase, len(ascii_uppercase))

    # Map "a" → "random_char", "b" → "another_random_char"
    monoalph_encrypt = dict(zip(ascii_uppercase, shuffled))

    # Map 'random_char' → "a", "another_random_char" → "b"
    monoalph_decrypt = dict(zip(shuffled, ascii_uppercase))

    return monoalph_encrypt, monoalph_decrypt

def validate_monoalphabet(alph):
    """
    Validates that a substitution alphabet is bijective.
    
    Checks that:
    1. Each source letter maps to exactly one destination letter.
    2. No two source letters map to the same destination letter.
    
    Args:
        alph (dict): The alphabet mapping to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    
    # If the number of unique values is the same as the number of keys,
    # then every key has a unique, one-to-one mapping.
    return len(set(alph.values())) == len(alph)