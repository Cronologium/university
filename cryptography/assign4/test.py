from math import sqrt

a = [0]
b = [1]
x = [0]
b2 = [0]
n = int(raw_input('n='))

a.append(int(sqrt(n)))
b.append(int(sqrt(n)))
x.append(sqrt(n) - a[-1])
b2.append(b[-1] * b[-1] - n)

for i in range(2, 8):
    a.append(int(1 / x[i-1]))
    x.append(1 / x[i-1] - a[i])
    b.append(a[i] * b[i-1] + b[i-2])
    crt = (b[i] * b[i]) % n
    if crt > n / 2:
        crt -= 8057
    b2.append(crt)

print (a)
print (b)
print (x)
print (b2)