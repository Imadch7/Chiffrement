from sympy import randprime, gcd
from sympy.ntheory import isprime

def rsa_encode(public_key: tuple[int, int], message: str, bits: int, to_str: bool = False):
    if bits not in (512, 1024, 2048):
        print(f"Number of bits passed is wrong")
        return
    
    msg_bytes = message.encode('utf-8')
    if len(msg_bytes) >= bits // 8:
        print(f"Error: message too long for a {bits}-bit cipher")
        return
    
    if not public_key:
        while True:
            p = randprime(2 ** (bits // 2 - 1), 2 ** (bits // 2) - 1)
            q = randprime(2 ** (bits // 2 - 1), 2 ** (bits // 2) - 1)
            n = p * q

            if n.bit_length() == bits:
                print(f"n is on {n.bit_length()} bytes")
                break

        phi = (p - 1) * (q - 1)

        while True:
            e = randprime(2, phi)
            if isprime(e) and gcd(e, phi) == 1:
                break
    else:
        n, e = public_key

    M = int.from_bytes(msg_bytes, 'big')

    C: int = pow(M, e, n)

    return C.to_bytes(bits // 8, 'big').hex() if to_str else C, (n, e), bits