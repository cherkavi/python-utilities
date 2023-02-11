import sys
from pyspark import SparkContext    # pylint: disable=wrong-import-position,import-error
from pyspark import SparkConf       # pylint: disable=wrong-import-position,import-error
from pyspark.sql import SQLContext  # pylint: disable=wrong-import-position,import-error

json_file = sys.getenv('json')
parquet_dir = sys.getenv('parquet_dir')

conf = SparkConf().setAppName('JSON => Parquet')
sc = SparkContext(conf=conf) # pylint: disable=invalid-name

sc.setLogLevel('WARN')
sqlContext = SQLContext(sc)  # pylint: disable=invalid-name
spark_version = sc.version

# df = sqlContext.read.json(json_file) # pylint: disable=invalid-name
# df.write.parquet(parquet_dir)

df = sqlContext.jsonFile(json_file) # pylint: disable=invalid-name
df.saveAsParquetFile(parquet_dir)
