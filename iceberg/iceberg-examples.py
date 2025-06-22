import pandas as pd

# pip install --break-system-packages "pyiceberg[pandas, sql-sqlite]"

# DataFrame - data organized into named columns similar to an SQL table.
#   DataSet - strongly-typed version of a DataFrame, where each row of the Dataset 
from pandas import DataFrame

from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import StringType, IntegerType, NestedField

import sqlite3
import os
import shutil

## input data 
my_data = { 
    "names":["petya", "vasya", "kolya"], 
    "age":[40, 51, 23], 
    "position":["senior", "pension", "junior"], 
    }
data_frame:pd.DataFrame = pd.DataFrame(data = my_data)

schema = Schema(
    NestedField(field_id=1,name='names',field_type=StringType(),required=False),
    NestedField(field_id=2,name="age",field_type=IntegerType(),required=False),
    NestedField(field_id=3,name="position",field_type=StringType(),required=False),
)


## iceberg catalog 
warehouse_path = "/tmp/warehouse"
warehouse_is_new:bool=False
if os.path.exists(warehouse_path):
    # shutil.rmtree(warehouse_path)
    warehouse_is_new=False
else:
    os.makedirs(warehouse_path)
    warehouse_is_new=True

warehouse_catalog_db=f"/{warehouse_path}/pyiceberg_catalog.db"
with sqlite3.connect(warehouse_catalog_db) as connection:
    pass

catalog = load_catalog(
    "default",
    **{
        'type': 'sql',
        "uri": f"sqlite://{warehouse_catalog_db}",
        "warehouse": f"file://{warehouse_path}",
    },
)

## iceberg fill 
if warehouse_is_new:
    catalog.create_namespace("default") 
    table = catalog.create_table(
        "default.people",
        schema=schema
    )
else:
    table = catalog.load_table(
        "default.people")

table.append(table.scan().to_arrow())
