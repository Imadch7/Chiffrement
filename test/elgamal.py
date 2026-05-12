from os.path import exists, splitext
from os import makedirs
import json
from secrets import randbelow, randbits
from sympy import randprime, mod_inverse
from sympy.ntheory import isprime, nextprime

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

    print(f"Searching for a {bits}-bit safe prime...")
    # Start at a cryptographically random odd number
    start_val = randbits(bits - 1) | 1 
    current_q = nextprime(start_val)
    
    print("Generating random prime number\nThis might take a long time to execute...")
    while True:
        p = 2 * current_q + 1
        if isprime(p):
            print(f"Prime number generated is {p}")
            break
        current_q = nextprime(current_q)

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

    return keys

if __name__ == "__main__":
    import os
    
    # Configuration
    TEST_BITS = 1024  # Using 1024 for faster testing than 2048
    TEST_PATH = "data/test_elgamal_keys.json"
    
    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")

    print(f"--- Starting ElGamal Test ({TEST_BITS} bits) ---")

    # 1. Test Key Generation & Encryption
    # We pass None for public_key to force it to use _key_gen
    original_text = "Alice knows Bob's secret!"
    print(f"\n[1] Encrypting message: '{original_text}'")
    
    # Note: your encode returns ((C1, C2), (y, p, g, s))
    ciphertext, keys_used = elgamal_encode(None, original_text, TEST_BITS, TEST_PATH)
    
    if ciphertext:
        c1, c2 = ciphertext
        y, p, g, s = keys_used
        print(f"Success! Ciphertext generated.")
        print(f"C1 (first 20 chars): {str(c1)[:20]}...")
        print(f"C2 (first 20 chars): {str(c2)[:20]}...")

        # 2. Test Decryption
        print(f"\n[2] Decrypting message...")
        # Your decode expects (s, p) as the private key tuple
        private_tuple = (s, p)
        decrypted_result, _ = elgamal_decode(private_tuple, c1, c2, TEST_BITS, to_str=True)

        print(f"Decrypted result: '{decrypted_result}'")

        # 3. Validation
        if original_text == decrypted_result:
            print("\n✅ PASSED: Decrypted message matches original!")
        else:
            print("\n❌ FAILED: Decrypted message mismatch.")

    # 4. Test Error Handling: Message too long
    print(f"\n[3] Testing message length limit...")
    long_message = "A" * (TEST_BITS // 8 + 1)
    # This should trigger your "Error: message too long" print
    elgamal_encode(keys_used, long_message, TEST_BITS, TEST_PATH)
    
    print("\n--- Test Complete ---")