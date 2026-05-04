import os
import sys
import random

# Use hashlib for SHA256 in PSS as a primitive
try:
    import hashlib
    def custom_sha256(msg):
        if isinstance(msg, str): msg = msg.encode('utf-8')
        return hashlib.sha256(msg).digest()
except ImportError:
    pass

def is_prime(n, k=5):
    """Miller-Rabin primality test."""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def generate_prime(bits):
    """Generate a prime number of specified bits."""
    while True:
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1
        if is_prime(p): return p

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Compute modular inverse using Extended Euclidean Algorithm."""
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi
    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi, e = e, temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2, x1 = x1, x
        d, y1 = y1, y
    if temp_phi == 1:
        return d + phi

def generate_keypair(bits=1024):
    """Generate an RSA keypair."""
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def mgf1(seed, mask_len):
    """Mask Generation Function 1 (using SHA-256)."""
    T = b''
    counter = 0
    while len(T) < mask_len:
        C = counter.to_bytes(4, byteorder='big')
        T += custom_sha256(seed + C)
        counter += 1
    return T[:mask_len]

def xor_bytes(a, b):
    """XOR two byte sequences of equal length."""
    return bytes(x ^ y for x, y in zip(a, b))

def rsa_pss_sign(m, private_key, sLen=32):
    """Sign a message using RSA-PSS."""
    d, n = private_key
    hLen = 32 # SHA-256 digest length
    emLen = (n.bit_length() + 7) // 8
    
    mHash = custom_sha256(m)
    salt = os.urandom(sLen)
    
    M_prime = (b'\x00' * 8) + mHash + salt
    H = custom_sha256(M_prime)
    
    PS = b'\x00' * (emLen - sLen - hLen - 2)
    DB = PS + b'\x01' + salt
    dbMask = mgf1(H, emLen - hLen - 1)
    maskedDB = xor_bytes(DB, dbMask)
    
    # Mask most significant bit of the first byte to 0
    maskedDB_list = list(maskedDB)
    maskedDB_list[0] &= 0x7F
    maskedDB = bytes(maskedDB_list)
    
    EM = maskedDB + H + b'\xbc'
    m_int = int.from_bytes(EM, byteorder='big')
    
    # RSA signature (s = m^d mod n)
    s = pow(m_int, d, n)
    return s

def rsa_pss_verify(m, s, public_key, sLen=32):
    """Verify an RSA-PSS signature."""
    e, n = public_key
    hLen = 32
    emLen = (n.bit_length() + 7) // 8
    
    # RSA verification (m = s^e mod n)
    m_int = pow(s, e, n)
    EM = m_int.to_bytes(emLen, byteorder='big')
    
    if EM[-1:] != b'\xbc':
        return False
        
    maskedDB = EM[:emLen - hLen - 1]
    H = EM[emLen - hLen - 1 : -1]
    
    if maskedDB[0] & 0x80 != 0:
        return False
        
    dbMask = mgf1(H, emLen - hLen - 1)
    DB = xor_bytes(maskedDB, dbMask)
    
    DB_list = list(DB)
    DB_list[0] &= 0x7F
    DB = bytes(DB_list)
    
    PS_len = emLen - sLen - hLen - 2
    for i in range(PS_len):
        if DB[i] != 0x00:
            return False
            
    if DB[PS_len] != 0x01:
        return False
        
    salt = DB[-sLen:]
    mHash = custom_sha256(m)
    M_prime = (b'\x00' * 8) + mHash + salt
    H_prime = custom_sha256(M_prime)
    
    return H == H_prime

if __name__ == "__main__":
    print("=== RSA-PSS Signature ===")
    print("Generating 1024-bit RSA keypair...")
    public, private = generate_keypair(1024)
    
    message = input("Enter a message to sign: ").encode()
    print("Signing...")
    signature = rsa_pss_sign(message, private)
    print(f"Signature (int): {signature}")
    
    print("\nVerifying signature...")
    is_valid = rsa_pss_verify(message, signature, public)
    if is_valid:
        print("Signature is VALID.")
    else:
        print("Signature is INVALID.")
