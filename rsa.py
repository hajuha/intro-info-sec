import sys
import libnum
import random
import time


def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def findModExp(base, e, mod):
    X = base
    E = e
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X * X) % mod
            E = E/2
        else:
            Y = (X * Y) % mod
            E = E - 1
    return Y


def generate_primes(bitsize):
    while True:
        p = libnum.generate_prime(bitsize)
        q = libnum.generate_prime(bitsize)

        if p == q:
            q = libnum.generate_prime(bitsize)
        else:
            break
    return p, q


def generate_coprime(phiN):
    while True:
        e = random.randint(0, phiN)

        if gcd(e, phiN) != 1:
            e = random.randint(0, phiN)
        else:
            break
    return e


if __name__ == '__main__':
    bitsize = 512

    if (len(sys.argv) > 1):
        x = int(sys.argv[1])
        bitsize = int(sys.argv[2])
    time_start = time.time()
    p, q = generate_primes(bitsize)
    N = p*q
    phiN = (p-1)*(q-1)
    e = 65537
    d = findModInverse(e, phiN)
    c = pow(x, e, N)
    _x = pow(c, d, N)

    print("\nPrime numbers:")
    print("   p: %d" % (p))
    print("   Length: %d bits, Digits: %d" %
          (libnum.len_in_bits(p), len(str(p))))
    print("   q: %d" % (q))
    print("   Length: %d bits, Digits: %d\n" %
          (libnum.len_in_bits(q), len(str(q))))
    print("Prime N:")
    print("   N = p*q = %d." %
          (N))
    print("   Length: %d bits, Digits: %d\n" %
          (libnum.len_in_bits(N), len(str(N))))
    print("   Φ(N) = (p-1)*(q-1): %d." %
          (phiN))
    print("   Length: %d bits, Digits: %d\n" %
          (libnum.len_in_bits(phiN), len(str(phiN))))
    print("e: %d. Length: %d bits, Digits: %d\n" %
          (e, libnum.len_in_bits(e), len(str(e))))
    print("d = e^-1 mod N: %d." %
          (d))
    print("Length: %d bits, Digits: %d" %
          (libnum.len_in_bits(d), len(str(d))))

    print('\n-----------------------------------------------------\n')

    print('GENERATE RSA KEY PAIR\n')
    print("Public key")
    print("  (e,N): (%d, %d)\n" % (e, N))
    print("Private key")
    print("  (d,N): (%d, %d)\n" % (d, N))
    time_spent = time.time() - time_start
    print("Spent time: %.3f sec." % time_spent)

    print('-----------------------------------------------------\n')

    print("ENCRYPTION\n")
    print("Plaintext: %d. Length: %d bits, Digits: %d\n" %
          (x, libnum.len_in_bits(x), len(str(x))))
    time_start = time.time()
    print("Encrypt - Ciphertext")
    print("   c = x ^ e mod n = ", c)
    print("   Length: %d bits, Digits: %d\n" %
          (libnum.len_in_bits(c), len(str(c))))
    print("Decrypt. Plaintext: %d. Length: %d bits, Digits: %d\n\n" %
          (_x, libnum.len_in_bits(_x), len(str(_x))))
    time_spent = time.time() - time_start
    print("Spent time: %.3f sec." % time_spent)

    print('-----------------------------------------------------\n')

    print("SIGN AND VERIFY\n")
    print("Plaintext: %d. Length: %d bits, Digits: %d\n" %
          (x, libnum.len_in_bits(x), len(str(x))))
    time_start = time.time()
    s = pow(x, e, N)
    print('Signature')
    print("   s = x ^ e mod n = %d" %
          (s))
    print("   Length: %d bits, Digits: %d\n" %
          (libnum.len_in_bits(s), len(str(s))))
    _s = pow(s, d, N)
    print("Verification: _s = s ^ d mod n = %d  %s" % (_s, "TRUE" if _s == x else "FALSE"))
    time_spent = time.time() - time_start
    print("Spent time: %.3f sec." % time_spent)
