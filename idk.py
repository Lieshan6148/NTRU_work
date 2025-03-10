from random import shuffle, getrandbits
from Crypto.Util.number import *
from sage import PolynomialRing

Zx = PolynomialRing(ZZ, 'x')
x = Zx.gen()


def convolution(f, g, R):
    return (f * g) % R


def balancedmod(f, q, R):
    g = list(map(lambda x: ((x + q//2) % q) - q//2, f.list()))
    return Zx(g) % R


def random_poly(n, d1, d2):
    assert d1 + d2 <= n
    result = d1 * [1] + d2 * [-1] + (n - d1 - d2) * [0]
    shuffle(result)
    return Zx(result)


def invert_poly_mod_prime(f, R, p):
    T = Zx.change_ring(Integers(p)).quotient(R)
    return Zx(lift(1 / T(f)))


def invert_poly_mod_powerof2(f, R, q):  #  f 在模 2^16 下的逆
    g = invert_poly_mod_prime(f, R, 2)
    e = log(q, 2)
    for i in range(1, e):
        g = ((2 * g - f * g ** 2) % R) % q
    return g


class NTRUCipher:
    def __init__(self, N, p, q, d):
        self.N = N
        self.p = p
        self.q = q
        self.d = d
        self.R = x ** N - 1
        # key generation
        self.g = random_poly(self.N, d, d)
        # self.g = x^119 - x^115 - x^112 + x^111 + x^110 - x^106 + x^103 - x^101 + x^100 - x^99 + x^98 - x^97 - x^96 + x^95 - x^90 + x^89 - x^88 - x^86 + x^85 + x^83 + x^82 + x^75 - x^74 + x^69 - x^64 + x^62 + x^58 + x^57 + x^54 - x^51 + x^50 - x^45 - x^42 + x^41 - x^40 - x^38 + x^37 - x^36 - x^35 - x^34 - x^32 - x^31 + x^30 - x^29 - x^27 + x^26 + x^25 + x^22 + x^20 - x^18 + x^16 + x^15 - x^14 - x^13 + x^12 - x^8 + x^7 + x^6 - x^4 - x
        while True:
            try:
                self.f = random_poly(self.N, d + 1, d)
                # self.f = x^119 + x^117 + x^114 - x^113 - x^112 - x^110 - x^109 + x^108 + x^107 - x^106 - x^103 - x^102 + x^100 + x^98 + x^97 + x^96 - x^93 + x^92 + x^91 - x^87 + x^85 - x^81 + x^80 - x^75 - x^73 + x^72 - x^71 + x^68 - x^67 - x^66 - x^62 - x^60 - x^57 + x^52 - x^51 + x^50 - x^48 + x^45 - x^43 - x^42 - x^38 + x^37 - x^34 + x^31 + x^30 - x^26 + x^24 + x^22 - x^21 + x^20 - x^17 + x^16 - x^14 - x^13 + x^12 + x^10 + x^8 + x^7 + x^6 - x^5 + x
                self.fp = invert_poly_mod_prime(self.f, self.R, self.p)
                self.fq = invert_poly_mod_powerof2(self.f, self.R, self.q)
                break
            except:
                pass

        self.h = balancedmod(self.p * convolution(self.fq, self.g, self.R), self.q, self.R)
    def getPubKey(self):
        return self.h
    def encrypt(self, m):
        r = random_poly(self.N, self.d, self.d)
        return balancedmod(convolution(self.h, r, self.R) + m, self.q, self.R)

    def decrypt(self, c):
        a = balancedmod(convolution(c, self.f, self.R), self.q, self.R)
        return balancedmod(convolution(a, self.fp, self.R), self.p, self.R)

    def encode(self, val):
        poly = 0
        for i in range(self.N):
            poly += ((val % self.p) - self.p // 2) * (x ** i)
            val //= self.p
        return poly

    def decode(self, poly):
        result = 0
        ll = poly.list()
        for idx, val in enumerate(ll):
            result += (val + self.p // 2) * (self.p ** idx)
        return result

    def poly_from_list(self, l: list):
        return Zx(l)


if __name__ == '__main__':
    N = 160
    d = 30
    p = 3
    q = 65536

    flag = b'cnss{}'
    cipher = NTRUCipher(N, p, q, d)
    # cipher.f = x^31 - x^29 + x^28 - x^27 + x^26 + x^25 + x^24 + x^23 + x^22 - x^21 - x^19 - x^18 + x^17 - x^15 - x^14 - x^11 - x^9 + x^8 - x^6 + x^2 + x
    # cipher.g = -x^31 - x^30 - x^29 - x^28 + x^27 + x^25 - x^23 + x^22 + x^21 - x^19 + x^18 + x^15 - x^13 + x^11 - x^10 - x^9 + x^6 - x^5 + x^2 + x
    
    # print("[Pk]---------")
    h = cipher.getPubKey()
    msg = bytes_to_long(flag)
    encode_msg = cipher.encode(msg)
    c = cipher.encrypt(encode_msg)
    # print(f'c={c}')
    mm = cipher.decrypt(c)
    decode_msg = cipher.decode(mm)
    assert decode_msg == msg