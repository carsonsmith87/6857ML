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
            

class OTP:

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
