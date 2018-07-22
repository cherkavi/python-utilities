print(">>> all <<<") 
# ---

# True 
print(all([True,True,True]))

# True 
print(all([1,2,3]))

# True 
print(all(["one", "two", "three"]))

# False 
print(all(["one", None, "two", "three"]))

# False 
print(all([1,0,2,3]))



print(">>> any <<<") 
# ---

# True 
print(any([True,False,False]))

# True 
print(any([None,None,3]))

# True 
print(any(["one", "two", "three"]))

# False 
print(all([None, None, None, ]))

# False 
print(any([0,0,0,0]))


print(">>> enumerate <<<")
# ---
print(list(enumerate([100,101,102,103,104,105,106,107], start = 3 )))


print(">>> filter <<<") 
# ---

