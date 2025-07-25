import pandas as pd
from kafka import KafkaProducer
import json
import time

# Load the creditcard.csv file
df = pd.read_csv("creditcard.csv")

# Drop rows with missing values
df = df.dropna()

# Drop the 'Class' column (target)
if 'Class' in df.columns:
    df = df.drop(columns=['Class'])

# Select a subset — e.g., first 10 rows
subset_df = df.head(10)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Stream the subset
for _, row in subset_df.iterrows():
    features = row.tolist()
    transaction = {"features": features}
    print(f"✅ Sending: {transaction}")
    producer.send("transactions", transaction)
    time.sleep(1)

producer.flush()
print("✅ Finished streaming 100 transactions.")