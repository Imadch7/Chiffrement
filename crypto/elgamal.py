from os.path import exists, splitext
from secrets import randbelow
from sympy import randprime, mod_inverse
from sympy.ntheory import isprime
from utils.file_handler import load_json_file, save_to_json_file

def elgamal_encode(public_key: tuple[int] | None, message: str, bits: int, path_to_keys: str):
    if bits not in (512, 1024, 2048):
        print(f"Number of bits passed is wrong")
        return
    
    msg_bytes = message.encode("utf-8")
    if len(msg_bytes) >= bits // 8:
        print(f"Error: message too long for a {bits}-bit cipher")
        return
    
    if not public_key:
        path = path_to_keys if path_to_keys else "data/elgamal_keys.json"
        keys = _key_gen(path, bits)
        if not keys:
            return
        pub = keys["public"]
        priv = keys["private"]
        y, p, g, s = pub.get("y"), pub.get("p"), pub.get("g"), priv.get("s")
    else:
        y, p, g, s = public_key

    k = randbelow(p - 2) + 1
    C1 = pow(g, k, p)
    M = int.from_bytes(msg_bytes, "big")
    C2 = (M * pow(y, k, p))  % p

    return (C1, C2), (y, p, g, s)

def elgamal_decode(private_key: tuple[int] | None, C1, C2, bits: int, to_str: bool = False):
    if bits not in (512, 1024, 2048):
        print(f"Number of bits passed is wrong")
        return
    
    if not private_key:
        print("Cannot decrypt the message with a private key")
        return
    else:
        s, p = private_key

    R = pow(C1, s, p)
    R_inv = mod_inverse(R, p)
    M = (C2 * R_inv) % p

    decrypted_bytes = M.to_bytes(bits // 8, "big")

    return (decrypted_bytes.lstrip(b'\x00').decode("utf-8") if to_str else M), bits

def _key_gen(path: str, bits: int):
    if bits not in (1024, 2048):
        print(f"Number of bits passed is wrong")
        return None
    
    if exists(path):
        print(f"Keys already exist in {path}")
        keys = load_json_file(path)

        if keys.get("bits") == bits:
            print(f"Compatible {bits}-bit keys already exist in {path}")
            return keys
        else:
            base, ext = splitext(path)
            path = f"{base}_{bits}{ext}"

            if exists(path):
                return load_json_file(path)
            
            print(f"Bit mismatch. Generating new {bits}-bit keys at {path}")
    
    while True:
        # this will take a long time to execute
        p = randprime(2 ** (bits - 1), 2 ** (bits) - 1)
        if isprime((p - 1) // 2):
            break

    while True:
        # 1 < g < p - 1
        g = randbelow(p - 3) + 2

        if pow(g, 2, p) != 1 and pow(g, (p - 1) // 2, p) != 1:
            break

    s = randbelow(p - 2) + 1
    y = pow(g, s, p)

    keys = {
        "public": { "y": y, "p": p, "g": g },
        "private": { "s": s, "p": p }
    }

    save_to_json_file(path, keys)