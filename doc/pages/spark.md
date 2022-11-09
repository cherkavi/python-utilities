# spark

## pyspark sql

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/spark/pyspark-sql.py) -->
<!-- The below code snippet is automatically added from ../../python/spark/pyspark-sql.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## spark test connection

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/spark/spark-test-connection.py) -->
<!-- The below code snippet is automatically added from ../../python/spark/spark-test-connection.py -->
```py
from pyspark import SparkContext

#sc = SparkContext("172.17.0.2", "test-app")
#sc = SparkContext("spark://172.17.0.2", "test-app")
#SparkConf().setAppName("App_Name").setMaster("spark://localhost:18080").set("spark.ui.port","18080");

try:
    sc = SparkContext("local", "test-app")
    print("------------")
    print(sc)
    print("------------")
finally:
    sc.stop()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## spark words count

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/spark/spark-words-count.py) -->
<!-- The below code snippet is automatically added from ../../python/spark/spark-words-count.py -->
```py
from pyspark import SparkContext
import re

sc:SparkContext = SparkContext("local","simple example")
sc.getConf().set("spark.hadoop.validateOutputSpecs", "false")

words = sc.textFile("words.txt").flatMap(lambda line: re.split(" |\n", line))

wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)

wordCounts.saveAsTextFile("output")
```
<!-- MARKDOWN-AUTO-DOCS:END -->


