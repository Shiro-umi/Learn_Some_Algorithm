>所有人都说递归的可解释性很强，好像只有我搞不明白？  
># 理性解释递归算法的套路  
  
# 1.什么是递归  
递归，顾名思义就理解不了。为啥叫这个名字我也不知道，不过意思就是一句话：  
**自己调用自己**  
用白话说就是：`想要想明白递归，首先你得想明白递归`  
比如：  
```python  

def recursion(wtf):
    ...
    recursion(wtf)
    ...
```  

# 2.关于递归的边界  
一个方法调用自己，在里面再调用自己，在里面...那岂不是永远也出不来了？  
按照递归的定义来讲确实如此，但事实上显然并不是这么简单的。举个例子：
```python  

myself = 10    # 我有10点血
def punch_someone(who):     
    if who:
        who -= 1
        print(who)
        punch_someone(who)      # 递归打人
    else:
        print("die")    # 打死了..

punch_someone(myself)   # 我打我自己
```  
让我们来看一下输出：  
```python  
9
8
7
6
5
4
3
2
1
0
die
```  
从上面的例子不难看出，为了避免出现鞭尸(不跳出循环)的情况，在递归算法中一定都会有一个**递归边界**的判断。  
在上面的例子里面，这个边界就是`if who:`，当血量为0的时候跳出递归。

# 3.关于递归的过程归纳  
还是参考上面`我打我自己`的例子，不难发现我们最终的目标是让`who`这个参数变为`0`，而我们的递归算法就是这个过程中的每一步。  
用通俗的说法解释一下就是，**递归方法的主体就是让大问题变小的一步过程**。  
在上面的例子中，`punch_someone()`方法就是每次打一拳，递归到下一层就变成了`who -= 1`，我们的问题就缩小了`1`。如果写成`who -= 2`，就是一次打两拳。  
当然在这个例子中的任务比较简单，在复杂的任务中需要根据不同的任务来完成**递归过程的归纳方法**，在这里先用一个`f(x)`表示。  
于是我们得到了如下形式的递归框架：  
```python  

x = 10      # 初始化参数
def recursion(x):     
    if x:       # 判断递归条件
        x -= f(x)       # 执行过程方法
        recursion(x)      # 递归调用
    else:
        print("not x")    

recursion(x)    # 递归入口
```  

# 4.递归算法的优缺点与数据结构的关系  
我们在使用递归算法的时候必须要想清楚一个事情：什么时候递归才是合适的。  
在这里就有必要谈一谈两种数据结构了：`树`和`链表`。  
按照递归的特性，上面两种数据结构都可以使用递归算法遍历，但并不是两种在大部分情况下都适合用递归方法遍历。
下面来考虑链表:
```python  
1 -> 2 -> 3 -> 4 -> ... -> (10**10)
```  
如果使用递归遍历上面的链表，思路还是和`我打我自己`的例子一样，每次将问题缩小1(`node.next`)，但仔细考虑一下就会发现不妥的地方，这个不妥反映出了**递归算法最大的缺点**。  
在我们使用递归遍历的过程中递归调用的主体是不会被释放的，也就是说我遍历到了`i`，区间`[0,i]`的所有递归主体都不会被释放，也就是说这个方法虽然在O(n)时间内完成了遍历，但也消耗了n倍的内存。  
所以对于链表我们只需要不停地`node.next`就可以完成全部遍历。**但是`树`呢？**  
以二叉树为例，考虑下面的二叉树： 
```
    3
   / \
  9  20
    /  \
   15   7
```   
在二叉树中每一个`node`都可能存在一个`node.left`和`node.right`，也就是说我们在遍历这个树的时候是存在分支的。这个时候我们就不能像链表一样使用简单的遍历去travel一个树结构。  
这个时候就体现出了递归的优势。

