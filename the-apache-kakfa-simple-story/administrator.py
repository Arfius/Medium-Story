# administrator.py
# create new topic if it not exists

# import the KafkaAdminClient and NewTopic classes
from kafka.admin import KafkaAdminClient, NewTopic

# instance a KafkaAdminClient 
administrator = KafkaAdminClient(
        bootstrap_servers='localhost:9093',
        api_version=(0, 10, 1))

# get topics from kafka ecosystem
existing_topics = administrator.list_topics()

# create the new topic if it is not already created
if 'example_topic' not in existing_topics:
    topic = NewTopic(name='example_topic',
                     num_partitions=1,
                     replication_factor=1)

    administrator.create_topics(new_topics=[topic])
