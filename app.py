import streamlit as st
import requests

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Health Insurance Premium Predictor",
    page_icon="🩺",
    layout="centered"
)

API_URL = "https://health-insurance-premium-model-api-bvgrg3bmcyhbbpb4.centralindia-01.azurewebsites.net/predict"

# ------------------------------------------------------------
# STYLES
# ------------------------------------------------------------
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    h1, h2, h3, h4 { color: #ffffff; }
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
        color: white;
    }
    .result-box {
        background: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
        font-size: 22px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
st.markdown("<h1 style='text-align:center;'>🩺 Health Insurance Premium Predictor</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#8b949e;'>AI-powered premium estimation using live ML model</p>",
    unsafe_allow_html=True
)

st.divider()

# ------------------------------------------------------------
# INPUT FORM
# ------------------------------------------------------------
with st.form("prediction_form"):
    st.subheader("👤 Personal Details")

    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("🎂 Age", 18, 65, 30)
        gender = st.selectbox("🚻 Gender", ["Male", "Female"])
        marital_status = st.selectbox("💍 Marital Status", ["Married", "Unmarried"])

    with col2:
        dependants = st.slider("👨‍👩‍👧 Dependants", 0, 5, 0)
        employment_status = st.selectbox("💼 Employment Status", ["Salaried", "Self-Employed", "Unemployed"])
        income = st.slider("💰 Annual Income (Lakhs)", 1, 50, 10)

    st.subheader("🩻 Health & Lifestyle")

    col3, col4 = st.columns(2)
    with col3:
        bmi_category = st.selectbox("⚖️ BMI Category", ["Underweight", "Normal", "Overweight", "Obese"])
        smoking = st.selectbox("🚬 Smoking Status", ["No", "Occasional", "Yes"])

    with col4:
        genetical_risk = st.selectbox("🧬 Genetic Risk", [0, 1])
        medical_history = st.selectbox(
            "🏥 Pre-Existing Condition",
            ["None", "Diabetes", "Heart Disease", "Thyroid", "Hypertension"]
        )

    st.subheader("📍 Policy Details")

    col5, col6 = st.columns(2)
    with col5:
        insurance_plan = st.selectbox("📄 Insurance Plan", ["Silver", "Gold", "Platinum"])
    with col6:
        region = st.selectbox("🌍 Region", ["Northwest", "Southeast", "Southwest", "Northeast"])

    submit = st.form_submit_button("🔮 Predict Premium")

# ------------------------------------------------------------
# API CALL
# ------------------------------------------------------------
if submit:
    payload = {
    "age": age,
    "dependants": dependants,
    "income": income,
    "genetical_risk": genetical_risk,
    "insurance_plan": insurance_plan,
    "gender": gender,
    "marital_status": marital_status,
    "employment_status": employment_status,
    "bmi": bmi_category,   # ✅ FIX HERE
    "smoking": smoking,
    "region": region,
    "medical_history": medical_history
}


    with st.spinner("⏳ Calculating premium..."):
        try:
            response = requests.post(
                API_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )

            if response.status_code == 200:
                premium = response.json()["predicted_premium"]
                st.markdown(
                    f"""
                    <div class="result-box">
                        💸 <b>Estimated Annual Premium</b><br><br>
                        <span style="font-size:30px; color:#2ea043;">₹ {premium:,}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error("❌ API Error")
                st.code(response.text)

        except requests.exceptions.RequestException as e:
            st.error("🚫 Unable to connect to the Model API")
            st.caption(str(e))

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.divider()
st.markdown(
    "<p style='text-align:center; color:#8b949e;'>Built with ❤️ using Streamlit & FastAPI · Model served from Azure App Service</p>",
    unsafe_allow_html=True
)
