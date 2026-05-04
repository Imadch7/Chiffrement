class Cesar:
    
    def __init__(self, shift):
        self.shift = shift
    
    def encrypt(self, plaintext):
        ciphertext = ""
        for char in plaintext:
            if char.isalpha():
                shift_amount = self.shift % 26
                if char.islower():
                    base = ord('a')
                else:
                    base = ord('A')
                ciphertext += chr((ord(char) - base + shift_amount) % 26 + base)
            else:
                ciphertext += char
        return ciphertext
    
    def decrypt(self, ciphertext):
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                shift_amount = self.shift % 26
                if char.islower():
                    base = ord('a')
                else:
                    base = ord('A')
                plaintext += chr((ord(char) - base - shift_amount) % 26 + base)
            else:
                plaintext += char
        return plaintext