# pandas

## df manipulation

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/pandas/df-manipulation.py) -->
<!-- The below code snippet is automatically added from ../../python/pandas/df-manipulation.py -->
```py
# https://pandas.pydata.org/
#
import pandas as pd
import numpy as np
import matplot as plt
import scipy.stats as stats
import seaborn

data_frame: pd.DataFrame = pd.read_csv("data.csv")
print(data_frame.columns)
print(data_frame.dropna())

print("# take subset of the DataFrame")
print(data_frame[["head-3", "head-2"]])
print("# rename column")
data_frame.rename(columns={"head-1": "head-001"}, inplace=True)
# for one column - don't use 'columns'
# data_frame.rename("head-1", inplace=True)

print(data_frame)
print("# print types")
print(data_frame.dtypes)
print("# change one of the column to specific type")
print(data_frame["head-2"].astype("str"))

print("standard deviation:", data_frame["head-001"].std())
print("average:", data_frame["head-001"].mean())

print("# divide values to categories, binning, categorization")
bins = np.linspace(min(data_frame["head-001"]), max(data_frame["head-001"]), 3)
data_frame["categories"] = pd.cut(data_frame["head-001"], bins, labels=["low", "high"], include_lowest=True)
print(data_frame)

print("# one-hot encoding")
print(pd.get_dummies(data_frame["categories"]))

print("# descriptive statistics")
print(data_frame)
print("## describe")
print(data_frame.describe())
print("## value counts")
print(data_frame["head-001"].value_counts())

# plt.scatter(data_frame["index"], data_frame["values"]
# plt.title, plt.xlabel, plt.ylabel

print("# group by")
sub_set_df = data_frame[["head-001", "price", "head-2"]].dropna()
print(sub_set_df.groupby(["head-2"], as_index=False).mean())
print("# pivot")
pivot_df = sub_set_df.pivot(index="price", columns="head-001")
print(pivot_df)

# plt.pcolor(pivot_df, cmap="RdBu")
# plt.colorbar()
# plt.show()

# stats.f_oneway

print("# correlation between two values")
print(seaborn.regplot(x="head-001", y="price", data=data_frame))

pearson_koef, p_value = stats.pearsonr(data_frame["price"], data_frame["head-001"])
print("Pearson Correlation: ", pearson_koef, p_value)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## fetching_tweet

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/pandas/fetching_tweet.py) -->
<!-- The below code snippet is automatically added from ../../python/pandas/fetching_tweet.py -->
```py
import pandas as pd
from datetime import datetime as dt

# Here we should fetch our data from the Twitter API but since now we have to
# apply for getting API's credentials we pass this step for the sake of the tutorial.
# We use data.csv as source of tweets.

LOCAL_DIR='/tmp/'

def main():
	# Create the dataframe from data.csv
	tweets = pd.read_csv('/home/airflow/airflow_files/data.csv', encoding='latin1')

	# Fomat time using pd.to_datetime and drop the column Row ID
	tweets = tweets.assign(Time=pd.to_datetime(tweets.Time)).drop('row ID', axis='columns')

	# Export the dataframe into a new csv file with the current date
	tweets.to_csv(LOCAL_DIR + 'data_fetched.csv', index=False)

if __name__ == '__main___':
	main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## pandas example

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/pandas/pandas-example.py) -->
<!-- The below code snippet is automatically added from ../../python/pandas/pandas-example.py -->
```py
import pandas as pd

my_data = { 
    "names":["petya", "vasya", "kolya"], 
    "age":[40, 51, 23], 
    "position":["senior", "pension", "junior"], 
    }

# pd.read_csv
print("create DataFrame from dictionary")
data_frame:pd.DataFrame = pd.DataFrame(data = my_data)
print(data_frame)

print("unique values from ")
print(data_frame["position"].unique())

print("get data by index")
print(data_frame.iloc[0,0])

print("subset of original DataFrame ")
print(data_frame.iloc[1:,0:2])

print("unique values from column")
print(data_frame["age"].unique())

print("take subset of DataFrame by condition")
print( data_frame[data_frame["age"]>39] )
print( data_frame[data_frame.age>39] )
```
<!-- MARKDOWN-AUTO-DOCS:END -->


