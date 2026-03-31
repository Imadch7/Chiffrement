from string import ascii_lowercase
from random import sample

class Alphabet:
    # Alphabet mapping
    # ALPH = {"a": 0, "b": 1, ...}
    # ALPH_REV = {0: "a", 1: "b", ...}
    ALPH_REV = dict(enumerate(ascii_lowercase))
    ALPH = {char: idx for idx, char in ALPH_REV.items()}

    def generate_random_monoalphabet(self):
        """
        Generates a random substitution alphabet (Monoalphabetic Cipher).
        
        Returns:
            tuple: Two dictionaries (encryption_map, decryption_map).
        """

        # Create a shuffled list of all 26 letters
        shuffled = sample(ascii_lowercase, len(ascii_lowercase))

        # Map "a" → "random_char", "b" → "another_random_char"
        monoalph_encrypt = dict(zip(ascii_lowercase, shuffled))

        # Map 'random_char' → "a", "another_random_char" → "b"
        monoalph_decrypt = dict(zip(shuffled, ascii_lowercase))

        return monoalph_encrypt, monoalph_decrypt
    
    def validate_monoalphabet(self, alph):
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