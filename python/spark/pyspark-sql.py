# pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql import SparkSession   

table_path = "/mapr/prod.zurich/vantage/data/store/processed/marker"
temp_table_name = "marker_table_01"

spark = SparkSession.builder.getOrCreate()  
schema = StructType([StructField("session_id", StringType()), StructField("marker_source", StringType())])
df = spark.lookupFromMapRDB(table_path, schema)
df.createOrReplaceTempView(temp_table_name)
df2 = df.filter("session_id = '9fc13577-8834-43f4-ad80-01747cb89f84' ")
df2 = spark.sql("select * from "+temp_table_name+" limit 5")  
df2.show()  

