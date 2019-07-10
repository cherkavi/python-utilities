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
