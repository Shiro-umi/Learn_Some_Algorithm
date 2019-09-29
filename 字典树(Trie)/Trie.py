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
        dic[True] = {}
        
for word in str_list:
    build_trie(root, word)
        
print(root)


s = "ababcde"
res = []

def compare(p2, p1):
    if s[p2] in p1:
        return compare(p2+1, p1[s[p2]])
    else:
        if True in p1:
            return (True, p2)
        else:
            return (False, p2)
            
for p3 in range(len(s)):
    succ, p2 = compare(p3, root)
    if succ:
        res.append(s[p3:p2])

print(res)

