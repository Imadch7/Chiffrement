def is_prime(num):
    pass

def sieve_of_eratosthenes(num):
    """
    Finds all prime numbers up to a given limit (num) using the Sieve of Eratosthenes.

    Args:
        num (int): The upper bound (inclusive) to check for primes.

    Returns:
        list: A list of all prime numbers less than or equal to num.
            Example: 10 → [2, 3, 5, 7]
    """

    # Primes start at 2; return empty list for 0 or 1
    if num < 2:
        return []
    
    # Initialize a boolean list "prime[0..num]" and set all to True.
    # A value in prime[i] will finally be False if i is Not a prime.
    prime = [True for _ in range(num+ 1)]
    
    # Set the value of 0 and 1 to False before the loop
    prime[0] = prime[1] = False

    # Start from 2
    p = 2

    # Only need to check up to the square root of num
    while p * p <= num:
        # If prime[p] is not changed, then it is a prime
        if prime[p]:
            # Update all multiples of p
            # We start at p * p because smaller multiples (like 2 * p)
            # would have already been marked False by earlier primes.
            for idx in range(p * p, num + 1, p):
                prime[idx] = False

        p += 1

    # Return the indices that remained True after the loop
    return [n for n, is_prime in enumerate(prime) if is_prime]