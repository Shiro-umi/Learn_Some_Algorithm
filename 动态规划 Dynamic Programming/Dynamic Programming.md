>听起来很高深的动态规划其实一点都不高深  
># 不严谨白话动态规划  
>~~又不是不能用~~  
  
# 1.什么是动态规划  
第一次听到动态规划很多人都觉得是一个很高深的东西，又动态又规划听起来很niup，但事实上它是个纸老虎。  
考虑下面问题： 
>计算100以内的质数 => 参考：[质数筛选算法 Sieve of Eratosthenes](https://github.com/Shiro-umi/Learn_Some_Algorithm/blob/master/%E8%B4%A8%E6%95%B0%E7%AD%9B%E9%80%89%E7%AE%97%E6%B3%95%20Sieve%20of%20Eratosthenes/Sieve%20of%20Eratosthenes.md )  

**(这道题并不是标准的动态规划，仅仅是个引例，具体的解题思路在上面的链接)**
首先我们知道两数(非01)乘积一定不为质数，按照一般的思路，我们计算质数的时候如果靠暴力遍历的话会存在大量的冗余。比如： 
```python

p1 = 3
p2 = 9      # p2 = p1**2 
p1 * p2 = 27

p1 = 2
p2 = 15
p1 * p2 = 30

p1 = 3
p2 = 10     # p2 += 1
p1 * p2 = 30
```  
假设质数标记为`True`非质数标记为`False`，经过观察不难发现：当`p2 += 1`的时候，`3*10`的结果已经被`2*15`标记为`False`了，而`动态规划`就是为了解决这种困境的。  
所谓`动态规划`用最简单的说法来解释就是：  
**通过已知状态来推断下一个状态，不考虑任何无关状态以达到减少冗余计算的目的**  

# 2.动态规划的思想  
理解一个算法最重要的是理解它的`思想`。尤其对那些看上去不那么直观的算法来说尤为重要，动态规划也是如此。  
回顾我们上面对动态规划的解释，我们发现我们需要解决的问题一共有两个：  
- 如何表示`状态`
- 如何使用`已知状态`推断`未来状态`
继续思考上面质数的例子，我们的状态只有`p1*p2的结果`是否在求解范围中(共两种，在或者不在)，所以只需要用一个一维List去记录这个状态就可以了：  
```python
n = 100     # 计数区间
isPrime = [True for i in range(n)]      # 初始化计数列表
```
那么如何使用已知状态推断未来状态呢？参考以下实现：
```python  
n = 100     
isPrime = [True for i in range(n)]     
p1 = 2      
while p1**2 < n:
    if isPrime[p1]:     #   在这停顿！
        p2 = p1
        while p2*p1 < n:
            isPrime[p2*p1] = False
            p2 += 1
    p1 += 1

print(isPrime.count(True)-2)
```
仔细思考上面实现中的注释行，不难发现在这里判断了当前的第一个乘数`x`是否为质数，因为如果不是质数的话，它的倍数一定已经被标记为`False`了(不是质数就意味着`x`是两个比它小的数的乘积，乘积一定不为质数)，所以就没有必要再继续遍历`x`的倍数了。  
这个时候有人要有话说了：**你这不就是给循环条件加了个判断吗？**  
没错，但这正是动态规划的基本思想。
  
# 3.动态规划问题的一般求解方法  
如果够细心可能已经发现问题了：  
上面的例子中，只完成了表示状态，但并没有使用已知状态直接得到未来状态，反而是未来状态建立在一个基于已知状态的函数的基础上。按照这种思路表示上面的实现：  
```python  
n = 100     
isPrime = [True for i in range(n)]     
p1 = 2      
while p1**2 < n:
    if isPrime[p1]:     
        f(p1,p2)    #   推断未来状态
    p1 += 1

print(isPrime.count(True)-2)
```
可以给f(p1,p2)起一个高大上的名字：  
**状态转移方程**  
结合上面的分析不难看出使用动态规划问题我们只需要： 
- 表示状态
- 状态转移方程

两个要素就可以解决问题。  
  
思考下面例题：  => 参考：[LeetCode@5 最长回文子串](https://github.com/Shiro-umi/Do_Some_Algorithm_Test/blob/master/LeetCode%405%20%E6%9C%80%E9%95%BF%E5%9B%9E%E6%96%87%E5%AD%90%E4%B8%B2/Algorithm.md) 
>给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。 
>  
>示例 1：  
>输入: "babad"  
>输出: "bab"  
>注意: "aba" 也是一个有效答案。  
>  
>示例 2：  
>输入: "cbbd"  
>输出: "bb"  

首先引出回文的性质：**回文串的两边各自+1相同的字符得到的结果必定是回文**  
我们以`s`中的每一个字符作为坐标，建立一个`size*size`的二位DP矩阵表示`s[L:R]`的状态。将状态初始化为`False`表示非回文。那么根据上面的性质不难推断出如果`DP[L][R] == True`，那么当`s[L-1] == s[R+1]`的时候就能直接得出`s[L+1:R+1]`的状态为`True`。另一个特殊情况 ，`R-L <= 2`的时候只要`s[l] == s[R]`那么`s[L:R]`就一定为回文。  
那么我们的状态转移方程就可以进行如下表示：  
```python 
if s[L] == s[R] and (R-L <= 2 or dp[L+1][R-1]):
    dp[L][R] = True
```
而中间提到的DP矩阵其实就是我们的状态表示：
```python  
dp = [[False for _ in range(size)] for _ in range(size)]
```
参考以下实现：(这里只解释动态规划的相关内容，详细解题思路参考上面的链接)
```python  
class Solution:   
    def longestPalindrome(self, s: str) -> str:

        size = len(s)
        if size <= 1:
            return s
        
        longest = 1
        res = s[0]
        dp = [[False for _ in range(size)] for _ in range(size)]
        
        for R in range(1, size):
            for L in range(R):
                if s[L] == s[R] and (R-L <= 2 or dp[L+1][R-1]):
                    dp[L][R] = True
                    (longest, res) = (R-L, s[L:R+1]) if R+1-L > longest else (longest, res)
        
        return res
```
上面这道题是一道比较经典的动态规划题目，通过这道题可以比较直观地表现出动态规划的思想。  
在这里可以发现，我们的状态转移方程直接通过已知状态得到了未来状态，而无需关心其他的任何状态。  
