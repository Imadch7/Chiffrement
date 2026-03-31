from collections import Counter

class Math:
    def get_gcd_prime_factors(self, a, b):
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
        a_pf = self.get_factors(a)
        b_pf = self.get_factors(b)
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
    
    def get_gcd_euclid(self, a, b):
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
            return self.get_gcd_euclid(a - b, b)
        
        return self.get_gcd_euclid(a, b - a)
    
    def get_gcd_euclid_fast(self, a, b):
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
        
        return self.get_gcd_euclid_fast(b, a % b)
    
    def get_lcm_prime_factors(self, a, b):
        """
        Calculates the Least Common Multiple (LCM) using prime factorization.

        Args:
            a (int): First integer.
            b (int): Second integer.

        Returns:
            int: The smallest positive integer divisible by both a and b.
        """

        # Get frequency maps of prime factors for both numbers
        a_pf = self.get_factors(a)
        b_pf = self.get_factors(b)

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
    
    def get_lcm_gcd(self, a, b):
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
        return abs(a) * (abs(b) // self.get_gcd_euclid_fast(a, b))
    
    def is_prime(self, num):
        pass

    def sieve_of_eratosthenes(self, num):
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

    def get_factors(self, num):
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
    
    def get_factors_gen(self, num):
        """
        A generator that yields prime factors of a given number one by one.

        It would be used like this:
            res = Counter(Math.get_factors_gen(100))

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

    def get_inverse_brute_force(self, num, mod=26):
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
        if self.get_gcd_euclid_fast(num, mod) != 1:
            return -1
        
        # Iterate through every possible value in the modular space [1, mod-1].
        for n in range(1, mod):
            # Check if 'n' is the inverse
            if (num * n) % mod == 1:
                return n
            
        return -1