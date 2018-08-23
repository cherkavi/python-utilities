# shallow copy 
a = {1: [1,2,3]}
b = a.copy()
a[1].append(4)
print(a)
# {1: [1, 2, 3, 4]}
print(b)
# {1: [1, 2, 3, 4]}


import copy
# deep copy
a = {1: [1,2,3]}
b = copy.deepcopy(a)
a[1].append(4)
print(a)
# {1: [1, 2, 3, 4]}
print(b)
# {1: [1, 2, 3]}
