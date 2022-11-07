from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import DataFrameReader
from kafka import KafkaConsumer, KafkaProducer
import json
import requests, shutil


def download_file(url, local_path):
    ''' download file from remote url and save it to path '''
    response = requests.get(url, stream=True)
    with open(local_path, "wb") as output_file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, output_file)


def as_json(row):
    ''' convert row from python object to JSON representation: https://openflights.org/data.html '''
    try:
        return json.dumps(
            {"Airport ID" : row._c0, "Name":row._c1,"City":row._c2,
            "Country":row._c3,"IATA":row._c4,"ICAO":row._c5,"Latitude":row._c6,
            "Longitude":row._c7,"Altitude":row._c8,"Timezone":row._c9,"DST":row._c10,
            "TimeZone":row._c11,"Type":row._c12,"Source":row._c13}, 
            sort_keys=False)
    except BaseException as e:
        return None


try:
    data_file = "airports.dat"
    data_file_url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
    download_file(data_file_url, data_file)
    kafka_url = "172.18.0.100:9092"
    kafka_topic = "airports"

    sc = SparkContext("local", "example-of-processing-data")
    sc.setLogLevel("ERROR")
    sqlContext = SQLContext(sc)

    airports = DataFrameReader(sqlContext).csv(data_file)

    producer = KafkaProducer(bootstrap_servers=kafka_url)    
    #for index in range(1, airports.count()):
    #    print(to_json(airports.take(index)[0]))
    for each in airports.collect():
        # logging.debug(as_json(each))
        producer.send(kafka_topic, as_json(each))


finally:
    producer.close()
    sc.stop()
    shutil.os.remove(data_file)
