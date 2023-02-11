import sys
from pyspark import SparkContext    # pylint: disable=wrong-import-position,import-error
from pyspark import SparkConf       # pylint: disable=wrong-import-position,import-error
from pyspark.sql import SQLContext  # pylint: disable=wrong-import-position,import-error

json_file = sys.getenv('json')
avro_dir = sys.getenv('avro_dir')

conf = SparkConf().setAppName('Json => Avro')
sc = SparkContext(conf=conf) # pylint: disable=invalid-name
sqlContext = SQLContext(sc)  # pylint: disable=invalid-name
df = sqlContext.read.json(json_file)
df.write.format('com.databricks.spark.avro').save(avro_dir)
