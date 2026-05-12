import json
from os.path import exists, splitext
from os import makedirs
from sympy import randprime, gcd, mod_inverse
from sympy.ntheory import isprime

def load_json_file(path):
    """
    Validates, opens, and parses a JSON file.
    
    Args:
        path (str): The relative or absolute path to the file.
        
    Returns:
        dict: The parsed JSON data, or an empty dict if an error occurs.
    """

    if not exists(path):
        raise ValueError(f"File path {path} does not exist")

    _, file_ext = splitext(path)
    if not file_ext or file_ext.lower() != ".json":
        raise ValueError(f"File {path}, is not a JSON file ❌")
    
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
        
    except FileNotFoundError:
        print(f"File {path} not found ❌")
        return {}
    
    except json.JSONDecodeError as e:
        print(f"File {path} contains invalid JSON format:{e} ❌")
        return {}
    
    except PermissionError:
        print(f"Permission to read {path} denied")
        return {}
    
def save_to_json_file(path, data):
    """
    Saves data specifically in JSON format within the ./usr_data directory.
    """

    if not path:
        raise ValueError(f"A file path must be passed, {path} not accepted")
    
    if data is None:
        raise ValueError(f"Data must be passed.")
    
    if not exists("./output"):
        makedirs("./output")
        
    try:
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
        
    except PermissionError:
        print(f"Permission to write to ({path}) has been denied")

def rsa_encode(public_key: tuple[int] | None, message: str, bits: int, path_to_keys: str | None, to_str: bool = False):
    if bits not in (512, 1024, 2048):
        print(f"Number of bits passed is wrong")
        return
    
    msg_bytes = message.encode("utf-8")
    if len(msg_bytes) >= bits // 8:
        print(f"Error: message too long for a {bits}-bit cipher")
        return
    
    if not public_key:
        path = path_to_keys if path_to_keys else "data/rsa_keys.json"
        keys = _key_gen(path, bits)
        if not keys:
            return
        pub = keys["public"]
        priv = keys["private"]
        n, e, d = pub.get("n"), pub.get("e"), priv.get("d")
    else:
        n, e = public_key

    M = int.from_bytes(msg_bytes, "big")

    C = pow(M, e, n)

    return C.to_bytes(bits // 8, "big").hex() if to_str else C, (n, e, d), bits

def rsa_decode(private_key: tuple[int] | None, cipher, bits: int, to_str: bool = False):
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
        C = int.from_bytes(cipher_bytes, "big")
    elif isinstance(cipher, bytes):
        C = int.from_bytes(cipher, "big")
    else:
        C = cipher

    M = pow(C, d, n)

    decrypted_bytes = M.to_bytes(bits // 8, "big")

    return (decrypted_bytes.lstrip(b'\x00').decode("utf-8") if to_str else M), bits

def _key_gen(path: str, bits: int):
    if bits not in (512, 1024, 2048):
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
        "private": { "n": n, "d": d },
        "bits": bits
    }

    save_to_json_file(path, keys)

    return keys







cipher, keys, bits = rsa_encode(None, "KFNSIENCLKNFLKRFDSMCLERNFLKDSCRLNRENGTRCSelwkenfemflreknglkermflkernlkfrnferflernflkremglktnrglkeflkrenetmrlkngotrngskdmflrengltnDCRKLENGERJCELFNERVNREREV", 2048, "keys.json", True)
n, e, d = keys

print(f"rsa encode result {cipher}")

text, bits_ = rsa_decode((n, d), cipher, bits, True)
print(f"rsa decode result {text}")