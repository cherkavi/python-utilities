#############################################
# Kafka Consumer
#############################################
# This script is a Kafka consumer that reads messages from a Kafka topic.
# The consumer reads messages from the beginning of the topic.
#############################################
# application parameters
# export KAFKA_BROKER=localhost:9092
# export KAFKA_TOPIC=stream-processor-output

import os
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from kafka.structs import TopicPartition

# Create a KafkaConsumer instance
consumer = KafkaConsumer(
    bootstrap_servers=[os.environ["KAFKA_BROKER"]], 
    auto_offset_reset='earliest', 
    # group_id=group,
    enable_auto_commit=False
)

# Subscribe to a specific topic
consumer.subscribe(topics=[os.environ["KAFKA_TOPIC"]])

# Poll for new messages
while True:
    msg = consumer.poll(timeout_ms=1000)
    if msg:
        for topic, message in msg.items():            
          # TopicPartition
            value: ConsumerRecord = message[0]
            print(f"Topic: {topic.topic} | Value: {value.value.decode('utf-8')}")
    else:
        pass
