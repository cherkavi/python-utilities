from pyspark import SparkContext
import re

sc:SparkContext = SparkContext("local","simple example")
sc.getConf().set("spark.hadoop.validateOutputSpecs", "false")

words = sc.textFile("words.txt").flatMap(lambda line: re.split(" |\n", line))

wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)

wordCounts.saveAsTextFile("output")