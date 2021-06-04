import sys
import libnum
import random
import time
import hashlib
import collections
from libnum import ecc


def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    if a == 0:
        raise ZeroDivisionError("division by zero")
    if a < 0:
        # k ** -1 = p - (-k) ** -1  (mod p)
        return m - findModInverse(-a, m)
    # if gcd(a, m) != 1:
    #     return None
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


def point_add(curve, point1, point2):
    p, a, b = curve
    if point1 is None:
        # 0 + point2 = point2
        return point2
    if point2 is None:
        # point1 + 0 = point1
        return point1
    x1, y1 = point1
    x2, y2 = point2
    if x1 == x2 and y1 != y2:
        # point1 + (-point1) = 0
        return None
    if x1 == x2:
        # This is the case point1 == point2.
        m = (3 * x1 * x1 + a) * findModInverse(2 * y1, p)
    else:
        # This is the case point1 != point2.
        m = (y1 - y2) * findModInverse(x1 - x2, p)
    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % p, -y3 % p)
    return result


def scalar_multiply(curve, c, d, point):
    result = None
    addend = point
    while d:
        if d & 1:
            # Add.
            result = point_add(curve, result, addend)
        # Double.
        addend = point_add(curve, addend, addend)
        d >>= 1
    assert c.check(result)
    return result


def generate_elliptic_curve(bitsize):
    p, a, b = (0, 0, 0)
    p = libnum.generate_prime(bitsize)

    while ((4*a**3 + 27 * b ** 2) % p == 0):
        a = random.randint(0, p-1)
        b = random.randint(0, p-1)
    print("Elliptic Curve: y^2 = x^3 + %dx + %db (mod%d)" % (a, b, p))
    return(p, a, b)


def gerenate_keys(curve):
    p, a, b = curve

    c = ecc.Curve(a, b, p)
    randX = len(c.find_points_in_range(1, 20))//2

    g = c.find_points_in_range(1, 20)[randX]
    n = c.get_order(g)
    d = random.randint(0, n)
    print("Private key:")
    print("  d = %d" % d)
    Q = scalar_multiply(curve, c, d, g)
    print("Public key:")
    print("  Elliptic Curve (p, a, b) = (%d, %d, %d)" % (p, a, b))
    print("  Base point g = (%d, %d)" % (g))
    print("  Subgroup order n = %d" % (n))
    print("  Q = (%d, %d)" % (Q))

    private_key = d
    public_key = (g, n, Q)
    return private_key, public_key


def sign_message(k, private_key, public_key, message, curve):
    p, a, b = curve
    _curve = ecc.Curve(a, b, p)
    (g, n, Q) = public_key
    message_hash = hashlib.sha512(message).digest()
    z = int.from_bytes(message_hash, "big")
    r = 0
    s = 0
    while not r or not s:
        if k == 0:
            k = random.randrange(1, n - 1)
        x, _ = scalar_multiply(curve, _curve, k, g)  # _:y
        r = x % n
        c = findModInverse(k, n)
        s = ((z + r * private_key) * c) % n
    print("\nSignature:")
    print("  r = %d" % r)  # 'sigR' in bitcoin transaction.
    print("  s = %d" % s)
    return (r, s, z)


def verify_signature(public_key, signature, curve):
    p, a, b = curve
    c = ecc.Curve(a, b, p)
    (g, n, Q) = public_key
    r, s, z = signature
    w = findModInverse(s, n)
    print(w)
    u1 = (z * w) % n
    u2 = (r * w) % n
    x, _ = point_add(curve, scalar_multiply(curve, c, u1, g),
                     scalar_multiply(curve, c, u2, Q)
                     )
    if (r % n) == (x % n):
        return True  # Signature matches!
    else:
        return False  # Invalid signature!


message = b'abcd'
time_start = time.time()
bitsize = int(sys.argv[1])
curve = generate_elliptic_curve(bitsize)
private_key, public_key = gerenate_keys(curve)
signature = sign_message(0, private_key, public_key, message, curve)
print("\nVerification: %s" %verify_signature(public_key, signature, curve))
time_spent = time.time() - time_start

print("Spent time: %.3f sec." % time_spent)
