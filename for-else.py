for each in range(5):
    print(each)
else:
    print("else without break")


for each in range(5):
    if each==3:
        break
    print(each)
else:
    print("else for break")
