import sys
from pyspark import SparkContext    # pylint: disable=wrong-import-position,import-error
from pyspark import SparkConf       # pylint: disable=wrong-import-position,import-error
from pyspark.sql import SQLContext  # pylint: disable=wrong-import-position,import-error
from pyspark.sql.types import *     # lgtm [py/polluting-import]  pylint: disable=wrong-import-position,import-error,wildcard-import
from pyspark.sql.types import StructType, StructField  # pylint: disable=wrong-import-position,import-error

csv_file = sys.getenv('csv')
parquet_dir = sys.getenv('parquet_dir')
# module = __import__('pyspark.sql.types', globals(), locals(), ['types'], -1)

conf = SparkConf().setAppName('CSV => Parquet')
sc = SparkContext(conf=conf) # pylint: disable=invalid-name
sc.setLogLevel('WARN')
sqlContext = SQLContext(sc)  # pylint: disable=invalid-name
spark_version = sc.version

df = sqlContext.read.format('com.databricks.spark.csv').options(header=header_str, inferschema='true').load(csv_file)
# df = sqlContext.read.format('com.databricks.spark.csv').options(header=header_str).load(csv_file, schema=self.schema)
df.write.parquet(parquet_dir)

df = sqlContext.load(source="com.databricks.spark.csv", path=csv_file, header=header_str, inferSchema='true')
# df = sqlContext.load(source="com.databricks.spark.csv", path=csv_file, header=header_str, schema=schema)
df.saveAsParquetFile(parquet_dir)

