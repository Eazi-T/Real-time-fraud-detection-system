import joblib
import numpy as np
from pathlib import Path

# Load the trained model on startup
MODEL_PATH = Path(__file__).parent.parent / "fraud_detection_model.pkl"
model = joblib.load(MODEL_PATH)

def predict_fraud(features: list):
    data = np.array(features).reshape(1, -1)
    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]
    return {
        "prediction": int(prediction),
        "fraud_probability": round(probability, 4)
    }