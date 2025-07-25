import json
import threading
import os
import logging
import time
import numpy as np
import joblib
from fastapi import FastAPI, Request
from prometheus_client import start_http_server
from pydantic import BaseModel
from starlette.responses import PlainTextResponse
from confluent_kafka import Consumer, Producer
from prometheus_client import Counter, Histogram, generate_latest

# ---------- Logging Setup ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ---------- FastAPI App ----------
app = FastAPI()
model = joblib.load("fraud_detection_model.pkl")

# ---------- Environment Variables ----------
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TRANSACTIONS_TOPIC = os.getenv("TRANSACTIONS_TOPIC", "transactions")
PREDICTIONS_TOPIC = os.getenv("PREDICTIONS_TOPIC", "predictions")

producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

# ---------- Prometheus Metrics ----------
REQUEST_COUNT = Counter(
    "app_requests_total", "Total HTTP requests", ["method", "endpoint"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Request latency", ["endpoint"]
)
KAFKA_PREDICTIONS_TOTAL = Counter(
    "kafka_predictions_total", "Total predictions made from Kafka stream"
)
KAFKA_PREDICTIONS_BY_CLASS = Counter(
    "kafka_predictions_by_class", "Number of Kafka predictions by fraud class", ["class"]
)
KAFKA_FRAUD_PROBA_HIST = Histogram(
    "kafka_fraud_probability", "Histogram of fraud probability scores from Kafka predictions"
)

# ---------- Middleware ----------
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(process_time)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    return response

# ---------- Prometheus Metrics Endpoint ----------
@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type="text/plain")

# ---------- Pydantic Schema ----------
class TransactionFeatures(BaseModel):
    features: list[float]

# ---------- API Endpoints ----------
@app.get("/")
def root():
    logger.info("📥 Root endpoint hit")
    return {"message": "🚀 Fraud Detection API is running with Kafka!"}

@app.post("/predict")
def predict(data: TransactionFeatures):
    logger.info(f"📥 Received prediction request: {data.features}")
    features = np.array(data.features).reshape(1, -1)
    pred = model.predict(features)[0]
    proba = model.predict_proba(features)[0][1]
    logger.info(f"📤 Prediction: {pred}, Probability: {proba}")
    return {"prediction": int(pred), "fraud_probability": float(proba)}

# ---------- Kafka Consumer Thread ----------
def consume_and_predict():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'fraud-detector',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([TRANSACTIONS_TOPIC])

    while True:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        try:
            record = json.loads(msg.value().decode('utf-8'))
            features = np.array(record['features']).reshape(1, -1)
            prediction = int(model.predict(features)[0])
            probability = float(model.predict_proba(features)[0][1])

            # ---------- Prometheus Metrics ----------
            KAFKA_PREDICTIONS_TOTAL.inc()
            KAFKA_PREDICTIONS_BY_CLASS.labels(class=str(prediction)).inc()
            KAFKA_FRAUD_PROBA_HIST.observe(probability)

            result = {
                "prediction": prediction,
                "fraud_probability": probability
            }

            producer.produce(PREDICTIONS_TOPIC, json.dumps(result).encode('utf-8'))
            producer.flush()
            logger.info(f"🔁 Kafka message processed: {result}")
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")

# ---------- Start Kafka Consumer on App Startup ----------
@app.on_event("startup")
def start_kafka_consumer():
    start_http_server(8001)
    thread = threading.Thread(target=consume_and_predict, daemon=True)
    thread.start()
