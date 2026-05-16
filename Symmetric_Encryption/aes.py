import os

class AES:
    def __init__(self,size=16):
        self.size = size
        # S-box for AES SubBytes transformation
        self.sbox = [
            0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5e, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xd7, 0x4b, 0x55, 0xcf, 0x34, 0xc5, 0x84,
            0xcb, 0xbb, 0x4b, 0xd6, 0xb8, 0xd8, 0x64, 0xd4, 0x14, 0xd5, 0x6d, 0xa9, 0xe9, 0xe1, 0x86, 0x1f,
            0xf8, 0xe9, 0xce, 0x9d, 0xb0, 0x93, 0x99, 0xea, 0xcb, 0x2b, 0xac, 0xc4, 0x03, 0x7c, 0x07, 0xba,
            0x78, 0x35, 0xc2, 0x42, 0xf1, 0x2a, 0x38, 0xee, 0xc4, 0xe3, 0x5a, 0x31, 0xbd, 0xc3, 0xaa, 0xff
        ]
        # Round constants for key expansion
        self.rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
    
    def generate_aes_key(self):
        key = os.urandom(self.size) # AES key can be 16, 24, or 32 bytes (128, 192, or 256 bits)
        return key
    
    def xor_bytes(self, a, b):
        """XOR two byte sequences"""
        return bytes([x ^ y for x, y in zip(a, b)])
    
    def sub_word(self, word):
        """Apply S-box to each byte in a word (4 bytes)"""
        return bytes([self.sbox[b] for b in word])
    
    def rot_word(self, word):
        """Rotate word left by 1 byte"""
        return word[1:] + word[:1]
    
    def key_expansion(self, key):
        """Expand the cipher key into round keys using Rijndael's key schedule"""
        key_size = len(key)
        # Determine number of rounds based on key size
        if key_size == 16:
            num_rounds = 10
        elif key_size == 24:
            num_rounds = 12
        else:  # 32 bytes
            num_rounds = 14
        
        # Total words needed: 4 * (num_rounds + 1)
        total_words = 4 * (num_rounds + 1)
        w = []
        
        # First 4 words are the key
        for i in range(key_size // 4):
            w.append(key[4*i:4*i+4])
        
        # Generate remaining words
        for i in range(key_size // 4, total_words):
            temp = w[i-1]
            
            if i % (key_size // 4) == 0:
                # Apply RotWord, SubWord, and XOR with round constant
                temp = self.xor_bytes(self.sub_word(self.rot_word(temp)), 
                                     bytes([self.rcon[(i // (key_size // 4)) - 1], 0, 0, 0]))
            elif key_size > 24 and i % (key_size // 4) == 4:
                # For 256-bit keys, apply SubWord
                temp = self.sub_word(temp)
            
            w.append(self.xor_bytes(w[i - (key_size // 4)], temp))
        
        return w
    
    def sub_bytes(self, state):
        """SubBytes transformation: replace each byte using S-box"""
        result = []
        for row in state:
            result.append(bytes([self.sbox[b] for b in row]))
        return result
    
    def shift_rows(self, state):
        """ShiftRows transformation: rotate rows by different amounts"""
        result = [list(row) for row in state]
        # Row 1: no shift
        # Row 2: shift left by 1
        result[1] = result[1][1:] + result[1][:1]
        # Row 3: shift left by 2
        result[2] = result[2][2:] + result[2][:2]
        # Row 4: shift left by 3
        result[3] = result[3][3:] + result[3][:3]
        
        return [bytes(row) for row in result]
    
    def gmul(self, a, b):
        """Galois Field multiplication for MixColumns"""
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi_bit_set = a & 0x80
            a = (a << 1) & 0xff
            if hi_bit_set:
                a ^= 0x1b
            b >>= 1
        return p
    
    def mix_columns(self, state):
        """MixColumns transformation"""
        result = []
        for col in range(4):
            column = [state[row][col] for row in range(4)]
            
            new_column = [
                self.gmul(0x02, column[0]) ^ self.gmul(0x03, column[1]) ^ column[2] ^ column[3],
                column[0] ^ self.gmul(0x02, column[1]) ^ self.gmul(0x03, column[2]) ^ column[3],
                column[0] ^ column[1] ^ self.gmul(0x02, column[2]) ^ self.gmul(0x03, column[3]),
                self.gmul(0x03, column[0]) ^ column[1] ^ column[2] ^ self.gmul(0x02, column[3])
            ]
            
            for row in range(4):
                if col == 0:
                    result.append([])
                result[row].append(new_column[row])
        
        return [bytes(row) for row in result]
    
    def add_round_key(self, state, round_key):
        """AddRoundKey transformation: XOR state with round key"""
        result = []
        for row in range(4):
            result.append(self.xor_bytes(state[row], round_key[row]))
        return result
    
    def aes_encrypt(self, plaintext, key):
        """AES encryption"""
        # Ensure plaintext is 16 bytes
        if len(plaintext) < 16:
            plaintext = plaintext + b'\x00' * (16 - len(plaintext))
        plaintext = plaintext[:16]
        
        # Key expansion
        round_keys_words = self.key_expansion(key)
        
        # Determine number of rounds
        key_size = len(key)
        if key_size == 16:
            num_rounds = 10
        elif key_size == 24:
            num_rounds = 12
        else:  # 32 bytes
            num_rounds = 14
        
        # Convert plaintext to state (4x4 matrix, column-major)
        state = [bytearray([plaintext[i + j*4] for i in range(4)]) for j in range(4)]
        
        # Initial round
        round_key = [round_keys_words[i] for i in range(4)]
        state = self.add_round_key(state, round_key)
        
        # Main rounds
        for round_num in range(1, num_rounds):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            
            round_key = [round_keys_words[round_num * 4 + i] for i in range(4)]
            state = self.add_round_key(state, round_key)
        
        # Final round (without MixColumns)
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        round_key = [round_keys_words[num_rounds * 4 + i] for i in range(4)]
        state = self.add_round_key(state, round_key)
        
        # Convert state back to bytes
        ciphertext = b''
        for j in range(4):
            for i in range(4):
                ciphertext += bytes([state[i][j]])
        
        return ciphertext