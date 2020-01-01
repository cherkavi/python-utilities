# https://pandas.pydata.org/
#
import pandas as pd
import numpy as np

data_frame: pd.DataFrame = pd.read_csv("data.csv")
print(data_frame.columns)
print(data_frame.dropna())

# rename column
data_frame.rename(columns={"head-1": "head-001"}, inplace=True)
print(data_frame)
# print types
print(data_frame.dtypes)
# change one of the column to specific type
print(data_frame["head-2"].astype("str"))

print("standard deviation:", data_frame["head-001"].std())
print("average:", data_frame["head-001"].mean())

# divide values to categories, binning, categorization
bins = np.linspace(min(data_frame["head-001"]), max(data_frame["head-001"]), 3)
data_frame["categories"] = pd.cut(data_frame["head-001"], bins, labels=["low", "high"], include_lowest=True)
print(data_frame)

# one-hot encoding
print(pd.get_dummies(data_frame["categories"]))
