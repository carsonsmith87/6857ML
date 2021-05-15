from encryption import *
from encrypt_data import *

#encryption schemes
caesar_cipher = CaesarCipher()
vernam_cipher = OTP(KEY_LEN)

#generate data
raw_data = get_data()
caesar_data = get_data(caesar_cipher)
vernam_data = get_data(vernam_cipher)

print("Raw data: \n", raw_data)
print("Caesar data: \n", caesar_data)
print("Vernam data: \n", vernam_data)
