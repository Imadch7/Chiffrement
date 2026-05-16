class VigenereCipher:
    
    def __init__(self):
        pass
    
    @staticmethod
    def cipher_vigenere(plain_text, key):
        cipher_text = ""
        key_length = len(key)
        for i, char in enumerate(plain_text):
            if char.isalpha():
                shift = ord(key[i % key_length].lower()) - ord('a')
                cipher_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                cipher_text += char
        return cipher_text
    
    @staticmethod
    def decrypt_vigenere(cipher_text, key):
        plain_text = ""
        key_length = len(key)
        for i, char in enumerate(cipher_text):
            if char.isalpha():
                shift = ord(key[i % key_length].lower()) - ord('a')
                plain_text += chr((ord(char)-ord('a') - shift) % 26 + ord('a')) 
            else:
                plain_text += char
        return plain_text