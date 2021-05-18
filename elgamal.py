import random
import time

LOWER_LARGE = pow(10, 15)

class ElGamal:

    def __init__(self):
        self.pk = None
        
    def generate_key(self):

        q = random.randint(pow(LOWER_LARGE,2), pow(LOWER_LARGE, 3))
        a = q
        start = time.time()
        while self.gcd(a, q) != 1:
            a = random.randint(LOWER_LARGE, q)
            
        k = q
        while self.gcd(k, q) != 1:
            k = random.randint(LOWER_LARGE, q)

        #print(time.time()-start)

        g = random.randint(2, q)
        return [q,g,a,k]

    def generate_keys(self, num_data, repeat):
        result = []
        while len(result) < num_data:
            keys = self.generate_key()
            for i in range(repeat):
                result.append(keys)
                if len(result) >= num_data:
                    break
        return result
                

    def gcd(self, i, j):

        if j > i:
            return self.gcd(j,i)
        elif i % j == 0:
            return j
        return self.gcd(j, i % j)


    def encrypt_one(self, text, key):

        [q,g,a,k] = key
        h = pow(g,a,q)
        self.pk = pow(g,k,q)
        sk = pow(h,k,q)

        return [str(sk * ord(letter)) for letter in text]

    def encrypt(self, data, repeat):

        result = []
        all_keys = self.generate_keys(len(data), repeat)
        for i in range(len(data)):
            text = data[i]
            key = all_keys[i]
            result.append(''.join(self.encrypt_one(text, key)))
        return result


    def decrypt(self, enc):

        sk = pow(self.pk, self.sender_key, self.q)
        return ''.join([chr(int(int(enc_letter)/sk)) for enc_letter in enc])

    def is_elgamal(self):
        return True


#elgamal = ElGamal()
#enc = elgamal.encrypt('lemon', 0.9)
#print(enc)
#print(''.join(enc))
#print(elgamal.decrypt(enc))

        

