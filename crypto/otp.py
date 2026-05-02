import secrets
import numpy as np

def otp_encode(text: str):
    text_bytes = text.encode('utf-8')
    pad_bytes = secrets.token_bytes(len(text_bytes))
    t_arr = np.frombuffer(text_bytes, dtype=np.uint8)
    p_arr = np.frombuffer(pad_bytes, dtype=np.uint)
    cipher_bytes = np.bitwise_xor(t_arr, p_arr).tobytes()
    return cipher_bytes.hex(), pad_bytes.hex()

def otp_decode(cipher_hex: str, pad_hex: str):
    c_arr = np.frombuffer(bytes.fromhex(cipher_hex), dtype=np.uint8)
    p_arr = np.frombuffer(bytes.fromhex(pad_hex), dtype=np.uint8)
    plain_bytes = np.bitwise_xor(c_arr, p_arr).tobytes()
    return plain_bytes.decode('utf-8')