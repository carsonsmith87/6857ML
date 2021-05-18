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
        #num_to_char[PRINTS_LEN] = '-'
        #num_to_char[PRINTS_LEN+1] = '_'
        #num_to_char[PRINTS_LEN+2] = ' '
        #num_to_char[PRINTS_LEN+2] = '!'
        #char_to_num['-'] = PRINTS_LEN
        #char_to_num['_'] = PRINTS_LEN+1
        #char_to_num[' '] = PRINTS_LEN+2
        #char_to_num['!'] = PRINTS_LEN+2

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
        rand_nums = random.sample(range(self.mod), k=length)
        rand_chars = [self.num_to_char[num] for num in rand_nums]
        self.secret_key = ''.join(rand_chars)

    def get_key_mod(self, key, length):

        return (key * (int(length/len(key))+1))[:length]

    def encrypt(self, text):
    
        key_mod = self.get_key_mod(self.secret_key, len(text))
        enc_nums = [(self.char_to_num[text[i]] + self.char_to_num[key_mod[i]]) % self.mod for i in range(len(text))]
        result = [self.num_to_char[num] for num in enc_nums]
        return ''.join(result)

    def decrypt(self, text):

        key_mod = self.get_key_mod(self.secret_key, len(text))
        dec_nums = [(self.char_to_num[text[i]] - self.char_to_num[key_mod[i]]) % self.mod for i in range(len(text))]
        result = [self.num_to_char[num] for num in dec_nums]
        return ''.join(result)

    def is_elgamal(self):
        return False

vernam_cipher = VernamCipher(7)
for i in range(10):
    enc = vernam_cipher.encrypt('azazazazazazazazlalalamimimfafadadnksljfnvrlhtbnvjgtkrrvcdnltgvmqpkdjvmf')
    if vernam_cipher.decrypt(enc) != 'azazazazazazazazlalalamimimfafadadnksljfnvrlhtbnvjgtkrrvcdnltgvmqpkdjvmf':
        print('boo')


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








    
