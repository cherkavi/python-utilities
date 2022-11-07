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