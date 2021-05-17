import csv
from encryption import *


#constants
KEY_LEN = 10
NUM_DATA = 500
file_paths = ['data/passwords.csv', 'data/products.csv', 'data/usernames.csv']


#Read CSV files.
def get_data(enc_class = None):
    data = []
    for file in file_paths:
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    col_name = row[0]
                    line_count += 1
                elif line_count <= NUM_DATA:
                    raw_data = col_name + row[0]
                    if enc_class == None:
                        data.append(raw_data)
                    else:
                        data.append(enc_class.encrypt(raw_data))
                    line_count += 1
                else:
                    break
    if enc_class == None:
        p,w,n = "PASSW", "USERN", "PRODU"
    else:
        p,w,n = enc_class.encrypt("PASSW"), enc_class.encrypt("USERN"), enc_class.encrypt("PRODU")
    return data,p,w,n
