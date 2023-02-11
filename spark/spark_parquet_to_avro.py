import sys
from pyspark import SparkContext    # pylint: disable=wrong-import-position,import-error
from pyspark import SparkConf       # pylint: disable=wrong-import-position,import-error
from pyspark.sql import SQLContext  # pylint: disable=wrong-import-position,import-error

parquet_file = sys.getenv('parquet')
avro_dir = sys.getenv('avro_dir')

conf = SparkConf().setAppName('Parquet => Avro')
sc = SparkContext(conf=conf) # pylint: disable=invalid-name

sc.setLogLevel('WARN')
sqlContext = SQLContext(sc)  # pylint: disable=invalid-name

df = sqlContext.read.parquet(parquet_file)
df.write.format('com.databricks.spark.avro').save(avro_dir)
