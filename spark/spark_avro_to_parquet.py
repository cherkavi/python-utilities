import sys
from pyspark import SparkContext    # pylint: disable=wrong-import-position,import-error
from pyspark import SparkConf       # pylint: disable=wrong-import-position,import-error
from pyspark.sql import SQLContext  # pylint: disable=wrong-import-position,import-error



avro_file = sys.getenv('avro')
parquet_dir = sys.getenv('parquet_dir')

conf = SparkConf().setAppName('Avro => Parquet')
sc = SparkContext(conf=conf) # pylint: disable=invalid-name
sc.setLogLevel('WARN')
sqlContext = SQLContext(sc)  # pylint: disable=invalid-name
spark_version = sc.version

df = sqlContext.read.format('com.databricks.spark.avro').load(avro_file)
df.write.parquet(parquet_dir)
