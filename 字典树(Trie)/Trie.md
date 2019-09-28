>本文基于labuladong公众号文章    
># 游戏中的敏感词过滤是如何实现的 | 什么是字典树（Trie）    
>结合自己对于字典树理解的总结  
  
# 1.什么是字典树(Trie)    
字典树是一种树结构，又称单词查找树，其特点是通过共享单词的前缀节点来实现压缩存储空间的目的。    
eg. 单词"ab","ac","bc"可以压缩为如 <font color=red>*Figure 1*</font> 表示的结构：    
  
![*Figure 1*](http://shiroumi.com/static/wtf_site_app/static_sources/essay_img/1.jpg)  
  
对于上面树结构进行解释：  
    1.树的跟节点为root(空)  
    2.从root出发，root的所有child表示所有<font color=red>存在于字典中的</font>单词的<font color=red>第一个字母</font>
    3.逐级向下查找最终找到或找不到目标单词  
    4.若目标单词中存在包含关系如：''ab'',''a''，其中''a''也为目标单词，但被目标单词"ab"包含这种情况下应对''a''节点做一个标记，若目标单词在树中遍历到''a''节点停止，则匹配成功  
  
# 2.构建字典树  
对于字典树的构建，一般情况下采用HashMap作为载体  
使用HashMap的原因在于HashMap可以在O(1)时间内定位到下一个节点  
        **~~毕竟这玩意在python里面就叫字典~~**
首先给出关键词的列表定义：  
`str_list = ['abc','abd','bcd','ab']`  
既然决定了要使用HashMap构建字典树，在开始之前我们现需要生成一个root节点：  
`root = {}`  
在生成了跟节点后面临两个遍历方式：  
1.按树的层级遍历  
2.按每个单词的路径遍历  
直觉上来说第二个方法容易一些，事实上也确实是这样。如果按照1方法来做的话，需要一个记录层级的外部辅助变量，还需要在每一个node下记录这个node下面应该有哪些单词，实现起来相对麻烦。所以这里采用方法2进行构建。  
按方法2的思路，首先给出我们对于每个单词的构建方法：  
```  
def build_trie(dic, word):  
    pass  
```  
(为什么需要这两个参数后面会提到)  
其中<font color=red>dic</font>代表当前的层级，<font color=red>word</font>代表当前构建中的单词然后遍历str_list调用构建方法build_trie()  
```  
for word in str_list:  
    build_trie(root, word)  
```  
接下来思考build_trie()的内部如何实现：  
首先在实现这个方法的时候要明确，每一次调用build_trie()都只对一层进行操作。在这一层中，层数是等价于单词中char的索引的。所以我们的方法应该在每一层只对word中对应的char进行判断，若这个当前层没有char这个节点，则添加一个名叫"char"的节点，之后继续向下层递归，递归的对象  为当前层级的HashMap以及除去已操作过的char的word：  
```  
if word[0] not in dic:  
    dic[word[0]] = {}  
    build_trie(dic[word[0]], word[1:]  
```  
否则跳过生成直接将对应节点作为新的递归对象：  
```  
else:  
    build_trie(dic[word[0]], word[1:])  
```  
  
下面给出完整代码作为参考：  
```  
str_list = ['abc','abd','bcd',"ab"]  
root = {}  
  
def build_trie(dic, word):  
    if word:  
        if word[0] not in dic:  
            dic[word[0]] = {}   
            build_trie(dic[word[0]], word[1:])  
        else:  
            build_trie(dic[word[0]], word[1:])  
    else:  
        dic[True] = {}        # 考虑单词的包含情况，给每个单词的结束添加标记  
          
for word in str_list:  
    build_trie(root, word)  
          
print(root)  
```  
得到如下结果：  
```  
{  
    'a': {  
        'b': {  
            'c': {  
                True: {}  
            },  
            'd': {  
                True: {}  
            },  
            True: {}  
        }  
    },  
    'b': {  
        'c': {  
            'd': {  
                True: {}  
            }  
        }  
    }  
  
}  
```  
  
# 3.基于字典树的关键词匹配  
现在我们构造完了字典树，接下来就可以使用字典树的结构在字符串里面匹配目标了。  
现在假设我们的匹配串为  
        # "ababcde"  
首先需要考虑我们需要多少个标记才能完成关键词的遍历和截取？  
![*Figure 2*](http://shiroumi.com/static/wtf_site_app/static_sources/essay_img/2.png)  
比较的时候我们需要一个指针p1指向树结构的节点，另外一个指针p2指向当前遍历到的序列节点，但只有这两个指针只能找到单词在序列中的结束位置，所以还需要另外一个指针p3指向当前子序列的开始位置，这样$\color{red}{p2到p3之间的序列}$就是我们的匹配内容。  
![*Figure 3*](http://shiroumi.com/static/wtf_site_app/static_sources/essay_img/3.png)  
特别值得一提的是，若遇到包含关系的时候，需要先确定短序列不是目标词，再判断长序列 。若短序列为目标词，则直接返回True。  
![*Figure 4*](http://shiroumi.com/static/wtf_site_app/static_sources/essay_img/4.png)  
现在思考 <font color=red>*Figure 4*</font> 的情况，p2指向的字符不在p1中，但之前的"a"，"b"都已经完成了匹配，也就是说在p2之前的序列全部匹配成功。  
在这种情况下，只需要判断p1中是否存在我们之前生成的结尾标记True。若存在则将匹配成功标记返回，则子序列"ab"完成匹配。  
若p2指向的字符在p1中存在，按正常的匹配逻辑则会自动忽略短序列。  
  
下面考虑实现方式：  
首先我们需要一个p3作为开始位置的索引：  
```  
for p3 in range(len(s)):  
    pass  
```  
然后我们要在这个循环中进行p2和p1的匹配，则设一个函数：  
```  
def compare(p2, p1):  
    pass  
```  
在这个函数中我们需要考虑所有可能发生的情况：  
1.p2的元素在p1中，则p2向后移动1，p1指向Trie中p2元素的位置  
2.p2的元素不在p1中，这个时候如果没有字串目标的话就应该返回False了，但是因为目标之间存在包含关系，则需要按照 $\color{blue}{*Figure 4*}$的逻辑判断当前的截断是否为目标串，根据情况返回True或False  
  
下面给出完整代码供参考：  
```  
s = "ababcde"  
res = []  
  
def compare(p2, p1):  
    if s[p2] in p1:  
        return compare(p2+1, p1[s[p2]])  
    else:  
        if True in p1:                    # figure 4 中的情况  
            return (True, p2)  
        else:  
            return (False, p2)  
              
for p3 in range(len(s)):  
    succ, p2 = compare(p3, root)  
    if succ:  
        res.append(s[p3:p2])  
  
print(res)  
```  
输出结果：  
`['ab', 'abc', 'bcd']`  
  
# 4.字典树的典型应用  
最典型的应用就是搜索引擎的关键字联想  
![*Figure 5*](http://shiroumi.com/static/wtf_site_app/static_sources/essay_img/5.png)  
或者参考文章中提到的敏感词屏蔽等  
  