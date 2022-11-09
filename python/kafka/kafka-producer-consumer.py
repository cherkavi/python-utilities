#docker image: https://hub.docker.com/r/spotify/kafka/
#docker image run: docker run -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=172.18.0.100 --env ADVERTISED_PORT=9092 --env advertised.host.name=172.18.0.100 --net docker.local.network --ip 172.18.0.100 spotify/kafka
from kafka import KafkaConsumer, KafkaProducer
import logging

kafka_url = "172.18.0.100:9092"
kafka_topic = "my-topic"

logging.basicConfig(level=logging.DEBUG)
try:
    producer = KafkaProducer(bootstrap_servers=kafka_url)
    producer.send(kafka_topic, b"test")
    producer.send(kafka_topic, "test 2")
finally:
    producer.close()


consumer = KafkaConsumer(bootstrap_servers=kafka_url, auto_offset_reset='earliest', consumer_timeout_ms=200)
consumer.subscribe([kafka_topic])
for message in consumer:
	print(message)