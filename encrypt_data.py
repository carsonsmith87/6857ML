import csv
from encryption import *
import pandas as pd


#constants
KEY_LEN = 10
NUM_DATA = 500
file_paths = ['data/passwords.csv', 'data/products.csv', 'data/usernames.csv']


#data = pd.read_csv("data/Passwords.csv").sample(10)
#print(data.columns[0])
#print(list(data["PASSWORD"]))

#Cleans text from random characters.
def is_valid(text):
    return not(('!' in text) or (' ' in text) or ('-' in text) or ('_' in text))

    
#Read CSV files.
def get_data(enc_class = None):
    result = []
    
    for file in file_paths:
        data = pd.read_csv(file)#.sample(NUM_DATA)
        col = data.columns[0]
        data = list(data[col])

        file_result = []
        text_idx = 0
        while len(file_result) < NUM_DATA:
            
            text = data[text_idx]
            if is_valid(text):
                text_add = col + text
                if enc_class != None:
                    text_add = enc_class.encrypt(text_add)
                file_result.append(text_add)
            text_idx += 1

        result += file_result
    return result


caesar_cipher = CaesarCipher()
vernam_cipher_7 = OTP(7)
vernam_cipher_10 = OTP(10)

raw_data = get_data()
caesar_data = get_data(caesar_cipher)
vernam_7_data = get_data(vernam_cipher_7)
vernam_10_data = get_data(vernam_cipher_10)

#print(len(get_data()), len(caesar_data), len(vernam_7_data), len(vernam_10_data))

pd.DataFrame({'Raw':raw_data}).to_csv('encrypted_data/RawData.csv', index=False)
pd.DataFrame({'Caesar':caesar_data}).to_csv('encrypted_data/CaesarCipher.csv', index=False)
pd.DataFrame({'Vernam7':vernam_7_data}).to_csv('encrypted_data/VernamCipher7.csv', index=False)
pd.DataFrame({'Vernam10':vernam_10_data}).to_csv('encrypted_data/VernamCipher10.csv', index=False)


