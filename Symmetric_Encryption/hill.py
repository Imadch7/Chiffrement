    
class HillCipher:
    
    def __init__(self):
        pass    
    
    
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