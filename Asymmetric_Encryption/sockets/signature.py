import hashlib
import sys
import os
import importlib.util

current_dir = os.path.dirname(os.path.abspath(__file__))
grandparent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
rsa_path = os.path.join(grandparent_dir, 'Asymmetric_Encryption', 'rsa_pss.py')

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

rsa_mod = load_module_from_path('rsa_mod', rsa_path)

#logic for signature
#sign the message with the private key of the sender,then encrypt it with an encryption algorithm, then Hash the encrypted message and send the hash along with the encrypted message to the receiver

class Signature:
    def __init__(self, private_key=None, public_key=None, encrypt_algo=None, decrypt_algo=None):
        self.private_key = private_key
        self.public_key = public_key
        self.encrypt_algo = encrypt_algo
        self.decrypt_algo = decrypt_algo

    def sign(self, message):
        # encrypt the message with the private key
        message_bytes = message.encode() if isinstance(message, str) else message
        if self.private_key:
            sig = rsa_mod.rsa_pss_sign(message_bytes, self.private_key)
            signed_message = f"{message}|||{sig}".encode()
        else:
            signed_message = message_bytes
            
        #encrypt the message example affine cipher
        if self.encrypt_algo:
            encrypted_message = self.encrypt_algo(signed_message).hex()
        else:
            encrypted_message = signed_message.hex()
            
        # hash the encrypted message 
        hash_object = hashlib.sha256(encrypted_message.encode())
        
        return encrypted_message, hash_object.hexdigest()

    
    def verify(self, encrypted, hash_val):
        # Hash the encrypted message
        hash_object = hashlib.sha256(encrypted.encode())
        expected_signature = hash_object.hexdigest()
        
        # Compare the expected signature with the provided signature
        if expected_signature != hash_val:
            return False, "Hash verification failed (Integrity compromised)"
            
        # Decrypt
        encrypted_bytes = bytes.fromhex(encrypted)
        if self.decrypt_algo:
            decrypted = self.decrypt_algo(encrypted_bytes).decode('utf-8', errors='ignore')
        else:
            decrypted = encrypted_bytes.decode('utf-8', errors='ignore')
            
        if "|||" in decrypted and self.public_key:
            message, sig_str = decrypted.rsplit("|||", 1)
            try:
                sig = int(sig_str)
                is_valid = rsa_mod.rsa_pss_verify(message.encode(), sig, self.public_key)
                if is_valid:
                    return True, message
                else:
                    return False, "RSA Signature verification failed (Authenticity compromised)"
            except ValueError:
                return False, "Invalid signature format"
        else:
            return True, decrypted
    
    

