
# 计数区间
n = 100
# 初始化计数列表
isPrime = [True for i in range(n)]
# 初始化指针
p1 = 2
while p1**2 < n:
    p2 = p1**2
    while p2 < n:
        isPrime[p2] = False
        p2 += p1
    p1 += 1
print(isPrime.count(True)-2)


