from confluent_kafka import Producer

p = Producer({'streams.producer.default.stream': '/mapr/dp.prod.zur/vantage/streams/extraction-test'})
print("Kafka producer connected ")
p.produce('scenarioextraction-start', data.encode('utf-8'))
p.flush
