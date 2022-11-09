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

