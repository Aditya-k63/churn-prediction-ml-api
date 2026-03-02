from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import os
app= FastAPI()

## load model artifact
BASE_DIR= os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "churn_model.pkl")
with open(MODEL_PATH,"rb") as f:
    artifact = pickle.load(f)

model=artifact["model"]
THRESHOLD=artifact["threshold"]


class Customer(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

@app.post("/predict")
def predict_churn(customer: Customer):
    data = pd.DataFrame([customer.dict()])
    prob = model.predict_proba(data)[0][1]

    prediction = "Churn" if prob >= THRESHOLD else "Stay"

    return {
        "churn_probability": float(prob),
        "threshold": THRESHOLD,
        "prediction": prediction
    }