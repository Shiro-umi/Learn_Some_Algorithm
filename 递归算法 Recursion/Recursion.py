myself = 10    # 我有10点血

def punch_someone(who):     # 打人循环
    if who:
        who -= 1
        print(who)
        punch_someone(who)
    else:
        print("die")

punch_someone(myself)   # 我打我自己

##############################################################

# # Definition for a binary tree node.
# # class TreeNode:
# #     def __init__(self, x):
# #         self.val = x
# #         self.left = None
# #         self.right = None

# class Solution:
#     def inorderTraversal(self, root: TreeNode) -> List[int]:
        
#         res = []
#         def travel(root):
#             if root:
#                 res.append(root.val)   # 此处返回 前序遍历
#                 travel(root.left)
#                 # res.append(root.val)   此处返回 中序遍历
#                 travel(root.right)
#                 # res.append(root.val)   此处返回 后序遍历
#             else:
#                 return
        
#         travel(root)
        
#         return res


##############################################################


# # Definition for a binary tree node.
# # class TreeNode(object):
# #     def __init__(self, x):
# #         self.val = x
# #         self.left = None
# #         self.right = None

# class Solution(object):

#     def buildTree(self, preorder, inorder):
#         """
#         :type preorder: List[int]
#         :type inorder: List[int]
#         :rtype: TreeNode
#         """
#         if len(inorder) == 0:
#             return None
#         root = TreeNode(preorder[0])        # 前序遍历第一个值为根节点
#         mid = inorder.index(preorder[0])        # 因为没有重复元素，所以可以直接根据值来查找根节点在中序遍历中的位置
#         root.left = self.buildTree(preorder[1:mid+1], inorder[:mid])        # 构建左子树
#         root.right = self.buildTree(preorder[mid+1:], inorder[mid+1:])        # 构建右子树
        
#         return root
