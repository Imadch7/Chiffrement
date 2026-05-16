class Affine:
    
    def __init__(self):
        pass
    
    @staticmethod
    def cipher_affine(plain_text, a, b):
        cipher_text = ""
        for char in plain_text:
            if char.isalpha():
                cipher_text += chr((a * (ord(char) - ord('a')) + b) % 26 + ord('a'))
            else:
                cipher_text += char
        return cipher_text
    
    @staticmethod
    def decrypt_affine(cipher_text, a, b):
        plain_text = ""
        a_inv = pow(a, -1, 26)  # Calcul de l'inverse de a modulo 26
        for char in cipher_text:
            if char.isalpha():
                plain_text += chr((a_inv * (ord(char) - ord('a') - b)) % 26 + ord('a'))
            else:
                plain_text += char
        return plain_text