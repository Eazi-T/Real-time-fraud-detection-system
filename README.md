# 🕵️‍♂️ Real-Time Fraud Detection System
A real-time fraud detection pipeline powered by FastAPI, Kafka, and Machine Learning, containerized with Docker, and monitored using Prometheus and Grafana. This system ingests financial transaction data via Kafka, performs real-time inference using a trained ML model, and outputs predictions to a Kafka topic.

## 📁 Project Structure
```
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── model.py                # Model loading and inference
│   ├── model_service.py        # Prediction logic
│   └── schemas.py              # Pydantic data schemas
├── consumer_test.py            # Kafka consumer test script
├── docker-compose.yml          # Orchestration of services
├── Dockerfile                  # FastAPI app container
├── fraud_detection_model.pkl   # Trained ML model (e.g., XGBoost)
├── kafka_test_consumer         # Utility for consuming Kafka topics
├── kafka_test_producer         # Utility for producing test data
├── prometheus.yml              # Prometheus monitoring config
├── requirements.txt            # Python dependencies
├── send_test_data.py           # Stream test data into Kafka
├── stream_producer             # Custom Kafka producer logic
├── source/                     # Raw or structured data (optional)
└── venv/                       # Virtual environment (not included in Docker build)
```

## ⚙️ Features
- ✅ Real-time streaming using Apache Kafka
- ✅ Fraud prediction using a pre-trained ML model
- ✅ REST API built with FastAPI
- ✅ Containerized using Docker
- ✅ Real-time monitoring with Prometheus and Grafana
- ✅ Modular design for easy extension

## 🚀 Getting Started
1. Clone the Repository
```
git clone https://github.com/your-username/fraud-detection-streaming.git
cd fraud-detection-streaming
```
2. Start Services
Make sure Docker is installed and running:
```
docker-compose up --build
```
This starts:
- Zookeeper
- Kafka broker
- FastAPI app
- Prometheus
- Grafana (available on localhost:3000)

## 🧠 How It Works
- Transaction data is sent to the transactions Kafka topic.
- FastAPI consumes the data, performs fraud prediction using the ML model (fraud_detection_model.pkl).
- Results are published to a predictions Kafka topic.
- Monitoring is handled via Prometheus metrics endpoint and visualized in Grafana.

## 🧪 Testing the Pipeline
- Send Test Transactions
```
python send_test_data.py
```
- Kafka Consumer (for Output)
```
python kafka_test_consumer
```

## 📊 Monitoring
- Prometheus config: prometheus.yml
- Metrics endpoint: http://localhost:8000/metrics
- Grafana Dashboard: Visit http://localhost:3000
- (Default user: admin / admin)

## 📦 Dependencies
Listed in requirements.txt. Includes:
- fastapi
- uvicorn
- kafka-python
- xgboost (or appropriate ML lib)
- prometheus_client
- pydantic
- scikit-learn
Install manually (if running outside Docker):

```
pip install -r requirements.txt
```

## 📌 Notes
Be sure to configure the correct Kafka topic names in both producer and consumer.
For large test datasets, you can batch-send via send_test_data.py.

## 🧠 Model Info
The model was trained on the Kaggle Credit Card Fraud Dataset using a binary classification algorithm [Dataset](). Only anonymized PCA components and transaction amount/time were used.

## 📄 License
This project is open-source and available under the MIT License.
