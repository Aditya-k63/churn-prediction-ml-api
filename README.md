I built this project to go beyond just training a model in a notebook. The goal was to take a real business problem — predicting which customers are about to leave — and build an actual system around it. That means a proper API, a frontend someone can use, authentication, and containerisation so it runs anywhere.
The model is Logistic Regression but the interesting part isn't the algorithm — it's the threshold tuning, the sklearn Pipeline setup, and the fact that it's deployed and usable, not just a .ipynb file sitting on my machine.


What it does
You enter a customer's details — tenure, monthly charges, contract type, etc. — and the system tells you the probability they'll churn, along with a classification (Churn / Stay). The threshold for that classification isn't the default 0.5 — I tuned it using F1-score to ~0.42, which makes more sense for a retention use case where missing a churner is more costly than a false alarm.



Model performance
MetricValueAlgorithmLogistic RegressionDatasetIBM Telco Customer Churn (7,043 rows)ROC-AUC~0.83Decision threshold~0.42 (F1-optimised)
I also verified the model makes sense — increasing tenure lowers churn probability, increasing monthly charges raises it. Basic sanity check but important before trusting any predictions.

Architecture
Streamlit Frontend      (port 8501)
        │
        ▼
FastAPI Backend         (port 8000)
  ├── JWT Authentication
  └── POST /predict
        │
        ▼
scikit-learn Pipeline
  ├── Encoding + StandardScaler
  └── Logistic Regression
        │
        ▼
  Churn probability + label

Project structure
churn-prediction-ml-api/
├── app/
│   ├── main.py              # FastAPI routes and prediction logic
│   └── auth.py              # JWT auth — admin-protected endpoints
├── Frontend/
│   └── streamlit_app.py     # Streamlit UI
├── model/
│   └── churn_model.pkl      # Trained pipeline artifact
├── training/                # Training scripts
├── docker-compose.yml
├── Dockerfile
├── start.sh
├── requirements.txt
└── README.md

Running it locally
bash# Clone the repo
git clone https://github.com/adsharma14/churn-prediction-ml-api
cd churn-prediction-ml-api

# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload

# In a new terminal — start the frontend
streamlit run Frontend/streamlit_app.py
ServiceURLStreamlit UIhttp://localhost:8501Swagger docshttp://localhost:8000/docsHealth checkhttp://localhost:8000/health

Or with Docker
bashdocker-compose up --build
Same result, no manual setup needed.

API
POST /predict
json{
  "tenure": 12,
  "MonthlyCharges": 65.5,
  "TotalCharges": 786.0,
  "Contract": "Month-to-month",
  "PaymentMethod": "Electronic check",
  "InternetService": "Fiber optic"
}
Response:
json{
  "churn_probability": 0.74,
  "threshold": 0.42,
  "prediction": "Churn"
}
GET /health
json{ "status": "ok" }
Full interactive docs available at /docs once the app is running.

A few things I learned building this
The versioning issue caught me off guard — the sklearn version used to train the model has to match the one running the API, otherwise the .pkl won't load. Obvious in hindsight but took me a while to debug.
Bundling preprocessing inside the Pipeline was the right call. I tried it the other way first (separate scaler, loaded separately in the API) and it's a mess to maintain. Having everything in one artifact means training and inference are always consistent.
Threshold tuning mattered more than I expected. The default 0.5 was missing a lot of real churners. Optimising for F1 dropped the threshold to ~0.42 and recall improved significantly without hurting precision too much.

What I want to add next

MySQL logging — store every prediction with input features, probability, and timestamp
MLflow — properly compare Logistic Regression vs Random Forest vs XGBoost instead of just going with LR
SHAP — so predictions come with an explanation, not just a number
GitHub Actions for CI/CD
Deploy it somewhere publicly accessible


Dataset
IBM Telco Customer Churn — available on Kaggle. 7,043 customers, 20 features.

Author
Aditya Kumar
GitHub: @adsharma14
