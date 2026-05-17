import os

class DES:
    #sbox 4*16
    
    def __init__(self):
        pass
    def generate_des_key(self):
        key = os.urandom(8) # DES key is 8 bytes (64 bits)
        return key
    
    # generate round keys for DES
    def generate_round_keys(self,key):
        binary_key = bin(int.from_bytes(key, 'big'))[2:]
        #matrix of 8*8
        key_matrix = [binary_key[i:i+8] for i in range(len(binary_key))]
        #drop parity bits and permute the key
        for i in range(len(key_matrix[0])):
            key_matrix[i] = key_matrix[i][0:7]
        
        shifts = [2,2,1,1,1,1,1,1,2,1,1,1,1,1,1,2]
        left_half = key_matrix[0:4]
        right_half = key_matrix[4:8]
        left_half = ''.join(left_half)
        right_half = ''.join(right_half)
        round_keys = []
        size = 28
        for shift in shifts:
            left_half = [left_half[i-shift] for i in range(size)]
            right_half = [right_half[i-shift] for i in range(size)]
            round_key = left_half + right_half
            kkey = [round_key[i] for i in range(56) if i not in [9,18,22,25,35,38,43,54]]
            round_keys.append(kkey)
        return round_keys
    
    def generate_initial_permutation_table(self):
        # Initial Permutation table for DES
        return [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9 ,1,
                59, 51, 43, 35, 27, 19,11 ,3,
                61, 53,45 ,37 ,29 ,21 ,13 ,5,
                63 ,55 ,47 ,39 ,31 ,23 ,15 ,7]
    
    def final_permutation(self):
        return [40, 8, 48, 16, 56, 24, 64, 32,
                39, 7, 47, 15, 55, 23, 63, 31,
                38, 6, 46, 14, 54, 22, 62, 30,
                37, 5, 45, 13, 53, 21, 61, 29,
                36, 4, 44, 12, 52, 20, 60, 28,
                35, 3, 43,11 ,51 ,19 ,59 ,27,
                34 ,2 ,42 ,10 ,50 ,18 ,58 ,26,
                33 ,1 ,41 ,9 ,49 ,17 ,57 ,25]
    
    def expansion(self, right_half):
        # list of 4 bits x 8
        list_of_4_bits = [right_half[i:i+4] for i in range(0, len(right_half), 4)]
        #expand to 48 bits
        expanded_half = []
        for i in range(8):
            if i == 0:
                expanded_half.append(list_of_4_bits[7][-1] + list_of_4_bits[0] + list_of_4_bits[1][0])
            elif i == 7:
                expanded_half.append(list_of_4_bits[6][-1] + list_of_4_bits[7] + list_of_4_bits[0][0])
            else:
                expanded_half.append(list_of_4_bits[i-1][-1] + list_of_4_bits[i] + list_of_4_bits[i+1][0])
        return ''.join(expanded_half)
    
    def xor(self, expanded_half, round_key):
        return ''.join(['1' if expanded_half[i] != round_key[i] else '0' for i in range(len(expanded_half))])
    
    def round_right_box(self, xored_half):
        #S-boxes for DES 4 * 16 bits
        s_boxes = [
            ['1110', '0100', '1101', '0001', '0010', '1111', '1011', '1000', '0011', '1010', '0110', '1100', '0101', '1001', '0000', '0111'],
            ['0000', '1111', '0111', '0100', '1110', '0010', '1101', '0001', '1010', '0110', '1100', '1011', '1001', '0101', '0011', '1000'],
            ['0100', '0001', '1110', '1000', '1101', '0110', '0010', '1011', '1111', '1100', '1001', '0111', '0011', '1010', '0101', '0000'],
            ['1111', '1100', '1000', '0010', '0100', '1001', '0001', '0111', '0101', '1011', '0011', '1110', '1010', '0000', '0110','1101']
        ]
        #xored_half is 48 bits, divide into 8 groups of 6 bits
        groups_of_6_bits = [xored_half[i:i+6] for i in range(0, len(xored_half), 6)]
        output = ''
        for i in range(8):
            row = int(groups_of_6_bits[i][0]+groups_of_6_bits[i][5], 2)
            col = int(groups_of_6_bits[i][1:5], 2)
            output += s_boxes[row][col]  
        return output
    
    def permutation(self, right_half):
        #permutation table for DES 32 bits
        permutation_table = [16, 7, 20, 21, 29, 12, 28, 17,
                              1, 15, 23, 26, 5, 18, 31, 10,
                              2, 8, 24, 14, 32, 27, 3, 9,
                              19, 13, 30, 6, 22, 11, 4, 25]
        # Apply permutation i-1 because the table is 1-indexed to 32
        permuted = ''.join([right_half[i-1] for i in permutation_table])
        return permuted
    
    def des_encrypt(self, plaintext, key):
            # Convert plaintext to binary string first
            if isinstance(plaintext, bytes):
                plaintext_binary = bin(int.from_bytes(plaintext, 'big'))[2:].zfill(len(plaintext) * 8)
            else:
                # If plaintext is a string, encode it to bytes first
                if isinstance(plaintext, str):
                    plaintext = plaintext.encode('utf-8')
                plaintext_binary = bin(int.from_bytes(plaintext, 'big'))[2:].zfill(len(plaintext) * 8)
            
            # Ensure plaintext_binary is exactly 64 bits (8 bytes)
            if len(plaintext_binary) < 64:
                plaintext_binary = plaintext_binary.zfill(64)
            elif len(plaintext_binary) > 64:
                plaintext_binary = plaintext_binary[:64]
            
            # Initial Permutation
            initial_permutation_table = self.generate_initial_permutation_table()
            permuted_plaintext = ''.join([plaintext_binary[i-1] for i in initial_permutation_table])
            left_half = permuted_plaintext[:32]
            right_half = permuted_plaintext[32:]
            round_keys = self.generate_round_keys(key)
            for round_key in round_keys:
                expanded_half = self.expansion(right_half)
                xored_half = self.xor(expanded_half, round_key)
                round_right_box_output = self.round_right_box(xored_half)
                permuted_right_half = self.permutation(round_right_box_output)
                new_right_half = ''.join(['1' if left_half[i] != permuted_right_half[i] else '0' for i in range(len(left_half))])
                left_half, right_half = right_half, new_right_half
            # Final Permutation (inverse of initial permutation)
            final_permutation_table = self.final_permutation()
            combined = right_half + left_half
            ciphertext = ''.join([combined[i-1] for i in final_permutation_table])
            return ciphertext