import csv
from encryption import *
from elgamal import *
import pandas as pd


#constants
KEY_LEN = 10
NUM_DATA = 500
#REPEAT = 10
file_paths = ['data/passwords.csv', 'data/products.csv', 'data/usernames.csv']


#data = pd.read_csv("data/Passwords.csv").sample(10)
#print(data.columns[0])
#print(list(data["PASSWORD"]))

#Cleans text from random charactehmrs.
def is_valid(text):
    return not(('!' in text) or (' ' in text) or ('-' in text) or ('_' in text))

    
#Read CSV files.
def get_data(repeat, enc_class = None):
    result = []
    
    for file in file_paths:
        data = pd.read_csv(file)#.sample(NUM_DATA)
        col = data.columns[0]
        data = list(data[col])

        raw_data = []
        text_idx = 0
        while len(raw_data) < NUM_DATA:
            
            text = data[text_idx]
            if is_valid(text):
                text_add = col + text
                raw_data.append(text_add)
            text_idx += 1
        result += raw_data

    if enc_class is None:
        return result

    return enc_class.encrypt(result, repeat)

        
vernam_cipher = VernamCipher(50)
el_gamal = ElGamal()

elgamal_data_250 = get_data(250, el_gamal)
vernam_data_250 = get_data(250, vernam_cipher)
pd.DataFrame({'ElGamal250':elgamal_data_250}).to_csv('encrypted_data/ElGamal250.csv', index=False)
pd.DataFrame({'Vernam250':vernam_data_250}).to_csv('encrypted_data/Vernam250.csv', index=False)

elgamal_data_1 = get_data(1, el_gamal)
vernam_data_1 = get_data(1, vernam_cipher)
pd.DataFrame({'ElGamal1':elgamal_data_1}).to_csv('encrypted_data/ElGamal1.csv', index=False)
pd.DataFrame({'Vernam1':vernam_data_1}).to_csv('encrypted_data/Vernam1.csv', index=False)

elgamal_data_500 = get_data(500, el_gamal)
vernam_data_500 = get_data(500, vernam_cipher)
pd.DataFrame({'ElGamal500':elgamal_data_500}).to_csv('encrypted_data/ElGamal500.csv', index=False)
pd.DataFrame({'Vernam500':vernam_data_500}).to_csv('encrypted_data/Vernam500.csv', index=False)

elgamal_data_10 = get_data(10, el_gamal)
vernam_data_10 = get_data(10, vernam_cipher)
pd.DataFrame({'ElGamal10':elgamal_data_10}).to_csv('encrypted_data/ElGamal10.csv', index=False)
pd.DataFrame({'Vernam10':vernam_data_10}).to_csv('encrypted_data/Vernam10.csv', index=False)

elgamal_data_50 = get_data(50, el_gamal)
vernam_data_50 = get_data(50, vernam_cipher)
pd.DataFrame({'ElGamal10':elgamal_data_50}).to_csv('encrypted_data/ElGamal50.csv', index=False)
pd.DataFrame({'Vernam10':vernam_data_50}).to_csv('encrypted_data/Vernam50.csv', index=False)






#caesar_cipher = CaesarCipher()
#vernam_cipher_7 = VernamCipher(7)
#vernam_cipher_10 = VernamCipher(10)
#vernam_permute = VernamThenPermute(13)
#permute_vernam = PermuteThenVernam(13)

#raw_data = get_data()
#print(get_data(vernam_cipher)[1400:])
#caesar_data = get_data(caesar_cipher)
#vernam_7_data = get_data(vernam_cipher_7)
#vernam_10_data = get_data(vernam_cipher_10)
#vernam_permute_data = get_data(vernam_permute)
#permute_vernam_data = get_data(permute_vernam)


#print(len(get_data()), len(caesar_data), len(vernam_7_data), len(vernam_10_data))

#pd.DataFrame({'Raw':raw_data}).to_csv('encrypted_data/RawData.csv', index=False)
#pd.DataFrame({'Caesar':caesar_data}).to_csv('encrypted_data/CaesarCipher.csv', index=False)
#pd.DataFrame({'Vernam7':vernam_7_data}).to_csv('encrypted_data/VernamCipher7.csv', index=False)
#pd.DataFrame({'Vernam10':vernam_10_data}).to_csv('encrypted_data/VernamCipher10.csv', index=False)
#pd.DataFrame({'VernamThenPermute':vernam_permute_data}).to_csv('encrypted_data/VernamThenPermute.csv', index=False)
#pd.DataFrame({'PermuteThenVernam':permute_vernam_data}).to_csv('encrypted_data/PermuteThenVernam.csv', index=False)
#pd.DataFrame({'ElGamal':elgamal_data}).to_csv('encrypted_data/ElGamal.csv', index=False)



