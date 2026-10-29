import random


def is_prime(n, rounds= 20):
    """Miller-Rabin素性检测"""

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
        a = random.randrange(2, n-1)
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
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1))
        candidate |= 1
        if is_prime(candidate):
            return candidate

if __name__ == "__main__":
    # 测试素数检测函数
    tests = [(0, False), (1, False), (2, True), (3, True), (4, False), (561, False), (1105, False), (104729, True), (2 ** 61 - 1, True), (3215031751, False)]

    for num, expect in tests:
        got = is_prime(num)
        flag = "OK " if got == expect else "FAIL"
        print(f"{flag} is_prime({num}) = {got:<5} (expected {expect})")