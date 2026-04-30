from collections import Counter
# from utils.alph import ALPH, ALPH_REV
from crypto.vigenere import vigenere

# text = "NTLIEMOEHQREZMCEQAEUZLTPXWXAFMQRMVLIETLGDIYDQNZROMOUOPTFRZPDQDTGQVPRQMDTCCPLMUPMQTPTFZPSQZLCTQQFDMPDQLTFRMCEZBPSYIYIQZPSXMNHUNQRQLPVUOPNQZPEJQREOWXMQXCEEYFEXIEOFIWIFMOEEAJSFMXEELPCTQQFDMXEZBBUQTPSPMFXOWCRQAAOZLLNFANOZVLIEAPNFCYEOTPFEMNRQBPCAUXUZM"
# fac = 4
# arr = []
# for i in range(fac):
#     col = text[i::fac]
#     arr.append(col)

# counter = [Counter(a) for a in arr]
# most_freq = [c.most_common(1)[0] for c in counter]

# print(f"counter is {counter}\n\n\n")
# print(f"most_freq is {most_freq}")

# key = ""
# for obj in most_freq:
#     char = obj[0]
#     new_char = ALPH_REV[(ALPH[char] - ALPH["E"]) % 26]
#     key += new_char

#print(key)
print(vigenere("./data/vigenere.json", False))