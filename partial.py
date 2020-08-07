# partial function
from functools import partial
def func(u,v,w,x):
    return u*4 + v*3 + w*2 + x

another_function = partial(func, 1,2,3)

print(another_function(4))
