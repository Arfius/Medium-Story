# consumer.py
# receive and print a message

# import the KafkaConsumer class
from kafka import KafkaConsumer

# instance a KafkaConsumer producer that listen for example_topic messages
consumer = KafkaConsumer('example_topic',
                          bootstrap_servers='localhost:9093',
                          api_version=(0, 10, 1))

# consumer object is a python cursor
# consumer waiting for new messages forever
for m in consumer:
    print(m)
