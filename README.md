# Customer Churn Prediction API

A production-ready machine learning application that predicts customer churn using the IBM Telco Customer Churn dataset.

The project includes:

* Scikit-learn training pipeline
* FastAPI REST API
* JWT authentication and role-based access
* Streamlit frontend
* Automated testing with Pytest
* Docker and Docker Compose
* GitHub Actions CI/CD
* Automatic Docker Hub image publishing
* Cloud deployment on Render

---

## Live Demo

* **API Health Check:** https://churn-prediction-api-2ftp.onrender.com/health
* **Swagger API Docs:** https://churn-prediction-api-2ftp.onrender.com/docs
* **Docker Hub:** https://hub.docker.com/r/adsharma14/churn-prediction-api
* **GitHub Repository:** https://github.com/Aditya-k63/churn-prediction-ml-api

---

## What It Does

Given a customer's account information (tenure, charges, contract type, internet service, payment method, and more), the model predicts:

* Probability of churn
* Tuned decision threshold
* Final classification (`Churn` or `Stay`)

Instead of using the default threshold of `0.50`, the model uses an F1-optimized threshold of approximately `0.42`, which improves recall for customers likely to churn.

---

## Model Performance

| Metric             | Value                    |
| ------------------ | ------------------------ |
| Algorithm          | Logistic Regression      |
| Dataset            | IBM Telco Customer Churn |
| Rows               | 7,043                    |
| Features           | 20                       |
| ROC-AUC            | ~0.83                    |
| Decision Threshold | ~0.42 (F1 Optimized)     |

---

## System Architecture

```text
Streamlit Frontend
        │
        ▼
FastAPI Backend
  ├── JWT Authentication
  ├── Role-Based Access Control
  └── /predict Endpoint
        │
        ▼
Scikit-learn Pipeline
  ├── Missing Value Imputation
  ├── One-Hot Encoding
  ├── StandardScaler
  └── Logistic Regression
        │
        ▼
Churn Probability + Business Classification
```

---

## Project Structure

```text
churn-prediction-ml-api/
├── .github/workflows/ci-cd.yml
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── schemas.py
│   └── utils.py
├── Frontend/
│   └── streamlit_app.py
├── model/
│   └── churn_model.pkl
├── training/
│   └── train.py
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── .env.example
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── start.sh
├── requirements.txt
├── LICENSE
└── README.md
```

---

## API Endpoints

| Method | Endpoint      | Description                       |
| ------ | ------------- | --------------------------------- |
| GET    | `/health`     | Service health check              |
| POST   | `/login`      | Obtain JWT access token           |
| POST   | `/predict`    | Predict churn probability         |
| GET    | `/admin/info` | Admin-only endpoint               |
| GET    | `/docs`       | Interactive Swagger documentation |

---

## Example Prediction Response

```json
{
  "churn_probability": 0.74,
  "threshold": 0.42,
  "prediction": "Churn"
}
```

---

## Authentication

### Demo Credentials

**Admin**

* Username: `aditya`
* Password: `password123`

**Viewer**

* Username: `viewer`
* Password: `viewer123`

---

## Run Locally

```bash
git clone https://github.com/Aditya-k63/churn-prediction-ml-api.git
cd churn-prediction-ml-api

python -m venv myenv
myenv\Scripts\activate   # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload
```

In a second terminal:

```bash
streamlit run Frontend/streamlit_app.py
```

---

## Run with Docker

```bash
docker compose up --build
```

---

## CI/CD Pipeline

The GitHub Actions workflow automatically:

1. Installs dependencies
2. Creates a temporary `.env`
3. Runs automated tests
4. Builds the Docker image
5. Pushes the image to Docker Hub

Every push to the `main` branch triggers the pipeline.

---

## Deployment

The application is deployed to Render using the Docker image published to Docker Hub.

---

## Key Engineering Lessons

* Packaging preprocessing inside a single Scikit-learn `Pipeline` ensures consistent training and inference.
* Matching Scikit-learn versions is critical when loading serialized models.
* Threshold tuning significantly improved churn recall compared to the default `0.50`.
* CI/CD automation eliminates manual build and deployment steps.
* Environment variables are essential for secure secret management.

---

## Future Improvements

* MySQL logging for prediction history
* MLflow experiment tracking
* SHAP-based model explanations
* Model monitoring and drift detection
* Multi-model comparison dashboard

---

## Dataset

IBM Telco Customer Churn dataset from Kaggle:
https://www.kaggle.com/datasets/blastchar/telco-customer-churn

---

## Author

**Aditya Kumar**

* GitHub: https://github.com/adsharma14
* LinkedIn: *(https://www.linkedin.com/in/aditya-kumar1407/)*
