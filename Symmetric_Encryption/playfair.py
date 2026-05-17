class Playfair:
    
    def __init__(self, key):
        self.matrix = self._generate_matrix(key)
    
    def _generate_matrix(self, key):
        # build the 5x5 matrix from the key
        # J is merged with I (standard Playfair rule)
        key = key.upper().replace('J', 'I')
        seen = []
        for ch in key:
            if ch.isalpha() and ch not in seen:
                seen.append(ch)
        # fill the rest with remaining letters
        for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # no J
            if ch not in seen:
                seen.append(ch)
        # turn the 25-letter list into a 5x5 grid
        matrix = [seen[i*5:(i+1)*5] for i in range(5)]
        return matrix
    
    def _find_position(self, char):
        # find the row and column of a character in the matrix
        for row in range(5):
            for col in range(5):
                if self.matrix[row][col] == char:
                    return row, col
        return None
    
    def _prepare_text(self, text):
        # clean the text: uppercase, replace J->I, remove non-alpha
        text = text.upper().replace('J', 'I')
        text = ''.join(ch for ch in text if ch.isalpha())
        
        # split into digraphs (pairs of 2 letters)
        # if both letters in a pair are the same, insert X between them
        digraphs = []
        i = 0
        while i < len(text):
            a = text[i]
            if i + 1 < len(text):
                b = text[i + 1]
                if a == b:
                    # same letter pair -> insert X as filler
                    digraphs.append(a + 'X')
                    i += 1
                else:
                    digraphs.append(a + b)
                    i += 2
            else:
                # odd length -> pad with X
                digraphs.append(a + 'X')
                i += 1
        return digraphs
    
    def encrypt(self, plaintext):
        digraphs = self._prepare_text(plaintext)
        ciphertext = ""
        
        for pair in digraphs:
            r1, c1 = self._find_position(pair[0])
            r2, c2 = self._find_position(pair[1])
            
            if r1 == r2:
                # same row -> shift columns to the right
                ciphertext += self.matrix[r1][(c1 + 1) % 5]
                ciphertext += self.matrix[r2][(c2 + 1) % 5]
            elif c1 == c2:
                # same column -> shift rows down
                ciphertext += self.matrix[(r1 + 1) % 5][c1]
                ciphertext += self.matrix[(r2 + 1) % 5][c2]
            else:
                # rectangle -> swap columns
                ciphertext += self.matrix[r1][c2]
                ciphertext += self.matrix[r2][c1]
        
        return ciphertext
    
    def decrypt(self, ciphertext):
        digraphs = self._prepare_text(ciphertext)
        plaintext = ""
        
        for pair in digraphs:
            r1, c1 = self._find_position(pair[0])
            r2, c2 = self._find_position(pair[1])
            
            if r1 == r2:
                # same row -> shift columns to the LEFT (reverse of encrypt)
                plaintext += self.matrix[r1][(c1 - 1) % 5]
                plaintext += self.matrix[r2][(c2 - 1) % 5]
            elif c1 == c2:
                # same column -> shift rows UP (reverse of encrypt)
                plaintext += self.matrix[(r1 - 1) % 5][c1]
                plaintext += self.matrix[(r2 - 1) % 5][c2]
            else:
                # rectangle -> swap columns (same as encrypt)
                plaintext += self.matrix[r1][c2]
                plaintext += self.matrix[r2][c1]
        
        return plaintext
