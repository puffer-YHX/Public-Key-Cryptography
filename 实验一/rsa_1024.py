import secrets
from math import gcd

def is_prime(n, rounds= 20):
    """Miller-Rabin素性检测"""
    if rounds < 20:
        raise ValueError("Miller-Rabin检测轮数不能少于20")

    if n < 2:
        return False
    if n in (2,3):
        return True
    if n % 2 ==0:
        return False

    for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        composite = True
        for _ in range(s - 1):

            x = x * x % n
            if x == n - 1:
                composite = False
                break

        if composite:
            return False

    return True

def gen_prime(bits):
    """生成一个恰好bits位的素数"""

    if bits < 2:
        raise ValueError("素数位数不能少于2")

    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1))
        candidate |= 1
        if is_prime(candidate):
            return candidate

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

#加密函数
def rsa_encrypt(m, e, n):
    if not 0 <= m < n:
        raise ValueError("明文整数必须满足 0 <= m < n")
    return pow(m, e, n)

#解密函数
def rsa_decrypt(c, d, n):
    if not 0 <= c < n:
        raise ValueError("密文整数必须满足 0 <= c < n")
    return pow(c, d, n)

def rsa_keygen(bits):

    if bits < 32:
        raise ValueError("RSA密钥位数至少为32")

    e = 65537

    while True:
        p = gen_prime(bits // 2)
        q = gen_prime(bits // 2)

        if p == q:
            continue

        n = p * q

        if n.bit_length() != bits:
            continue

        phi = (p - 1) * (q - 1)

        if gcd(e, phi) != 1:
            continue

        g, x, y = extended_gcd(e, phi)
        d = x % phi

        return n, e, d

if __name__ == "__main__":
    # 测试素数检测函数
    tests = [(0, False), (1, False), (2, True), (3, True), (4, False), (561, False), (1105, False), (104729, True), (2 ** 61 - 1, True), (3215031751, False)]

    for num, expect in tests:
        got = is_prime(num)
        flag = "OK " if got == expect else "FAIL"
        print(f"{flag} is_prime({num}) = {got:<5} (expected {expect})")
    
    print("/n开始生成1024位RSA密钥...")

    n, e, d = rsa_keygen(1024)

    print("n的位数:",n.bit_length())
    print("公钥指数e:",e)

    m = 65
    c = rsa_encrypt(m, e, n)
    recovered = rsa_decrypt(c, d, n)

    assert n.bit_length() == 1024
    assert recovered == m

    print("明文m: ", m)
    print("密文c: ", c)
    print("解密结果: ", recovered)
    print("1024位RSA加解密验证通过")