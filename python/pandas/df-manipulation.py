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

