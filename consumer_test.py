from kafka import KafkaConsumer
import json

# Connect to Kafka and subscribe to the 'transactions' topic
consumer = KafkaConsumer(
    'predictions',
    bootstrap_servers='localhost:29092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',  # start from the beginning if no offset is stored
    enable_auto_commit=True,
    group_id='test-consumer-group'
)

print("✅ Listening for messages on 'transactions' topic...\n")

# Continuously listen for messages
for message in consumer:
    print(f"📥 Received message: {message.value}")