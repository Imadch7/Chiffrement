# a and b are 8 bit numbers

octa_degits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
gf_2_8 = "100011011" # 11B

def AES_MULT(a,b):
    if not a[0] in octa_degits or not a[1] in octa_degits or not b[0] in octa_degits or not b[1] in octa_degits:
        raise ValueError("a and b must be octa degits")
        return None
    
    if int(a,16) < int(b,16):
        a, b = b, a
    
    a_bin = bin(int(a, 16))[2:].zfill(8)
    b_bin = bin(int(b, 16))[2:].zfill(8)
    
    # multiply a and b in gf(2^8), shift a to the left and if the leftmost bit of a is 1
    result = []
    # if the leftmost bit of a is 1, add a to the result {a x 00000001} = a
    if a_bin[7] == '1':
        result.append(a_bin)
        
    for i in range(1,7):
        if b_bin[7 - i] == '1':
            a_shifted = a_bin+'0'*(i)
            result.append(a_shifted)
    
    # find the max length element in result
    max_len = max(len(x) for x in result)
    # fill the left of each element in result with 0 to make them all the same length until find 1
    
    for i in range(len(result)):
        lenght = max_len - len(result[i])
        result[i] = '0' * lenght + result[i]
    
    print(f'result: {result}')
    # XOR all the results
    final_result = result[0]
    for i in range(1, len(result)):
        final_result = ''.join(str(int(final_result[j]) ^ int(result[i][j])) for j in range(max_len))
    print(f'final_result before reduction: {final_result}')
    
    # modulo gf(2^8) 11B-> 100011011
    # each time shift final_result to the left eleminating the leftmost bit and if the leftmost bit is 1, XOR with gf_2_8
    while len(final_result) > 8:
        if final_result[0] == '0':
            final_result = final_result[1:] 
        else:
            # xor with gf_2_8 and add the remaining bits of final_result
            final_result = ''.join(str(int(final_result[j]) ^ int(gf_2_8[j])) for j in range(len(gf_2_8))) + final_result[len(gf_2_8):]
        print(f'final_result: {final_result}')
    return hex(int(final_result, 2))[2:].zfill(2)
        
    
a = "bb"
b = "bb"

print(f'a: {a} -> {int(a, 16)}')
print(f'b: {b} -> {int(b, 16)}')
a_bin = bin(int(a, 16))[2:].zfill(8)
b_bin = bin(int(b, 16))[2:].zfill(8)

print(f'a: {a} -> {a_bin}')
print(f'b: {b} -> {b_bin}')

print(f'AES_MULT({a}, {b}) = {AES_MULT(a, b)}')
