# sudo apt install python3-pandas
# pip3 install --break-system-packages pyarrow
# pip3 install --break-system-packages fastparquet
import pandas as pd

# DataFrame - data organized into named columns similar to an SQL table.
#   DataSet - strongly-typed version of a DataFrame, where each row of the Dataset 
from pandas import DataFrame
from pandas import Series

my_data = { 
    "names":["petya", "vasya", "kolya"], 
    "age":[40, 51, 23], 
    "position":["senior", "pension", "junior"], 
    }

# pd.read_csv
print("\n---\ncreate DataFrame from dictionary")
data_frame:pd.DataFrame = pd.DataFrame(data = my_data)
print(data_frame)

print("\n---\nunique values from ")
print(data_frame["position"].unique())

print("\n---\nget data by index")
print(data_frame.iloc[0,0])

print("\n---\nsubset of original DataFrame ")
print(data_frame.iloc[1:,0:2])

print("\n---\nunique values from column")
print(data_frame["age"].unique())

print("\n---\ntake subset of DataFrame by condition")
print( data_frame[data_frame["age"]>39] )
print( data_frame[data_frame.age>39] )

print("\n---\nsave to parquet file")
parquet_file = 'people.parquet'
data_frame.to_parquet(parquet_file, index=False)

print("\n---\nread parquet file")
data_frame:DataFrame = pd.read_parquet(parquet_file)
data_frame.info()

# Series
print("\n---\nSeries type")
series_a: Series = pd.Series([1, 2, 3], index=['a', 'b', 'c'     ])
series_b: Series = pd.Series([   4, 5, 6], index=[  'b', 'c', 'd'])
sum_series: Series = series_a + series_b 
print(sum_series)