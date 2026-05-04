class LFSR:
    def __init__(self, length, taps, initial_state):
        self.length = length
        self.taps = taps
        # Ensure state is exactly 'length' bits
        self.state = initial_state & ((1 << length) - 1)
        if self.state == 0:
            self.state = 1  # Prevent all-zero state
        
    def step(self):
        # Calculate feedback bit using XOR of tap positions
        feedback = 0
        for tap in self.taps:
            feedback ^= (self.state >> (self.length - tap)) & 1
            
        # Output is the least significant bit
        out_bit = self.state & 1
        
        # Shift and insert feedback at the MSB
        self.state = (self.state >> 1) | (feedback << (self.length - 1))
        return out_bit

class E0Cipher:
    """
    Implementation of the Bluetooth E0 stream cipher.
    Uses 4 LFSRs of lengths 25, 31, 33, and 39 bits.
    Total state is 128 bits.
    """
    def __init__(self, key):
        # Key should be a 128-bit integer
        # Split the key to initialize the 4 LFSRs
        state1 = (key >> 103) & ((1 << 25) - 1)
        state2 = (key >> 72) & ((1 << 31) - 1)
        state3 = (key >> 39) & ((1 << 33) - 1)
        state4 = key & ((1 << 39) - 1)
        
        # LFSR polynomials for E0
        self.lfsr1 = LFSR(25, [25, 20, 12, 8], state1)
        self.lfsr2 = LFSR(31, [31, 24, 16, 12], state2)
        self.lfsr3 = LFSR(33, [33, 28, 24, 4], state3)
        self.lfsr4 = LFSR(39, [39, 36, 28, 4], state4)
        
        # FSM state (2 bits)
        self.c = 0 
        
    def generate_bit(self):
        x1 = self.lfsr1.step()
        x2 = self.lfsr2.step()
        x3 = self.lfsr3.step()
        x4 = self.lfsr4.step()
        
        y = x1 + x2 + x3 + x4
        
        # Combine LFSR outputs and FSM state
        z = (x1 ^ x2 ^ x3 ^ x4 ^ (self.c & 1)) & 1
        
        # Update FSM state
        self.c = (y + self.c) // 2
        
        return z
        
    def process_byte(self, byte):
        out_byte = 0
        for i in range(8):
            bit = self.generate_bit()
            in_bit = (byte >> i) & 1
            out_bit = in_bit ^ bit
            out_byte |= (out_bit << i)
        return out_byte
        
    def crypt(self, data):
        """Encrypt or decrypt data (stream cipher operation is symmetric)"""
        if isinstance(data, str):
            data = data.encode()
        result = bytearray()
        for b in data:
            result.append(self.process_byte(b))
        return bytes(result)

if __name__ == "__main__":
    import os
    print("=== Bluetooth E0 Stream Cipher ===")
    key_hex = input("Enter a 128-bit key (hex) or leave blank for random: ")
    
    if not key_hex.strip():
        key = int.from_bytes(os.urandom(16), 'big')
        print(f"Random key generated: {hex(key)}")
    else:
        key = int(key_hex, 16)
        
    e0_encryptor = E0Cipher(key)
    
    message = input("Enter message to encrypt: ")
    encrypted = e0_encryptor.crypt(message)
    print(f"Encrypted (hex): {encrypted.hex()}")
    
    # Reset cipher state for decryption
    e0_decryptor = E0Cipher(key)
    decrypted = e0_decryptor.crypt(encrypted)
    print(f"Decrypted: {decrypted.decode(errors='ignore')}")
