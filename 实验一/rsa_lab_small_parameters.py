from math import gcd

p = 61
q = 53

n = p * q
phi = (p-1) * (q-1)

e = 17

print("n =", n)
print("phi(n) =", phi)
print("gcd(e,phi(n)) =",gcd(e,phi))

def extended_gcd(a,b):

    if b == 0:
        return a,1,0

    g,x1,y1 = extended_gcd(b,a%b)
    x = y1
    y = x1 - (a//b) * y1
    return g,x,y

g,x,y = extended_gcd(e,phi)
d = x % phi

print("扩展欧几里得结果：",g,x,y)
print("d =", d)
print("(d * e) % phi =",(d * e) % phi)

def rsa_encrypt(m,e,n):
    if not 0 <= m < n:
        raise ValueError("明文整数必须满足 0 <= m < n")
    return pow(m, e, n)

def rsa_decrypt(c,d,n):
    if not 0<= c ,n:
        raise ValueError("密文整数必须满足 0 <= c < n")
