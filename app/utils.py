import joblib


def load_model():
    """
    Load the trained churn prediction model.
    """
    return joblib.load("model/churn_model.pkl")


def get_risk_label(probability: float) -> str:
    """
    Convert probability into a business-friendly risk label.
    """
    if probability < 0.30:
        return "Low"
    elif probability < 0.70:
        return "Medium"
    else:
        return "High"