from utils.alph import ALPH, ALPH_REV

class CaesarCipher:
    def encode(self, plain_text, offset=3, encode=True, mod=26):
        """
        Encodes or decodes text using the Caesar Cipher algorithm.

        Args:
            plain_text (str): The input string to be processed.
            offset (int): The number of positions to shift each character.
            encode (bool): If True, shifts forward; if False, shifts backward (decodes).
            mod (int): The size of the alphabet (default is 26).

        Returns:
            str: The resulting cipher text or plain text, or None if input is empty.
        """
        
        if not plain_text:
            return None
        
        shift = offset if encode else -offset
        text = []

        for char in plain_text:
            lower_char = char.lower()

            # Check if the character exists in our alphabet mapping
            if lower_char in ALPH:
                new_idx = (ALPH[lower_char] + shift) % mod
                new_char = ALPH_REV[new_idx]

                # Maintain the original casing (Uppercase vs Lowercase)
                text.append(new_char.upper() if char.isupper() else new_char)

            # If it's a space, number, or punctuation, keep it as is
            else:
                text.append(char)

        cipher_text = "".join(text)

        return cipher_text