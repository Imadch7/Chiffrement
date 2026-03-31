from string import ascii_lowercase
from collections import Counter

ALPH_REV = dict(enumerate(ascii_lowercase))
ALPH = {char: num for num, char in ALPH_REV.items()}

# --------------------------------------- Prime Factorisation ---------------------------------------
def prime_factors(num):
    factors = []
    d = 2
    
    while d * d <= num:
        while num % d == 0:
            factors.append(d)
            num //= d
        d += 1

    if num > 1:
        factors.append(num)

    return Counter(factors)

def prime_factors_fast(num):
    factors = []
    d = 3

    while num % 2 == 0:
        factors.append(2)
        num //= 2

    while d * d <= num:
        while num % d == 0:
            factors.append(d)
            num //= d
        d += 2

    if num > 1:
        factors.append(num)

    return Counter(factors)

def prime_factors_gen(num):
    idx = 2
    while idx * idx <= num:
        if num % idx:
            idx += 1
        else:
            num //= idx
            yield idx
    if num > 1:
        yield num

# It would be used lie this
result = Counter(prime_factors_gen(100))

def sieve_of_eratosthenes(num):
    if num < 2:
        return []
    
    prime = [True for _ in range(num + 1)]
    prime[0] = prime[1] = False
    p = 2

    while p * p <= num:
        if prime[p]:
            # Update all multiples of p
            for idx in range(p * p, num + 1, p):
                prime[idx] = False
        p += 1

    return [n for n, is_prime in enumerate(prime) if is_prime]

# IDK WHAT ANY OF THIS MEANS OR DOES
from itertools import islice
from contextlib import suppress
from math import isqrt

class IDK:
    def iter_index(self, iterable, value, start=0, stop=None):
        """Return indices where a value occurs in a sequence or iterable"""
        # iter_index("AABCADEAF", "A") → 0 1 4 7
        seq_index = getattr(iterable, "index", None)
        if seq_index is None:
            iterator = islice(iterable, start, stop)
            for idx, element in enumerate(iterator, start):
                if element is value or element == value:
                    yield idx

        else:
            stop = len(iterable) if stop is None else stop
            idx = start
            with suppress(ValueError):
                while True:
                    yield (idx := seq_index(value, idx, stop))
                    idx += 1

    def sieve(self, num):
        """Primes less than num"""
        # sieve(30) → 2 3 5 7 11 13 17 19 23 29
        if num > 2:
            yield 2
        data = bytearray((0, 1) * (num // 2))
        for p in self.iter_index(data, 1, start=3, stop=isqrt(num) + 1):
            data[p * p : num : p + p] = bytes(len(range(p * p, num, p + p)))
        yield from self.iter_index(data, 1, start=3)

    def factor(self, num):
        """Prime factors of num"""
        # factor(99) → 3 3 11
        # factor(1_000_000_000_000_007) → 47 59 360620266859
        # factor(1_000_000_000_000_403) → 1000000000000403

        for prime in self.sieve(isqrt(num) + 1):
            while not num % prime:
                yield prime
                num //= prime
                if num == 1:
                    return
                
        if num > 1:
            yield num

    def is_prime(self, num):
        """Return True if num is prime"""
        # is_prime(1_000_000_000_000_403) → True
        return num > 1 and next(self.factor(num)) == num

# THE CRAZYNESS ENDS HERE (hopefuly)

    
def get_inverse_brute_force(num, mod=26):
    if GreatestCommonDivisor.gcd_euclid_fast(num, mod) != 1:
        return -1
    
    for n in range(1, mod):
        if (num * n) % mod == 1:
            return n
        
    return -1

# --------------------------------------- Greatest Common Divisor ---------------------------------------
class GreatestCommonDivisor:
    def prime_factorization(self, a, b):
        apf = prime_factors(a)
        bpf = prime_factors(b)
        gcd = 1

        for factor, count in apf.items():
            if factor in bpf:
                count_b = bpf.get(factor, 0)
                shared_counter = min(count, count_b)
                gcd *= (factor ** shared_counter)

        return gcd

    def euclid(self, a, b):
        if b == 0:
            return a
        
        if a == 0:
            return b
        
        # Base case
        if a == b:
            return a
        
        if a > b:
            return self.euclid(a - b, b)
        
        return self.euclid(a, b - a)

    def euclid_fast(self, a, b):
        if b == 0:
            return a
        return self.euclid_fast(b, a % b)


# --------------------------------------- Least Common Multiple ---------------------------------------
class LeastCommonMultiple:
    def prime_factorization(self, a, b):
        apf = prime_factors(a)
        bpf = prime_factors(b)
        factors = set(apf.keys()) | set(bpf.keys())
        lcm = 1

        for factor in factors:
            count_a = apf.get(factor, 0)
            count_b = bpf.get(factor, 0)
            max_count = max(count_a, count_b)
            lcm *= (factor ** max_count)

        return lcm

    def with_gcd(self, a, b):
        return abs(a) * (abs(b) // GreatestCommonDivisor.euclid_fast(a, b))

# --------------------------------------- Cryptography ---------------------------------------

# --------------------------------------- Caesar's Encoding ---------------------------------------
class CaesarEncoding:
    def encode(self, plain_text, offset=3, encode=True, mod=26):
        if not plain_text:
            return None
        
        shift = offset if encode else -offset
        txt = []

        for char in plain_text:
            lower_char = char.lower()
            if lower_char in ALPH:
                new_idx = (ALPH[lower_char] + shift) % mod
                new_char = ALPH_REV[new_idx]
                txt.append(new_char.upper() if char.isupper() else new_char)
            else:
                txt.append(char)

        cipher_text = "".join(txt)

        return cipher_text

# --------------------------------------- Affine Cipher ---------------------------------------
class AffineCipher:
    def encrypt(self, plain_text, a, b, mod=26):
        if GreatestCommonDivisor.gcd_euclid_fast(a, mod) != 1:
            raise ValueError(f"Multiplier 'a' ({a}) must be coprime to ({mod})")
        
        if a == 1:
            return CaesarEncoding.encode(plain_text, offset=b)
        
        txt = []

        for char in plain_text:
            lower_char = char.lower()
            if lower_char in ALPH:
                new_idx = (a * ALPH[lower_char] + b) % mod
                new_char = ALPH_REV[new_idx]
                txt.append(new_char.upper() if char.isupper() else new_char)
            else:
                txt.append(char)

        cipher_text = "".join(txt)

        return cipher_text

    def decrypt(self, plain_text, a, b, mod=26):
        txt = []

        for char in plain_text:
            lower_char = char.lower()
            if lower_char in ALPH:
                new_idx = a * (ALPH[lower_char] - b) % mod
                new_char = ALPH_REV[new_idx]
                txt.append(new_char.upper() if char.isupper() else new_char)
            else:
                txt.append(char)

        decipher_text = "".join(txt)

        return decipher_text