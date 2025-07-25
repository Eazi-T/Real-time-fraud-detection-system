# model_service.py
from kafka import KafkaConsumer, KafkaProducer
import json
from model import predict_fraud  # <-- import your function

# Create Kafka consumer to read from 'transactions' topic
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='model-group'
)

# Create Kafka producer to send to 'predictions' topic
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("🤖 ML Service running... Waiting for transactions.\n")

for msg in consumer:
    transaction = msg.value
    features = transaction['features']

    result = predict_fraud(features)  # Use your imported function
    print(f"✅ Prediction: {result}")

    producer.send("predictions", result)
    producer.flush()