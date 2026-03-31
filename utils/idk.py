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