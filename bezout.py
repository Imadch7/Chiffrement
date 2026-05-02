def get_coeff(a,b):
    u0,u1 = 1,0
    v0,v1 = 0,1
    
    while b!=0 :
        q = a//b
        r = a%b
        a,b = b,r
        
        u0,u1 = u1,u0 - q*u1
        v0,v1 = v1,v0 - q*v1
    
    return abs(a),u0,v0

# calcul des inverses ceasar affine

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def inverses() :
    nmb_let = int(input("Entrez le nombre de lettres : "))
    nmb_prime_with_nmb_lettres = [i for i in range(2, nmb_let) if gcd(i, nmb_let) == 1]
    for i in range(len(nmb_prime_with_nmb_lettres)):
        a = nmb_prime_with_nmb_lettres[i]
        pgcd, u, v = get_coeff(a, nmb_let)
        print(f"Inverse de {a} mod {nmb_let} est {u % nmb_let}")

special_char = {'\'':26,'.':27,',':28,' ':29} 

def chiffrer(cle,message) :
    chiff = []
    for i in range(len(message)):
        if message[i] in special_char:
            chiff.append(special_char[message[i]])
        else:
            chiff.append(((cle * (ord(message[i]) - ord('a'))) % 30))
    
    if not chiff:
        return ""
    
    message_chiffrer = ""
    for i in range(len(chiff)):
        if chiff[i]>=26:
            message_chiffrer += list(special_char.keys())[list(special_char.values()).index(chiff[i])]
        else:
            message_chiffrer += chr(chiff[i] + ord('a'))
    
    return message_chiffrer

def dechiffrer(cle,message) :
    dechiff = []
    for i in range(len(message)):
        if message[i] in special_char:
            dechiff.append(special_char[message[i]])
        else:
            dechiff.append(((cle * (ord(message[i]) - ord('a'))) % 30))
    
    if not dechiff:
        return ""
    
    message_dechiffrer = ""
    for i in range(len(dechiff)):
        if dechiff[i]>=26:
            message_dechiffrer += list(special_char.keys())[list(special_char.values()).index(dechiff[i])]
        else:
            message_dechiffrer += chr(dechiff[i] + ord('a'))
    
    return message_dechiffrer

cle = 7
inv_cle = 13

#inverses

inverses()



    