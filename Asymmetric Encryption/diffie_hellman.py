import random

def is_prime(n, k=5):
    """Miller-Rabin primality test."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
        
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
        
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Generate a prime number of specified bits."""
    while True:
        p = random.getrandbits(bits)
        # Ensure it's the correct bit length and odd
        p |= (1 << bits - 1) | 1
        if is_prime(p):
            return p

def find_primitive_root(p):
    """Find a primitive root for prime p."""
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // 2
    while True:
        g = random.randint(2, p - 1)
        # Check that g is a primitive root
        if pow(g, (p - 1) // p1, p) != 1 and pow(g, (p - 1) // p2, p) != 1:
            return g

class DiffieHellman:
    def __init__(self, bits=256, p=None, g=None):
        if p and g:
            self.p = p
            self.g = g
        else:
            self.p = generate_prime(bits)
            self.g = find_primitive_root(self.p)
            
        self.private_key = random.randint(2, self.p - 2)
        self.public_key = pow(self.g, self.private_key, self.p)

    def generate_shared_secret(self, other_public_key):
        return pow(other_public_key, self.private_key, self.p)

if __name__ == "__main__":
    print("=== Diffie-Hellman Key Exchange ===")
    
    print("Generating parameters for Alice...")
    alice = DiffieHellman(bits=128) # Smaller bits for faster demo
    print(f"Prime (p): {alice.p}")
    print(f"Base (g): {alice.g}")
    print(f"Alice's Private Key: {alice.private_key}")
    print(f"Alice's Public Key: {alice.public_key}")

    print("\nGenerating parameters for Bob (using same p and g)...")
    bob = DiffieHellman(p=alice.p, g=alice.g)
    
    print(f"Bob's Private Key: {bob.private_key}")
    print(f"Bob's Public Key: {bob.public_key}")

    print("\nExchanging keys...")
    alice_shared_secret = alice.generate_shared_secret(bob.public_key)
    bob_shared_secret = bob.generate_shared_secret(alice.public_key)

    print(f"Alice's Shared Secret: {alice_shared_secret}")
    print(f"Bob's Shared Secret:   {bob_shared_secret}")

    if alice_shared_secret == bob_shared_secret:
        print("\nSuccess! Both shared secrets match.")
    else:
        print("\nError! Shared secrets do not match.")
