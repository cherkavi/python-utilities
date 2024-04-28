#############################################
# Kafka producer
#############################################
# This script sends a message to a Kafka topic

# Usage:
# export KAFKA_BROKER=localhost:9092
# export KAFKA_TOPIC=stream-processor-input


# python3
from kafka import KafkaProducer
import os
import sys

if len(sys.argv)>1:
    message = sys.argv[1]
else:
    message = '{"test1":"value1", "test2":"value2"}'

producer = KafkaProducer(bootstrap_servers=[os.environ["KAFKA_BROKER"]])
producer.send(os.environ["KAFKA_TOPIC"], value=message.encode("utf-8"))
producer.flush()
