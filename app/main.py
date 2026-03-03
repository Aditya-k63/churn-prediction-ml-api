from fastapi import FastAPI,Path, Query,HTTPException
from pydantic import BaseModel,Field, computed_field
from typing import Annotated, Literal, Optional
import pandas as pd
import pickle
import os
app= FastAPI(
    title="Customer Churn Prediction API",
    description="An API to predict customer churn based on various features using a pre-trained machine learning model."
)

## load model artifact
BASE_DIR= os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "churn_model.pkl")

try:
    with open(MODEL_PATH,"rb") as f:
        artifact = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load model artifact: {e}")

model=artifact["model"]
THRESHOLD=artifact["threshold"]


class Customer(BaseModel):

    gender:Annotated[Literal['Male', 'Female','Other'], Field(..., description='Gender of the customer')]
    SeniorCitizen:Annotated[Literal["Yes", "No"], Field(..., description='Whether the customer is a senior citizen')]
    Partner: Annotated[Literal["Yes", "No"], Field(..., description='Whether the customer has a partner')]
    Dependents: Annotated[Literal["Yes", "No"], Field(..., description='Whether the customer has dependents')]
    tenure:Annotated[int, Field(..., ge=0, description='Number of months the customer has stayed with the company')]
    PhoneService: Annotated[Literal["Yes", "No"], Field(..., description='Whether the customer has phone service')]
    MultipleLines: Annotated[Literal["Yes", "No",'No phone service'], Field(..., description='Whether the customer has multiple lines')]
    InternetService: Annotated[Literal["DSL", "Fiber optic", "No"], Field(..., description='Internet service type')]
    OnlineSecurity: Annotated[Literal["Yes", "No",'No internet service'], Field(..., description='Whether the customer has online security')]
    OnlineBackup: Annotated[Literal["Yes", "No",'No internet service'], Field(..., description='Whether the customer has online backup')]
    DeviceProtection: Annotated[Literal["Yes", "No",'No internet service'], Field(..., description='Whether the customer has device protection')]
    TechSupport: Annotated[Literal["Yes", "No",'No internet service'], Field(..., description='Whether the customer has tech support')]
    StreamingTV: Annotated[Literal["Yes", "No",'No internet service'], Field(..., description='Whether the customer has streaming TV')]
    StreamingMovies: Annotated[Literal["Yes", "No",'No internet service'], Field(..., description='Whether the customer has streaming movies')]
    Contract: Annotated[Literal["Month-to-month", "One year", "Two year"], Field(..., description='Contract type')]
    PaperlessBilling: Annotated[Literal["Yes", "No"], Field(..., description='Whether the customer has paperless billing')]
    PaymentMethod: Annotated[Literal["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], Field(..., description='Payment method')]
    MonthlyCharges: Annotated[float, Field(..., gt=0, description='Monthly charges for the customer')]
    TotalCharges: Annotated[float, Field(..., gt=0, description='Total charges for the customer')]


### response schema 

class PredictionResponse(BaseModel):
    churn_probability: float
    threshold: float
    prediction: str

##  Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

#prediction endpoint 

@app.post("/predict", response_model=PredictionResponse)
def predict_churn(customer: Customer):
    
    try:
        data = pd.DataFrame([customer.dict()])

    ## coverting SenorCitizen, Partner, Dependents, PhoneService, PaperlessBilling to binary
        data["SeniorCitizen"] = data["SeniorCitizen"].map({
        "Yes": 1,
        "No": 0})
   
        prob = model.predict_proba(data)[0][1]

        prediction = "Churn" if prob >= THRESHOLD else "Stay"

        return  PredictionResponse( 
        churn_probability=float(prob),
        threshold=THRESHOLD,
        prediction=prediction
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")