import random

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

def find_primitive_root(p):
    """Find a primitive root (generator) for prime p."""
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // 2
    while True:
        g = random.randint(2, p - 1)
        if pow(g, (p - 1) // p1, p) != 1 and pow(g, (p - 1) // p2, p) != 1:
            return g

class ElGamal:
    def __init__(self, bits=256):
        """
        Generate ElGamal key pair.
        
        Public key  = (p, g, h)   where h = g^x mod p
        Private key = x           (random secret exponent)
        """
        # Generate a large prime p
        self.p = generate_prime(bits)
        # Find a generator g of the multiplicative group Z*_p
        self.g = find_primitive_root(self.p)
        # Private key: random x in [2, p-2]
        self.x = random.randint(2, self.p - 2)
        # Public key component: h = g^x mod p
        self.h = pow(self.g, self.x, self.p)

    def get_public_key(self):
        """Return the public key (p, g, h)."""
        return (self.p, self.g, self.h)

    def get_private_key(self):
        """Return the private key x."""
        return self.x

    @staticmethod
    def encrypt(plaintext_int, public_key):
        """
        Encrypt a message (integer) using ElGamal.
        
        plaintext_int: message as integer, must be in [1, p-1]
        public_key:    tuple (p, g, h)
        
        Returns ciphertext (c1, c2) where:
            c1 = g^y mod p
            c2 = m * h^y mod p
        """
        p, g, h = public_key
        # Choose random ephemeral key y
        y = random.randint(2, p - 2)
        # c1 = g^y mod p
        c1 = pow(g, y, p)
        # c2 = m * h^y mod p  (shared secret s = h^y)
        s = pow(h, y, p)
        c2 = (plaintext_int * s) % p
        return (c1, c2)

    def decrypt(self, ciphertext):
        """
        Decrypt an ElGamal ciphertext (c1, c2).
        
        Uses private key x to recover:
            m = c2 * (c1^x)^(-1) mod p
        """
        c1, c2 = ciphertext
        # Compute shared secret: s = c1^x mod p
        s = pow(c1, self.x, self.p)
        # Modular inverse of s: s^(-1) = s^(p-2) mod p  (Fermat's little theorem)
        s_inv = pow(s, self.p - 2, self.p)
        # Recover plaintext: m = c2 * s^(-1) mod p
        plaintext_int = (c2 * s_inv) % self.p
        return plaintext_int

def text_to_int(text):
    """Convert a text string to an integer."""
    return int.from_bytes(text.encode('utf-8'), byteorder='big')

def int_to_text(n):
    """Convert an integer back to a text string."""
    byte_length = (n.bit_length() + 7) // 8
    return n.to_bytes(byte_length, byteorder='big').decode('utf-8')


