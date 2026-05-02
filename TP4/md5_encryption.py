import math

def md5(message):
    # 1. Constants (S-Table: rotation amounts)
    S = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + \
        [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

    # 2. K-Table (Constants derived from Sine)
    K = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

    # 3. Initial State (A, B, C, D)
    # Note: These are defined in Little-Endian in the RFC
    a0, b0, c0, d0 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476

    # 4. Padding
    msg = bytearray(message, 'utf-8')
    orig_len_bits = (len(msg) * 8) & 0xFFFFFFFFFFFFFFFF
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0)
    msg += orig_len_bits.to_bytes(8, byteorder='little')

    # 5. Main Loop (Process each 512-bit block)
    for i in range(0, len(msg), 64):
        chunk = msg[i:i+64]
        M = [int.from_bytes(chunk[j:j+4], byteorder='little') for j in range(0, 64, 4)]
        
        A, B, C, D = a0, b0, c0, d0

        # 64 Operations (The "Combined Function")
        for i in range(64):
            f, g = 0, 0
            if 0 <= i <= 15:
                f = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                f = (B & D) | (C & ~D)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f = B ^ C ^ D
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                f = C ^ (B | ~D)
                g = (7 * i) % 16

            # Force 32-bit overflow
            f = (f + A + K[i] + M[g]) & 0xFFFFFFFF
            A = D
            D = C
            C = B
            B = (B + rotate(f, S[i])) & 0xFFFFFFFF

        # Add this chunk's result to the running total
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

    # 6. Final Result (Convert state to hex)
    # Result must be converted back to Little-Endian bytes
    return sum(x << (32 * i) for i, x in enumerate([a0, b0, c0, d0])).to_bytes(16, byteorder='little').hex()

def rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def main():
    message = input("Enter the message to encrypt: ")
    print(md5(message))

if __name__ == "__main__":
    main()
