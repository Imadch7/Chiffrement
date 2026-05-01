from os import urandom

def otp_encode(text):
    text_bytes = text.encode('utf-8')
    pad = urandom(len(text_bytes))
    cipher_bytes = bytes([p ^ t for p, t in zip(pad, text_bytes)])
    return cipher_bytes.hex(), pad.hex()

def otp_decode(text, pad):
    pad = bytes.fromhex(pad)
    text = bytes.fromhex(text)
    plain = bytes([p ^ t for p, t in zip(pad, text)])
    return plain.decode('utf-8')