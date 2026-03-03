# Customer Churn Prediction System

An end-to-end machine learning system that predicts customer churn using a Logistic Regression model, deployed via FastAPI and integrated with a Streamlit frontend.

---

## Project Overview

This project builds a complete ML pipeline for customer churn prediction:

- Data preprocessing using scikit-learn Pipeline
- Feature encoding and scaling
- Model training and evaluation
- ROC-AUC analysis and threshold optimization
- FastAPI deployment
- Streamlit frontend integration

The system allows users to input customer details and receive churn probability and classification in real-time.

---

## Model Performance

- Model: Logistic Regression
- ROC-AUC: ~0.83
- Threshold optimized using F1-score
- Handles class imbalance via threshold tuning

---

## Architecture

Streamlit Frontend  
↓  
FastAPI Backend  
↓  
Scikit-learn Pipeline (Preprocessing + Model)  
↓  
Churn Prediction  

---

## Project Structure
churn-prediction-ml-api/
│
├── app/
│ └── main.py # FastAPI backend
│
├── model/
│ └── churn_model.pkl # Trained model artifact
│
├── Frontend/
│ └── streamlit_app.py # Streamlit UI
│
├── requirements.txt
└── README.md


---

## Running the Project Locally

### 1. Clone the Repository


git clone <your-repo-url>
cd churn-prediction-ml-api


### 2. Install Dependencies


pip install -r requirements.txt


### 3. Start FastAPI Backend


uvicorn app.main:app --reload


API documentation:

http://127.0.0.1:8000/docs


Health check:

http://127.0.0.1:8000/health


### 4. Start Streamlit Frontend

In a new terminal:


streamlit run Frontend/streamlit_app.py


---

## API Endpoint

### POST /predict

Accepts customer information and returns:


{
"churn_probability": float,
"threshold": float,
"prediction": "Churn" | "Stay"
}


---

## Key Learnings

- Importance of consistent scikit-learn versioning in model deployment
- Threshold tuning vs default 0.5 classification
- Proper schema validation with Pydantic
- Model sanity checking via controlled feature perturbation
- Building full-stack ML systems beyond notebooks

---

## Future Improvements

- Docker containerization
- Cloud deployment
- Model explainability (SHAP integration)
- CI/CD pipeline

---

## Author

Aditya Kumar
