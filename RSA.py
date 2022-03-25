from sympy import randprime
import random

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
        pt = plaintext.split(",")
        res = []
        for block in pt:
            res.append(pow(int(block), e, n))
        return res

    def decrypt(self, pt, d, n):
        res = []
        for block in pt:
            res.append(pow(int(block), d, n))
        return res