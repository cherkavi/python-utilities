# mapr-stream

## kafka consumer

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/mapr-stream/kafka-consumer.py) -->
<!-- The below code snippet is automatically added from ../../python/mapr-stream/kafka-consumer.py -->
```py
from confluent_kafka import Consumer, KafkaError

c = Consumer({'group.id': 'mygroup', 'default.topic.config': {'auto.offset.reset': 'earliest'}})
c.subscribe(['/mapr/dp.prod.zur/vantage/streams/extraction-test:extraction-start'])
while True:
    msg = c.poll(timeout=1.0)
    if msg is None: continue
    if not msg.error():
        print('Received message: %s' % msg.value().decode('utf-8'))
        continue
    else:
        print ("error happend during the reading")
        if msg.error().code() != KafkaError._PARTITION_EOF:
            print(msg.error())
            break
c.close()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## kafka producer

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/mapr-stream/kafka-producer.py) -->
<!-- The below code snippet is automatically added from ../../python/mapr-stream/kafka-producer.py -->
```py
from confluent_kafka import Producer

p = Producer({'streams.producer.default.stream': '/mapr/dp.prod.zur/vantage/streams/extraction-test'})
print("Kafka producer connected ")
p.produce('scenarioextraction-start', data.encode('utf-8'))
p.flush
```
<!-- MARKDOWN-AUTO-DOCS:END -->


