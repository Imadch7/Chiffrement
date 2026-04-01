from .factors import get_factors

def get_gcd_prime_factors(a, b):
    """
    Calculates the Greatest Common Divisor (GCD) of two numbers 
    using their prime factorizations.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The greatest common divisor of a and b.
    """

    # Get frequency maps of prime factors for both numbers
    # Example: a = 12 → {2: 2, 3: 1}, b = 18 → {2: 1, 3: 2}
    a_pf = get_factors(a)
    b_pf = get_factors(b)
    gcd = 1

    # Iterate through factors of 'a' to find intersections with 'b'
    for factor, count_a in a_pf.items():
        if factor in b_pf:
            # Get the frequency of the same factor in 'b', return 0 if not found
            count_b = b_pf.get(factor, 0)

            # The GCD uses the lowest exponent of shared prime factors
            shared_counter = min(count_a, count_b)

            # Multiply the running GCD by (factor ^ shared_exponent)
            gcd *= (factor ** shared_counter)

    return gcd

def get_gcd_euclid(a, b):
    """
    Calculates the GCD using the original Euclidean algorithm (subtraction).
    
    Args:
        a (int): First integer.
        b (int): Second integer.
        
    Returns:
        int: The greatest common divisor.
    """

    # If one number is 0, the GCD is the other number
    if b == 0:
        return a
    
    if a == 0:
        return b
    
    # Base case
    if a == b:
        return a
    
    if a > b:
        return get_gcd_euclid(a - b, b)
    
    return get_gcd_euclid(a, b - a)

def get_gcd_euclid_fast(a, b):
    """
    Calculates the GCD using the optimized Euclidean algorithm (modulo).
    
    Args:
        a (int): First integer.
        b (int): Second integer.
        
    Returns:
        int: The greatest common divisor.
    """

    if b == 0:
        return a
    
    return get_gcd_euclid_fast(b, a % b)

def get_lcm_prime_factors(a, b):
        """
        Calculates the Least Common Multiple (LCM) using prime factorization.

        Args:
            a (int): First integer.
            b (int): Second integer.

        Returns:
            int: The smallest positive integer divisible by both a and b.
        """

        # Get frequency maps of prime factors for both numbers
        a_pf = get_factors(a)
        b_pf = get_factors(b)

        # Combine all unique prime factors from both numbers using a Set Union
        factors = set(a_pf.keys()) | set(b_pf.keys())
        lcm = 1

        for factor in factors:
            # Get the power of the prime in both numbers (0 if not present)
            count_a = a_pf.get(factor, 0)
            count_b = b_pf.get(factor, 0)

            max_count = max(count_a, count_b)
            lcm *= (factor ** max_count)

        return lcm
    
def get_lcm_gcd(a, b):
    """
    Calculates the LCM using the mathematical relationship with the GCD.
    
    Formula: LCM(a, b) = |a * b| / GCD(a, b)

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: The least common multiple.
    """

    # We divide by GCD first to prevent extremely large intermediate numbers
    # that could lead to overflow in some languages.
    return abs(a) * (abs(b) // get_gcd_euclid_fast(a, b))

def get_inverse_brute_force(num, mod=26):
    """
    Finds the modular multiplicative inverse using a brute-force search.
    
    The inverse 'n' satisfies the equation: (num * n) % mod == 1.
    This is commonly used in cryptography (e.g., the Affine or RSA ciphers).

    Args:
        num (int): The number to find the inverse for.
        mod (int, optional): The modulus. Defaults to 26 (common for English alphabet).

    Returns:
        int: The modular inverse if it exists, otherwise -1.
    """

    # An inverse only exists if num and mod are 'coprime' (GCD is 1).
    # If they share a factor, no multiple of 'num' will ever result in a remainder of 1.
    if get_gcd_euclid_fast(num, mod) != 1:
        return None
    
    # Iterate through every possible value in the modular space [1, mod-1].
    for n in range(1, mod):
        # Check if 'n' is the inverse
        if (num * n) % mod == 1:
            return n
        
    return None