# 5.递归的简单应用 - 树的前,中,后序遍历  
首先说明一下三种遍历方式的区别：  
**前序遍历:**  根，左，右  
**中序遍历:**  左，根，右  
**后序遍历:**  左，右，根  
根据上述定义不难发现，所谓`前中后`其实指的是`根`节点在遍历顺序中的位置。  
所以在我们遍历的时候只需要分别在`递归左`之前，`递归右`之前，`递归右`之后返回当前节点就可以分别得到`前,中,后序遍历`的结果了。  
参考如下实现：  
```python  

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        
        res = []
        def travel(root):
            if root:
                res.append(root.val)   # 此处返回 前序遍历
                travel(root.left)
                # res.append(root.val)   此处返回 中序遍历
                travel(root.right)
                # res.append(root.val)   此处返回 后序遍历
            else:
                return
        
        travel(root)
        
        return res
```

# 6.相对复杂的例题分析  
本例题参考**LeetCode 105.从前序与中序遍历序列构造二叉树**  
>根据一棵树的前序遍历与中序遍历构造二叉树。  
>  
>注意:  
>你可以假设树中没有重复的元素。  
>  
>例如，给出  
>前序遍历 preorder = [3,9,20,15,7]  
>中序遍历 inorder = [9,3,15,20,7]  
>返回如下的二叉树：  
> 
>```python  
>    3  
>   / \  
>  9  20  
>    /  \  
>   15   7 
>```    
根据上一节了解的`前中后序遍历`的定义不难看出，前序遍历的第一个节点一定是`root`，而第二个节点一定是`root`左子树的`root`。而在中序遍历中，对于每一个节点其序列中**左边的节点一定在树结构中位于该节点的左边。**  
在上题中前序序列第一个节点为`3`，也就是说`3`就是整个树的`root`，那么要构造树结构的话就需要找到`3`的`左子树`和`右子树`分别构建。  
这个地方又回到了上面总结的递归框架，我们将棵树构建的问题转换为了更小的**构建左右子树**的问题。  
那么怎么确定节点`3`的左右子树呢？根据中序遍历的定义(左根右)很容易就能想到，在中序序列中`3`这个节点左边的序列就包含了左子树的全部节点，右侧同理。  
这么看来问题就迎刃而解了，我们每次从前序序列中取出一个节点，在当前递归主体内生成新的节点，分别让当前新节点的`left`和`right`分别等于对中序当前节点的左右序列，和前序序列的下一节点的递归值就可以了。递归边界就是当前序序列遍历到末尾的时候。  
参考实现如下：
```python  
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        
        def build(val, inorder):
            root = TreeNode(val)    # 构造新的节点
            L, R = [], []
            L, R = inorder[:inorder.index(root.val)], inorder[inorder.index(root.val):]     # 切分左右子树的集合
            if preorder and preorder[0] in L:       # 判断递归条件
                root.left = build(preorder.pop(0), L)       # 递归左子树
            if preorder and preorder[0] in R:       # 判断递归条件
                root.right = build(preorder.pop(0), R)      # 递归右子树
            return root     # 将包含当前节点左子树和右子树的节点root返回给上一层作为上一层的左或右子树
        
        if not len(preorder):
            return None
        else:
            return build(preorder.pop(0), inorder)
```

可以让代码变得更简洁一些：  
```python  
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):

    def buildTree(self, preorder, inorder):
        """
        :type preorder: List[int]
        :type inorder: List[int]
        :rtype: TreeNode
        """
        if len(inorder) == 0:
            return None
        root = TreeNode(preorder[0])        # 前序遍历第一个值为根节点
        mid = inorder.index(preorder[0])        # 因为没有重复元素，所以可以直接根据值来查找根节点在中序遍历中的位置
        root.left = self.buildTree(preorder[1:mid+1], inorder[:mid])        # 构建左子树
        root.right = self.buildTree(preorder[mid+1:], inorder[mid+1:])        # 构建右子树
        
        return root
```




