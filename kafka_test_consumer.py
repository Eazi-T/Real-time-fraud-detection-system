from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='test-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("🟢 Waiting for messages...")
for message in consumer:
    print("📥 Received:", message.value)
    break