import os

class OTP:
    
    def __init__(self):
        pass
    
    @staticmethod
    def generate_key(length):
        # the key must be the same length as the plaintext (that's the whole point of OTP)
        return os.urandom(length)
    
    @staticmethod
    def encrypt(plaintext, key):
        # plaintext can be a string or bytes
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        if len(key) < len(plaintext):
            raise ValueError("Key must be at least as long as the plaintext")
        
        # XOR each byte of plaintext with the corresponding byte of the key
        ciphertext = bytes([p ^ k for p, k in zip(plaintext, key)])
        return ciphertext
    
    @staticmethod
    def decrypt(ciphertext, key):
        if len(key) < len(ciphertext):
            raise ValueError("Key must be at least as long as the ciphertext")
        
        # decryption is the same operation as encryption (XOR is its own inverse)
        plaintext = bytes([c ^ k for c, k in zip(ciphertext, key)])
        return plaintext
