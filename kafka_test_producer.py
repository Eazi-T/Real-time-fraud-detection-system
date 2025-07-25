from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

sample_data = {"message": "Kafka is working!"}
producer.send('test-topic', sample_data)
producer.flush()
print("✅ Message sent to 'test-topic'")