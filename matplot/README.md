# Jupyter graph
```sh
pip3 install matplotlib
```

```python
import matplotlib.pyplot as plt

plt.title("My Title")
plt.xlabel("x-axis label")
plt.ylabel("y-axis label")
```

```py
x=[1,2,3,4,5,6,7,8]
y=[2,4,6,8,10,12,14,16]

plt.plot(x,y)
# plt.bar(x,y)
# plt.scatter(x,y)
# 
plt.show()
```

```py
x=[4,9,16,25,36]
fig = plt.figure(figsize =(9, 5)) # line 4

# plt.pie(x)
plt.pie(x, labels=("Guavas", "Berries","Mangoes","Apples", "Avocado"), colors = ( "#a86544", "#eb5b13", "#ebc713", "#bdeb13", "#8aeb13"))

plt.show()
```

