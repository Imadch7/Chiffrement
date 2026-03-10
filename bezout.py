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

# Exemple
nmb_lettres = int(input("Entrez le nombre de lettres : "))
nmb_prime_with_nmb_lettres = [i for i in range(2, nmb_lettres) if gcd(i, nmb_lettres) == 1]

for i in range(len(nmb_prime_with_nmb_lettres)):
    a = nmb_prime_with_nmb_lettres[i]
    pgcd, u, v = get_coeff(a, nmb_lettres)
    print(f"Inverse de {a} mod {nmb_lettres} est {u % nmb_lettres}")

    