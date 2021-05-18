import numpy as np
from string import ascii_uppercase, printable, ascii_lowercase
import random

#constants
ALPH_LEN = 26
PRINTS_LEN = 62

def generate_conversion_dicts(is_alphabet = False):
    
    if is_alphabet:
        mod = ALPH_LEN 
        char_to_num = {letter: index for index, letter in enumerate(ascii_uppercase)}
        num_to_char = {index: letter for index, letter in enumerate(ascii_uppercase)}

    else:
        mod = PRINTS_LEN
        char_to_num = {letter: index for index, letter in enumerate(printable[:mod])}
        num_to_char = {index: letter for index, letter in enumerate(printable[:mod])}

    return mod, char_to_num, num_to_char

    
    
class CaesarCipher:
    
    def __init__(self):

        self.mod, self.char_to_num, self.num_to_char = generate_conversion_dicts()

        self.shift = int(np.random.rand()*self.mod)

    def encrypt(self, text):

        result = [self.num_to_char[(self.char_to_num[char] + self.shift) % self.mod] for char in text]
        return ''.join(result)

    def decrypt(self, text):

        result = [self.num_to_char[(self.char_to_num[char] - self.shift) % self.mod] for char in text]
        return ''.join(result)

    def is_elgamal(self):
        return False

caesar_cipher = CaesarCipher()
for i in range(10):
    enc = caesar_cipher.encrypt('azazazazazazazazlalalamimimfafadadnksljfnvrlhtbnvjgtkrrvcdnltgvmqpkdjvmf')
    if caesar_cipher.decrypt(enc) != 'azazazazazazazazlalalamimimfafadadnksljfnvrlhtbnvjgtkrrvcdnltgvmqpkdjvmf':
        print('boo')


class VernamCipher:

    def __init__(self, length):

        self.mod, self.char_to_num, self.num_to_char = generate_conversion_dicts()
            
        self.length = length

    def gen_keys(self, num_data, repeat):

        result = []
        while len(result) < num_data:
            rand_nums = random.sample(range(self.mod), k=self.length)
            rand_chars = [self.num_to_char[num] for num in rand_nums]
            sk = ''.join(rand_chars)
            for i in range(repeat):
                result.append(sk)
                if len(result) >= num_data:
                    break
        return result

    def get_key_mod(self, key, length):

        return (key * (int(length/len(key))+1))[:length]

    def encrypt_one(self, text, key):
    
        key_mod = self.get_key_mod(key, len(text))
        enc_nums = [(self.char_to_num[text[i]] + self.char_to_num[key_mod[i]]) % self.mod for i in range(len(text))]
        result = [self.num_to_char[num] for num in enc_nums]
        return ''.join(result)

    def decrypt_one(self, text, key):

        key_mod = self.get_key_mod(key, len(text))
        dec_nums = [(self.char_to_num[text[i]] - self.char_to_num[key_mod[i]]) % self.mod for i in range(len(text))]
        result = [self.num_to_char[num] for num in dec_nums]
        return ''.join(result)

    def encrypt(self, data, repeat):

        num_data = len(data)
        secret_keys = self.gen_keys(num_data, repeat)

        result = []
        for i in range(len(data)):
            text = data[i]
            key = secret_keys[i]
            result.append(self.encrypt_one(text, key))
        return result
            

    def is_elgamal(self):
        return False

vernam_cipher = VernamCipher(50)
l = ['lemon' for i in range(500)]
#print(vernam_cipher.encrypt(l, 0.9)[400:])



class PermuteThenVernam(VernamCipher):

    def __init__(self, length):

        self.vernam = VernamCipher(length)

    def encrypt(self, text):

        permute = random.randint(0, len(text)-1)
        new_text = text[permute:]+text[:permute]
        return self.vernam.encrypt(new_text)

    def is_elgamal(self):
        return False


class VernamThenPermute(VernamCipher):

    def __init__(self, length):

        self.vernam = VernamCipher(length)

    def encrypt(self, text):

        enc_text = self.vernam.encrypt(text)
        permute = random.randint(0, len(enc_text)-1)
        return enc_text[permute:]+enc_text[:permute] 

    def is_elgamal(self):
        return False


#text = 'lemon'
#for i in range(10):
#    permute = random.randint(0, len(text)-1)
#    new_text = text[permute:]+text[:permute]
#    print(new_text)








    
