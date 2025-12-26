# app.py
import streamlit as st
import requests
import os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Health Insurance Premium Predictor",
    page_icon="🩺",
    layout="centered"
)

# --------------------------------------------------
# ENV CONFIG (AZURE SAFE)
# --------------------------------------------------
API_URL = os.getenv("MODEL_API_URL")

if not API_URL:
    st.error("❌ MODEL_API_URL environment variable not set.")
    st.stop()

API_URL = API_URL.rstrip("/") + "/predict"

# --------------------------------------------------
# STYLES
# --------------------------------------------------
st.markdown("""
<style>
.main { background-color: #0e1117; }
h1, h2, h3 { color: #ffffff; }
label { color: #c9d1d9 !important; }

.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3.2em;
    font-size: 18px;
    background: linear-gradient(90deg, #238636, #2ea043);
    color: white;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #2ea043, #238636);
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🩺 Health Insurance Premium Predictor")
st.caption("AI-powered premium estimation • Secure • Cloud Deployed")

st.divider()

# --------------------------------------------------
# INPUTS
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("🎂 Age", 18, 100, 30)
    dependants = st.number_input("👨‍👩‍👧 Dependants", 0, 10, 0)
    income = st.number_input("💰 Annual Income (Lakhs)", 0, 200, 10)
    genetical_risk = st.number_input("🧬 Genetic Risk Index", 0, 5, 1)

with col2:
    gender = st.selectbox("⚧ Gender", ["Male", "Female"])
    marital_status = st.selectbox("💍 Marital Status", ["Married", "Unmarried"])
    employment_status = st.selectbox("🏢 Employment", ["Salaried", "Self-Employed"])
    bmi = st.selectbox("⚖️ BMI Category", ["Normal", "Overweight", "Obesity", "Underweight"])

st.subheader("🩺 Health & Policy Details")

col3, col4 = st.columns(2)

with col3:
    smoking = st.selectbox("🚬 Smoking Status", ["No", "Occasional", "Regular"])
    medical_history = st.selectbox(
        "📋 Pre-Existing Conditions",
        [
            "None",
            "Diabetes",
            "High blood pressure",
            "Heart disease",
            "Diabetes & High blood pressure",
            "Diabetes & Heart disease",
            "Thyroid",
        ],
    )

with col4:
    insurance_plan = st.selectbox("📄 Insurance Plan", ["Bronze", "Silver", "Gold"])
    region = st.selectbox("🌍 Region", ["Northwest", "Southeast", "Southwest"])

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
st.divider()

if st.button("🔮 Predict Premium"):
    payload = {
        "age": age,
        "dependants": dependants,
        "income": income,
        "genetical_risk": genetical_risk,
        "insurance_plan": insurance_plan,
        "gender": gender,
        "marital_status": marital_status,
        "employment_status": employment_status,
        "bmi": bmi,
        "smoking": smoking,
        "region": region,
        "medical_history": medical_history,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=15)

        if response.status_code == 200:
            result = response.json()
            premium = result["predicted_premium"]
            st.success(f"💸 **Predicted Premium: ₹ {premium:,}**")
        else:
            st.error(f"❌ API Error ({response.status_code})")

    except requests.exceptions.RequestException as e:
        st.error("❌ Unable to connect to Model API")
        st.code(str(e))

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.caption(
    "Built with ❤️ using Streamlit • Model served via Azure App Service (FastAPI)"
)
