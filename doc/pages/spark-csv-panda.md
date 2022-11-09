# spark-csv-panda

## spark csv matplot

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/spark-csv-panda/spark-csv-matplot.py) -->
<!-- The below code snippet is automatically added from ../../python/spark-csv-panda/spark-csv-matplot.py -->
```py
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import DataFrameReader
import requests, shutil


def download_file(url, local_path):
    ''' download file from remote url and save it to path '''
    response = requests.get(url, stream=True)
    with open(local_path, "wb") as output_file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, output_file)

try:
    output_image = "out.png"
    data_file = "tweets.csv"
    data_file_url = "http://waxy.org/random/misc/gamergate_tweets.csv"
    download_file(data_file_url, data_file)

    sc = SparkContext("local", "example-of-processing-data")
    sc.setLogLevel("ERROR")
    sqlContext = SQLContext(sc)

    tweets = sqlContext.read.format('com.databricks.spark.csv').options(header="true").load(data_file)

    tweets.createOrReplaceTempView("tweets")

    panda_df = sqlContext.sql(" select cast(tweet_count as int) tweet_count, count(user_id) users from (select count(tweet_id) tweet_count, user_id from tweets group by user_id ) group by tweet_count having tweet_count>5 order by tweet_count").toPandas()

    panda_df.plot(x="tweet_count", y='users', kind='pie', figsize=(50, 50)).get_figure().savefig(output_image)

    print("done into file: "+output_image)

finally:
    sc.stop()
    shutil.os.remove(data_file)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


