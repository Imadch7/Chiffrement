from collections import Counter
from string import ascii_uppercase as alph
from random import sample
from .math import get_factors_gen, get_factors

def _get_key_frequency_analysis(text):
    factors = Counter(get_factors(list(text)))
    common_factor = factors.most_common(1)[0]
    arr = []

    for idx in range(common_factor):
        column = text[idx::common_factor]
        arr.append(column)

    frequency = [Counter(txt) for txt in text]
    most_frequent = [counter.most_common(1)[0] for counter in frequency]
    key = []

    for obj in most_frequent:
        char = obj[0]
        new_char = alph[(alph.index(char) - alph.index("E")) % 26]
        key.append(new_char)

    return "".join(key)

def generate_random_monoalphabet():
    """
    Generates a random substitution alphabet (Monoalphabetic Cipher).
    
    Returns:
        tuple: Two dictionaries (encryption_map, decryption_map).
    """

    # Create a shuffled list of all 26 letters
    shuffled = sample(alph, len(alph))

    # Map "a" → "random_char", "b" → "another_random_char"
    monoalph_encrypt = dict(zip(alph, shuffled))

    # Map 'random_char' → "a", "another_random_char" → "b"
    monoalph_decrypt = dict(zip(shuffled, alph))

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