from os.path import exists
from sympy import randprime, gcd, mod_inverse
from sympy.ntheory import isprime
from utils.file_handler import load_json_file, save_to_json_file

def rsa_encode(public_key: tuple[int, int] | None, message: str, bits: int, path_to_keys: str, to_str: bool = False):
    if bits not in (512, 1024, 2048):
        print(f"Number of bits passed is wrong")
        return
    
    msg_bytes = message.encode('utf-8')
    if len(msg_bytes) >= bits // 8:
        print(f"Error: message too long for a {bits}-bit cipher")
        return
    
    if not public_key:
        path = path_to_keys if path_to_keys else "data/rsa_keys.json"
        keys = _key_gen(path, bits)
        n, e = keys["public"]
    else:
        n, e = public_key

    M = int.from_bytes(msg_bytes, 'big')

    C = pow(M, e, n)

    return C.to_bytes(bits // 8, 'big').hex() if to_str else C, (n, e), bits

def rsa_decode(private_key: tuple[int, int] | None, cipher, bits: int, to_str: bool = False):
    if bits not in (512, 1024, 2048):
        print(f"Number of bits passed is wrong")
        return
    
    if not private_key:
        print("Cannot decrypt the message with a private key")
        return
    else:
        n, d = private_key
    
    if isinstance(cipher, str):
        cipher_bytes = bytes.fromhex(cipher)
    else:
        cipher_bytes = cipher

    C = int.from_bytes(cipher_bytes, 'big')

    M = pow(C, d, n)

    decrypted_bytes = M.to_bytes(bits // 8, 'big')

    return (decrypted_bytes.lstrip(b'\x00').decode('utf-8') if to_str else M), bits

def _key_gen(path: str, bits: int):
    if exists(path):
        print(f"Keys already exist in {path}")
        keys = load_json_file(path)
        return keys
    
    if bits not in (512, 1024, 2048):
        print(f"Number of bits passed is wrong")
        return
    
    while True:
        p = randprime(2 ** (bits // 2 - 1), 2 ** (bits // 2) - 1)
        q = randprime(2 ** (bits // 2 - 1), 2 ** (bits // 2) - 1)
        n = p * q

        if n.bit_length() == bits:
            print(f"n is on {n.bit_length()} bits")
            break

    phi = (p - 1) * (q - 1)

    while True:
        e = randprime(2, phi)
        if isprime(e) and gcd(e, phi) == 1:
            break

    d = mod_inverse(e, phi)

    keys = {
        "public": { "n": n, "e": e },
        "private": { "n": n, "d": d }
    }

    save_to_json_file(path, keys)

    return keys