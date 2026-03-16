# Customer Churn Prediction API

An end-to-end machine learning system that predicts customer churn probability using a Logistic Regression model — deployed via **FastAPI**, with an interactive **Streamlit** frontend for real-time predictions.

> **Docker Hub:** `docker pull adsharma14/churn-prediction-api`

## Model Performance

| Metric    | Value  |
|-----------|--------|
| Model     | Logistic Regression |
| ROC-AUC   | ~0.83  |
| Threshold | Optimised via F1-score (not default 0.5) |
| Imbalance | Handled via threshold tuning |

---

## Architecture

```
Streamlit Frontend  (port 8501)
        ↓
FastAPI Backend     (port 8000)
        ↓
scikit-learn Pipeline
  └── Preprocessing (encoding + scaling)
  └── Logistic Regression model
        ↓
Churn Probability + Label
```

---

## Project Structure

```
churn-prediction-ml-api/
├── app/
│   └── main.py              # FastAPI backend
├── model/
│   └── churn_model.pkl      # Trained model artifact
├── Frontend/
│   └── streamlit_app.py     # Streamlit UI
├── requirements.txt
└── README.md
```

---

## Quick Start

### Option 1 — Docker (recommended)

```bash
# Pull and run the API
docker pull adsharma14/churn-prediction-api
docker run -p 8000:8000 adsharma14/churn-prediction-api
```

API docs live at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Option 2 — Run locally

**1. Clone the repo**
```bash
git clone https://github.com/adsharma14/churn-prediction-ml-api
cd churn-prediction-ml-api
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Start the FastAPI backend**
```bash
uvicorn app.main:app --reload
```

**4. Start the Streamlit frontend** _(new terminal)_
```bash
streamlit run Frontend/streamlit_app.py
```

| Service       | URL                                      |
|---------------|------------------------------------------|
| Streamlit UI  | http://localhost:8501                    |
| API docs      | http://localhost:8000/docs               |
| Health check  | http://localhost:8000/health             |

---

## API Reference

### `POST /predict`

Accepts customer information and returns churn probability and classification.

**Request body:**
```json
{
  "tenure": 12,
  "MonthlyCharges": 65.5,
  "TotalCharges": 786.0,
  "Contract": "Month-to-month",
  "PaymentMethod": "Electronic check",
  "InternetService": "Fiber optic"
}
```

**Response:**
```json
{
  "churn_probability": 0.74,
  "threshold": 0.42,
  "prediction": "Churn"
}
```

### `GET /health`
Returns API status.

```json
{ "status": "ok" }
```

---

## Key Technical Decisions

- **Threshold tuning** — Default 0.5 threshold replaced with F1-optimised threshold (~0.42) to better handle class imbalance. This catches more true churners at the cost of slightly more false positives — the right tradeoff for retention use cases.
- **sklearn Pipeline** — Preprocessing (encoding + scaling) bundled inside the same `.pkl` as the model. Ensures identical transformations at training and inference time. Eliminates the most common deployment bug.
- **Pydantic validation** — All inputs validated before reaching the model. Returns clear 422 errors on bad input rather than silent failures.
- **Model sanity checking** — Verified model direction by perturbing key features (e.g. increasing tenure should decrease churn probability).

---

## Future Improvements

- [ ] Docker Compose with MySQL prediction logging
- [ ] MLflow experiment tracking (LR vs RF vs XGBoost comparison)
- [ ] SHAP explainability — feature contribution per prediction
- [ ] CI/CD with GitHub Actions
- [ ] Cloud deployment (Railway / Render / AWS EC2)

---

## Dataset

**IBM Telco Customer Churn Dataset** — 7,043 customers, 20 features including contract type, tenure, monthly charges, internet service type, and payment method.

Source: [Kaggle — Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## Author

**Aditya Kumar**
- GitHub: [@adsharma14](https://github.com/adsharma14)
- Docker Hub: [adsharma14](https://hub.docker.com/u/adsharma14)

---

## License

MIT License — free to use and modify.
