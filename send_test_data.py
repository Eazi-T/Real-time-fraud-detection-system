from kafka import KafkaProducer
import json

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define sample transaction
sample_transaction = {
    "features": [
        0.0,
        -1.3598071336738,
        -0.0727811733098497,
        2.53634673796914,
        1.37815522427443,
        -0.338320769942518,
        0.462387777762292,
        0.239598554061257,
        0.0986979012610507,
        0.363786969611213,
        0.0907941719789316,
        -0.551599533260813,
        -0.617800855762348,
        -0.991389847235408,
        -0.311169353699879,
        1.46817697209427,
        -0.470400525259478,
        0.207971241929242,
        0.0257905801985591,
        0.403992960255733,
        0.251412098239705,
        -0.018306777944153,
        0.277837575558899,
        -0.110473910188767,
        0.0669280749146731,
        0.128539358273528,
        -0.189114843888824,
        0.133558376740387,
        -0.0210530534538215,
        149.62
    ]
}

# Send transaction to Kafka topic
producer.send("transactions", sample_transaction)
producer.flush()
print("✅ Sent sample transaction to 'transactions' topic")