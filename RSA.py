from sympy import randprime
import random
from utility import plaintext_to_blockvalue, block_to_plaintext
import os

class RSA:
    def __init__(self, key_size=180):
        self.key_size = key_size
        self.e = None
        self.d = None
        self.n = None

    def gcd(self, a, b):
        while a != 0:
            a, b = b % a, a
        return b

    def extended_gcd(self, a, b):
        if a == 0:  # base
            return (b, 0, 1)
        g, y, x = self.extended_gcd(b % a, a)  # recc
        return (g, x - (b // a) * y, y)

    def mod_inverse(self, a, m):
        g, x, _ = self.extended_gcd(a, m)
        if g != 1:  # not exists
            raise Exception('Modular inverse not exists!')
        return x % m

    def generate_key(self):
        self.p = randprime(2**(self.key_size - 1), 2**self.key_size)
        self.q = randprime(2**(self.key_size - 1), 2**self.key_size)
        self.n = self.p*self.q
        self.toitent_euler = (self.p - 1) * (self.q - 1)

        while True:
            self.e = random.randrange(2 ** (self.key_size - 1), 2 ** self.key_size)
            if (self.gcd(self.e, self.toitent_euler) == 1):
                break
        # self.d = pow(self.e, -1, self.toitent_euler)
        self.d = self.mod_inverse(self.e, self.toitent_euler)

    def save_key(self, path, e, n, d):
        pub = open(path + ".pub", "w")
        pub.write(str(e) + " " + str(n))
        pub.close()
        pri = open(path + ".pri", "w")
        pri.write(str(d) + " " + str(n))
        pri.close()

    def load_public_key(self, path):
        f = open(path, "r")
        pub = f.read().split(" ")
        f.close()
        self.e = int(pub[0])
        self.n = int(pub[1])

    def load_private_key(self, path):
        f = open(path, "r")
        pri = f.read().split(" ")
        f.close()
        self.d = int(pri[0])
        self.n = int(pri[1])

    def encrypt(self, plaintext, e, n):
        pt = plaintext_to_blockvalue(plaintext)
        res = []
        for block in pt:
            mi = pow(int(block), e, n)
            res.append(str(hex(mi)))
        return res

    def decrypt(self, ciphertext, d, n):
        res = []
        for block in ciphertext:
            res.append(pow(block, d, n))
        res = block_to_plaintext(res)
        return res

if __name__ == "__main__":
    RSA = RSA()
    # rsa.load_public_key("rsa.pub")
    # rsa.load_private_key("rsa.pri")
    f = open("test.txt", "rb")
    pt = (f.read())
    f.close()
    ct = RSA.encrypt(pt, RSA.e, RSA.n)
    RSA.decrypt(ct, RSA.d,RSA.n)
    # temp = rsa.encrypt(999)
    # rsa.decrypt(temp)