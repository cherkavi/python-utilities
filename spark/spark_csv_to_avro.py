import sys

from pyspark import SparkContext    # pylint: disable=wrong-import-position,import-error
from pyspark import SparkConf       # pylint: disable=wrong-import-position,import-error
from pyspark.sql import SQLContext  # pylint: disable=wrong-import-position,import-error
from pyspark.sql.types import *     # lgtm [py/polluting-import]  pylint: disable=wrong-import-position,import-error,wildcard-import
from pyspark.sql.types import StructType, StructField  # pylint: disable=wrong-import-position,import-error


csv_file = sys.getenv('csv')
avro_dir = sys.getenv('avro_dir')

conf = SparkConf().setAppName('CSV => Avro')
sc = SparkContext(conf=conf) # pylint: disable=invalid-name
sc.setLogLevel('WARN')
sqlContext = SQLContext(sc)  # pylint: disable=invalid-name
spark_version = sc.version

df = sqlContext.read.format('com.databricks.spark.csv').options(header=header_str, inferschema='true').load(csv_file)
# df = sqlContext.read.format('com.databricks.spark.csv').options(header=header_str).load(csv_file, schema=schema)

df.write.format('com.databricks.spark.avro').save(avro_dir)
