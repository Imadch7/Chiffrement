from collections import Counter

def get_factors(num):
    """
    Calculates prime factors efficiently by skipping even divisors, and returns their counts.

    Example: 12 → {2: 2, 3: 1}.

    Args:
        num (int): The positive integer to factorize.

    Returns:
        Counter: A frequency map of prime factors. 
        Example: 28 → Counter({2: 2, 7: 1})
    """

    if num <= 1:
        return -1
    
    factors = []
    d = 3

    # Handle the only even prime separately
    # Allowing us to skip all other even numbers in the main loop
    while num % 2 == 0:
        factors.append(2)
        num //= 2

    # Only need to check up to the square root of num
    # If num has a factor larger than sqrt(num), 
    # there must be a corresponding factor smaller than sqrt(num)
    while d * d <= num:
        while num % d == 0:
            factors.append(d)
            num //= d

        d += 2

    # If num is still > 1 after the loop, the remaining num is prime
    if num > 1:
        factors.append(num)

    # Returns a dictionary-like object mapping prime factors to their frequency
    return Counter(factors)

def get_factors_gen(num):
    """
    A generator that yields prime factors of a given number one by one.

    It would be used like this:
        res = Counter(get_factors_gen(100))

    Args:
        num (int): The positive integer to factorize.

    Yields:
        int: The next prime factor found in the factorization.

    Returns:
        Counter: A frequency map of prime factors. 
        Example: 28 → Counter({2: 2, 7: 1})
    """

    if num <= 1:
        return -1
    
    idx = 2

    # Loop until idx exceeds the square root of the remaining num
    while idx * idx <= num:
        # If num is not divisible by idx, move to the next possible divisor
        if num % idx != 0:
            idx += 1

        # If num is divisible, yield the factor and reduce num
        else:
            num //= idx
            yield idx
    
    # If num is still > 1 after the loop, the remaining num is prime
    if num > 1:
        yield num