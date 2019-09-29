
# 计数区间
n = 100
# 初始化计数列表
isPrime = [True for i in range(n)]
# 初始化指针
p1 = 2
while p1**2 < n:
    if isPrime[p1]:
        p2 = p1
        while p2*p1 < n:
            isPrime[p2*p1] = False
            p2 += 1
    p1 += 1
print(isPrime.count(True)-2)


