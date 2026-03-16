import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Churn Prediction", layout="wide")

# ── Session state init ────────────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None

# ── Login Page 
def show_login():
    st.title(" Customer Churn Prediction System")
    st.subheader("Please login to continue")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        try:
            response = requests.post(
                f"{API_URL}/login",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                token = response.json()["access_token"]
                st.session_state.token = token
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(" Invalid username or password")
        except Exception as e:
            st.error(f"Connection error: {e}")

# ── Prediction Page ─
def show_prediction():
    st.title("Customer Churn Prediction System")

    # Top right logout
    col1, col2 = st.columns([8, 1])
    with col1:
        st.markdown(f" Logged in as **{st.session_state.username}**")
    with col2:
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.username = None
            st.rerun()

    st.markdown("Fill in customer details to predict churn risk.")
    st.divider()

    # ── Form Inputs ───────────────────────────────────────
    with st.form("churn_form"):

        col1, col2 = st.columns(2)

        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            senior = st.selectbox("Senior Citizen", ["Yes", "No"])
            partner = st.selectbox("Partner", ["Yes", "No"])
            dependents = st.selectbox("Dependents", ["Yes", "No"])
            tenure = st.number_input("Tenure (months)", min_value=0, value=12)
            phone = st.selectbox("Phone Service", ["Yes", "No"])
            multiple = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
            internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
            contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

        with col2:
            security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
            backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
            protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
            tech = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
            tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
            movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
            paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
            payment = st.selectbox("Payment Method", [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ])
            monthly = st.number_input("Monthly Charges", min_value=0.0, value=70.0)
            total = st.number_input("Total Charges", min_value=0.0, value=840.0)

        submitted = st.form_submit_button("🔍 Predict Churn")

    # ── Prediction Call ─
    if submitted:
        payload = {
            "gender": gender,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone,
            "MultipleLines": multiple,
            "InternetService": internet,
            "OnlineSecurity": security,
            "OnlineBackup": backup,
            "DeviceProtection": protection,
            "TechSupport": tech,
            "StreamingTV": tv,
            "StreamingMovies": movies,
            "Contract": contract,
            "PaperlessBilling": paperless,
            "PaymentMethod": payment,
            "MonthlyCharges": monthly,
            "TotalCharges": total
        }

        try:
            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )

            if response.status_code == 200:
                result = response.json()
                prob = result["churn_probability"]
                prediction = result["prediction"]

                st.subheader(" Prediction Result")

                if prediction == "Churn":
                    st.error(f"High Risk of Churn ({prob:.2%})")
                else:
                    st.success(f"Low Risk of Churn ({prob:.2%})")

                st.progress(float(prob))

            elif response.status_code == 401:
                st.error(" Session expired. Please login again.")
                st.session_state.token = None
                st.rerun()
            else:
                st.error(f"API Error: {response.text}")

        except Exception as e:
            st.error(f"Connection error: {e}")


# ── Router 
if st.session_state.token is None:
    show_login()
else:
    show_prediction()