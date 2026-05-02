class cryptography:
    def __init__(self):
        pass

    @staticmethod
    def cipher_cesar(plain_text, shift):
        cipher_text = ""
        shift = shift % 26
        for char in plain_text:
            # si le caractère est une lettre, on applique le décalage, sinon on le laisse tel quel
            cipher_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a')) if char.isalpha() else char
        return cipher_text

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

    # DES methode de chiffrement et de déchiffrement 
    MAX_ROUNDS = 16
    LENGTH = 16
    
    @staticmethod
    def generate_round_keys(round, length):
        table = []
        row = []

        for j in range(1, round + 1):
            for i in range(0, length):
                row.append(i)
            table.append(row)
            row = []
        return table
    
    @staticmethod
    def text_to_binary(text):
        binary = ''.join(format(ord(char), '08b') for char in text if char.isalpha())
        return binary
            
    @staticmethod
    def DES(left, right, ronds, table, i):
        if ronds <= 0:
            return str(left) + str(right)
        
        return cryptography.DES(right, left ^ table[i][right], ronds - 1, table, i + 1)
    
    @staticmethod
    def Hill_cipher(plain_text,key):
        cipher_text = ""
        #key is a square matrix of size 2 x 2
        for i in range(len(plain_text)):
            x = (key[0][0] * (ord(plain_text[i]) - ord('a')) + key[0][1] * (ord(plain_text[(i + 1) % len(plain_text)]) - ord('a'))) % 26
            y = (key[1][0] * (ord(plain_text[i]) - ord('a')) + key[1][1] * (ord(plain_text[(i + 1) % len(plain_text)]) - ord('a'))) % 26
            cipher_text += chr(x + ord('a')) + chr(y + ord('a'))
        return cipher_text
    
    @staticmethod
    def decrypt_Hill_cipher(cipher_text,key): 
        plain_text = ""
        #key is a square matrix of size 2 x 2
        det = key[0][0] * key[1][1] - key[0][1] * key[1][0]
        det_inv = pow(det, -1, 26)  # Calcul de l'inverse de det modulo 26
        inv_key = [[key[1][1] * det_inv % 26, -key[0][1] * det_inv % 26],
                   [-key[1][0] * det_inv % 26, key[0][0] * det_inv % 26]]
        
        
        for i in range(0, len(cipher_text), 2):
            x = (inv_key[0][0] * (ord(cipher_text[i]) - ord('a')) + inv_key[1][0] * (ord(cipher_text[i + 1]) - ord('a'))) % 26
            y = (inv_key[0][1] * (ord(cipher_text[i]) - ord('a')) + inv_key[1][1] * (ord(cipher_text[i + 1]) - ord('a'))) % 26
            plain_text += chr(x + ord('a')) + chr(y + ord('a'))
        return plain_text

        



