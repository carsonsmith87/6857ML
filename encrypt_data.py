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

#Read CSV files.
def get_data(enc_class = None):
    result = []
    
    for file in file_paths:
        data = pd.read_csv(file).sample(NUM_DATA)
        col = data.columns[0]
        data = list(data[col])
        data = [col + text for text in data]
        if enc_class != None:
            data = [enc_class.encrypt(text) for text in data]
        result += data
        
    return result


caesar_cipher = CaesarCipher()
vernam_cipher_7 = OTP(7)
vernam_cipher_10 = OTP(10)

#caesar_data = get_data(caesar_cipher)
#vernam_7_data = get_data(vernam_cipher_7)
#vernam_10_data = get_data(vernam_cipher_10)

#print(len(caesar_data), len(vernam_7_data), len(vernam_10_data))

#pd.DataFrame({'Caesar':caesar_data}).to_csv('CaesarCipher.csv', index=False)
#pd.DataFrame({'Vernam7':vernam_7_data}).to_csv('VernamCipher7.csv', index=False)
#pd.DataFrame({'Vernam10':vernam_10_data}).to_csv('VernamCipher10.csv', index=False)


