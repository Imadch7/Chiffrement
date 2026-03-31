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