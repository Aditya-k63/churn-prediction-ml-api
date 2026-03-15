from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Annotated, Literal
import pandas as pd
import pickle
import os

from app.auth import (
    USERS_DB,
    verify_password,
    create_token,
    get_current_user,
    require_admin
)

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict customer churn. Protected with JWT Authentication.",
)

# ── Load model artifact ───────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "churn_model.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        artifact = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load model artifact: {e}")

model = artifact["model"]
THRESHOLD = artifact["threshold"]


# ── Schemas ───────────────────────────────────────────────

class Customer(BaseModel):
    gender: Annotated[Literal['Male', 'Female', 'Other'], Field(..., description='Gender of the customer')]
    SeniorCitizen: Annotated[Literal["Yes", "No"], Field(..., description='Whether the customer is a senior citizen')]
    Partner: Annotated[Literal["Yes", "No"], Field(..., description='Whether the customer has a partner')]
    Dependents: Annotated[Literal["Yes", "No"], Field(..., description='Whether the customer has dependents')]
    tenure: Annotated[int, Field(..., ge=0, description='Number of months the customer has stayed')]
    PhoneService: Annotated[Literal["Yes", "No"], Field(..., description='Whether the customer has phone service')]
    MultipleLines: Annotated[Literal["Yes", "No", "No phone service"], Field(..., description='Whether the customer has multiple lines')]
    InternetService: Annotated[Literal["DSL", "Fiber optic", "No"], Field(..., description='Internet service type')]
    OnlineSecurity: Annotated[Literal["Yes", "No", "No internet service"], Field(..., description='Whether the customer has online security')]
    OnlineBackup: Annotated[Literal["Yes", "No", "No internet service"], Field(..., description='Whether the customer has online backup')]
    DeviceProtection: Annotated[Literal["Yes", "No", "No internet service"], Field(..., description='Whether the customer has device protection')]
    TechSupport: Annotated[Literal["Yes", "No", "No internet service"], Field(..., description='Whether the customer has tech support')]
    StreamingTV: Annotated[Literal["Yes", "No", "No internet service"], Field(..., description='Whether the customer has streaming TV')]
    StreamingMovies: Annotated[Literal["Yes", "No", "No internet service"], Field(..., description='Whether the customer has streaming movies')]
    Contract: Annotated[Literal["Month-to-month", "One year", "Two year"], Field(..., description='Contract type')]
    PaperlessBilling: Annotated[Literal["Yes", "No"], Field(..., description='Whether the customer has paperless billing')]
    PaymentMethod: Annotated[Literal["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], Field(..., description='Payment method')]
    MonthlyCharges: Annotated[float, Field(..., gt=0, description='Monthly charges')]
    TotalCharges: Annotated[float, Field(..., gt=0, description='Total charges')]


class PredictionResponse(BaseModel):
    churn_probability: float
    threshold: float
    prediction: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# ── Public routes ─────────────────────────────────────────

@app.get("/health")
def health_check():
    """Public - no auth needed."""
    return {"status": "ok"}


@app.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends()):
    """
    Login with username + password.
    Returns a JWT token to use in protected routes.
    
    Test credentials:
    - username: aditya | password: password123 (admin)
    - username: viewer | password: viewer123   (viewer)
    """
    user = USERS_DB.get(form.username)
    if not user or not verify_password(form.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}


# ── Protected routes ──────────────────────────────────────

@app.post("/predict", response_model=PredictionResponse)
def predict_churn(
    customer: Customer,
    current_user: dict = Depends(get_current_user)   # ← requires login
):
    """
    Protected - requires JWT token.
    Both admin and viewer can access this.
    """
    try:
        data = pd.DataFrame([customer.dict()])
        data["SeniorCitizen"] = data["SeniorCitizen"].map({"Yes": 1, "No": 0})

        prob = model.predict_proba(data)[0][1]
        prediction = "Churn" if prob >= THRESHOLD else "Stay"

        return PredictionResponse(
            churn_probability=float(prob),
            threshold=THRESHOLD,
            prediction=prediction
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/admin/info")
def admin_info(current_user: dict = Depends(require_admin)):  # ← requires admin role
    """
    Admin only route - viewer role will get 403 Forbidden.
    """
    return {
        "message": f"Welcome Admin {current_user['username']}!",
        "model_threshold": THRESHOLD,
        "total_users": len(USERS_DB)
    }