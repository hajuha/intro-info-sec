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
    return libnum.generate_prime(bitsize)


def generate_coprime(phiN):
    while True:
        e = random.randint(0, phiN)

        if gcd(e, phiN) != 1:
            e = random.randint(0, phiN)
        else:
            break
    return e


def find_primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p-1) // p1

    # test random g's until one is found that is a primitive root mod p
    while(1):
        g = random.randint(2, p-1)
        # g is a primitive root if for all prime factors of p-1, p[i]
        # g^((p-1)/p[i]) (mod p) is not congruent to 1
        if not (pow(g, (p-1)//p1, p) == 1):
            if not pow(g, (p-1)//p2, p) == 1:
                return g


def generate_keys():
    print("------------------------------------")
    print("\nGENERATE KEY PAIR\n")
    p = generate_primes(bitsize)
    alpha = find_primitive_root(p)
    a = random.randint(1, (p - 1) // 2)
    beta = pow(alpha, a, p)
    print("Prime numbers:")
    print("   p: %d" % (p))
    print("Primitive root:")
    print("   α: %d" % (alpha))
    print("Private key:")
    print("   a: %d" % (a))
    print("Public key β = α ^ a mod p:")
    print("   β: %d" % (beta))

    print("\nPublic key (p, α, β):")
    print("   (%d, %d, %d)" % (p, alpha, beta))
    print("Private key a:")
    print("   %d" % (a))

    return (p, alpha, a, beta)


def encrypt(x, keys):

    print("------------------------------------")
    print("\nENCRYPTION\n")
    print("Plaintext = %d" % x)
    p, alpha, a, beta = keys

    k = generate_coprime(p-1)
    print("Random k = %d" % k)

    gamma = pow(alpha, k, p)
    print(" δ = x * β ^ k mod p = %d" % gamma)

    delta = (x*pow(beta, k, p)) % p
    print(" γ = a^k mod p = %d" % delta)

    print("Cyphertext: (γ,δ) = (%d, %d)" % (gamma, delta))
    return (gamma, delta)


def decrypt(cyphertext, keys, x):
    print("------------------------------------")
    print("\nDECRYPTION\n")
    p, alpha, a, beta = keys
    gamma, delta = cyphertext

    _x = (delta * pow(pow(gamma, a, p), p-2, p)) % p

    print("Plaintext = δ * (γ ^ -a) mod p = %d" % x)
    print("Decrypt: %s" % ("SUCCESS" if _x == x else "FALSE"))


def sign(x, keys):
    print("------------------------------------")
    print("\nSIGN\n")
    p, alpha, a, beta = keys
    k = generate_coprime(p-1)
    print("Random k = %d" % k)
    r = pow(alpha, k, p)
    print(" r = alpha * k ^ k mod p = %d" % r)
    
    s = ((x-a*r) * findModInverse(k, p-1)) % (p - 1)
    print(" s = (x - a * r) * (k ^ -1 mod (p - 1)) = %d\n" % s)
    print("Signature (r,s) = (%d, %d)" % (r,s))
    return (r,s)

def verify_signature(signature, keys, x):
    print("------------------------------------")
    print("\nVERIFY SIGNATURE\n")
    p, alpha, a, beta = keys
    r,s = signature
    v1 = pow(alpha, x, p)
    v2 = pow(beta, r , p) * pow(r, s, p) % p
    print("Verification: %s" % ("TRUE" if v1 == v2 else "FALSE"))

if __name__ == '__main__':
    bitsize = 512
    x = 123
    if (len(sys.argv) > 1):
        x = int(sys.argv[1])
        bitsize = int(sys.argv[2])
    keys = generate_keys()
    cyphertext = encrypt(x, keys)
    decrypt(cyphertext, keys, x)
    signature = sign(x, keys)
    verify_signature(signature, keys, x)
