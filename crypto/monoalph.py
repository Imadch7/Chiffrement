from utils.file_handler import FileHandler
from utils.alph import Alphabet

class MonoalphabeticCipher:
    def process_text(self, input_text, path):
        """
        Processes text using a substitution alphabet loaded from a JSON file.
        
        This method works for both encoding and decoding. To encode, provide 
        the 'encrypt' mapping. To decode, provide the 'decrypt' mapping.
        
        Args:
            input_text (str): The message to be transformed.
            path (str): Path to the JSON file containing the character mapping.
            
        Returns:
            str: The resulting cipher or plain text.
            
        Raises:
            ValueError: If the path is missing, data is empty, or alphabet is invalid.
        """

        if not path:
            raise ValueError(f"A file path must be provided")
        
        # Load the mapping (either encryption or decryption) from the JSON file
        alph = FileHandler.load_json_file(path)

        if not alph:
            raise ValueError(f"Data provided ({alph}) was empty")
        
        if not Alphabet.validate_monoalphabet(alph):
            raise ValueError(f"Invalid Monoalphabet format provided")
        
        text = []

        for char in input_text:
            lower_char = char.lower()

            if lower_char in alph:
                new_char = alph[lower_char]
                text.append(new_char.upper() if char.isupper() else new_char)
            else:
                text.append(char)

        return "".join(text)