# producer.py
# send a message

# import the KafkaProducer class
from kafka import KafkaProducer

# instance a KafkaProducer object
producer = KafkaProducer(bootstrap_servers='localhost:9093', 
                         api_version=(0, 10, 1))

# send the message to 'Hello, World!' using the topic 'example_topic'
producer.send('example_topic', b'Hello, World!')
producer.flush()
print('message sent')
