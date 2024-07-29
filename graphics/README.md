# Graphics, plot, visualize tables 
## Jupyter graph
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

## [Ploty](https://plotly.com/python/)
> show graphics in browser 
```py
# pip3 install plotly
import plotly.express as px
import pandas as pd

# Your data
D05 = [3000, 3200, 2900, 3400, 3100, 3150]
D10 = [4100, 4300, 3900, 4200, 4250, 3250]
D15 = [2100, 2300, 2900, 2200, 2450, 2250]

# Combine the data into a DataFrame
data = {
    'Value': D05 + D10 + D15,
    'Category': ['D05'] * len(D05) + ['D10'] * len(D10) + ['D15'] * len(D15)
}

df = pd.DataFrame(data)

# Create the box plot
fig = px.box(df, x='Category', y='Value', title="Box Plot for D05, D10, and D15")
fig.show()
```