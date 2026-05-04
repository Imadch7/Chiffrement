
import os


class RC4:
    def __init__(self):
       pass
    # RC4 key from 40 to 2048 bits (5 to 256 bytes)
    def generate_rc4_key(self, key_length=16):
        key = os.urandom(key_length)
        return key
    
    
    def KSA(self, key):
        key_length = len(key)
        S = list(range(256)) #list de 0 a 255
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]
        return S
    
    def PRGA(self, S):
        i, j = 0, 0
        while True:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            yield K #stop until next call

    def rc4_encrypt(self, plaintext, key):
        S = self.KSA(key)
        plaintext = b'' + plaintext 
        keystream = self.PRGA(S)
        ciphertext = bytes([p ^ next(keystream) for p in plaintext])
        return ciphertext
    
    def rc4_decrypt(self, ciphertext, key):
        #Xor with keystream again to get plaintext
        return self.rc4_encrypt(ciphertext, key) #because RC4 is symmetric
