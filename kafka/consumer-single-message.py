#############################################
# Description: Kafka Consumer
#############################################
# consume one message from the topic

#############################################
# application parameters
# export KAFKA_BROKER=localhost:9092
# export KAFKA_TOPIC=stream-processor-output

import os
from kafka import KafkaConsumer

broker = os.environ["KAFKA_BROKER"]
topic: str = os.environ["KAFKA_TOPIC"]
group: str = os.environ["KAFKA_CONSUMER_GROUP"] if os.environ["KAFKA_CONSUMER_GROUP"] else "my_group_id"

consumer = KafkaConsumer(topic,
                         bootstrap_servers=[broker],
                         auto_offset_reset='earliest',
                         enable_auto_commit=False,
                         group_id=group,
                         value_deserializer=lambda x: x.decode('utf-8')
                        )

for message in consumer:
    print(f"Received data: {message}")    
