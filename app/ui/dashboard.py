import streamlit as st
import requests
import time
import plotly.graph_objects as go

# -----------------------------
# 1. PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Sleep AI | Pro",
    layout="wide",
    page_icon="💤",
    initial_sidebar_state="expanded"
)

# CRITICAL: Pointing to Port 8001
API_URL = "http://127.0.0.1:8001/predict"

# -----------------------------
# 2. CUSTOM DARK THEME CSS
# -----------------------------
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(to bottom, #0f172a, #1e293b);
        color: #f8fafc;
    }

    /* Sidebar Background & Text */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }

    /* FIX: Force Input Boxes to Dark Blue */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #475569 !important;
    }
    input { color: white !important; }
    ul[data-baseweb="menu"] { background-color: #1e293b !important; }

    /* Cards */
    .stCard, div[data-testid="metric-container"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(90deg, #4f46e5, #818cf8);
        border: none;
        color: white;
        font-weight: bold;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 3. HELPER FUNCTIONS
# -----------------------------
def create_gauge_chart(score, label):
    color = "#ef4444" if score < 50 else "#f97316" if score < 80 else "#22c55e"
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': label, 'font': {'size': 24, 'color': 'white'}},
        number = {'font': {'color': 'white'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#334155",
            'steps': [{'range': [0, 100], 'color': '#1e293b'}] 
        }
    ))
    # FIX: Removed deprecated use_container_width logic here, handled in chart call
    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "white"}, height=250)
    return fig

def create_radar_chart(input_data):
    categories = ['Sleep Duration', 'Physical Activity', 'Low Stress', 'Steps']
    user_vals = [
        min(input_data['sleep_duration'], 10),
        min(input_data['physical_activity'] / 10, 10),
        10 - input_data['stress_level'], 
        min(input_data['daily_steps'] / 1000, 10)
    ]
    ideal_vals = [8, 6, 8, 8]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=user_vals, theta=categories, fill='toself', name='You', line_color='#818cf8'))
    fig.add_trace(go.Scatterpolar(r=ideal_vals, theta=categories, fill='toself', name='Ideal', line_color='rgba(255, 255, 255, 0.2)', line_dash='dot'))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10], tickfont=dict(color='gray')), bgcolor='rgba(0,0,0,0)'),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True,
        height=300,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    return fig

# -----------------------------
# 4. SIDEBAR & MAIN
# -----------------------------
with st.sidebar:
    # [FIX] Using the Direct URL prevents the "MediaFileStorageError"
    st.image("https://openmoji.org/data/color/png/1F634.png", width=80)
    st.title("User Profile")
    st.markdown("---")
    
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", 10, 90, 25)
    occupation = st.selectbox("Occupation", ["Software Engineer", "Doctor", "Sales Representative", "Teacher", "Nurse", "Engineer", "Accountant", "Scientist", "Lawyer", "Salesperson", "Other"])
    bmi = st.selectbox("BMI", ["Normal", "Overweight", "Obese", "Underweight"])
    sleep_disorder = st.selectbox("Sleep Disorder", ["None", "Insomnia", "Sleep Apnea"])
    
    st.markdown("### ❤️ Vitals")
    heart_rate = st.slider("Heart Rate (bpm)", 40, 120, 72)
    systolic = st.number_input("Systolic BP", 90, 180, 120)
    diastolic = st.number_input("Diastolic BP", 60, 120, 80)
    st.info("Adjust sliders in main view.")

st.title("🧬 Sleep Quality Predictor")
st.markdown("### Analyze your daily biometrics and sleep patterns.")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🌙 Sleep Duration**")
    sleep_duration = st.slider("Hours", 3.0, 12.0, 7.0, 0.1, label_visibility="collapsed")
    bedtime_hour = st.slider("Bedtime Hour (24h)", 0, 23, 22)
    st.caption(f"Target: 7-9 hours")
with col2:
    st.markdown("**🔥 Physical Activity**")
    physical_activity = st.slider("Minutes", 0, 180, 45, 5, label_visibility="collapsed")
    st.caption("Target: >30 mins")
with col3:
    st.markdown("**🧠 Stress Level**")
    stress_level = st.slider("Level (1-10)", 1, 10, 5, 1, label_visibility="collapsed")
    st.caption("Target: <5")

daily_steps = st.slider("👣 Daily Steps", 0, 20000, 6000, 500)
st.markdown("<br>", unsafe_allow_html=True)

# [FIX] Replaced 'use_container_width=True' with 'width="stretch"' to fix deprecation warning
predict_btn = st.button("🚀 Analyze Sleep Quality", width="stretch")

if predict_btn:
    payload = {
        "age": age, "gender": gender, "occupation": occupation,
        "sleep_duration": sleep_duration, "bedtime_hour": bedtime_hour,
        "physical_activity": physical_activity, "stress_level": stress_level,
        "bmi_category": bmi, "heart_rate": heart_rate,
        "daily_steps": daily_steps, "sleep_disorder": sleep_disorder,
        "blood_pressure_systolic": systolic, "blood_pressure_diastolic": diastolic
    }

    try:
        with st.spinner("Analyzing..."):
            time.sleep(0.5)
            response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            score = data.get('score', 0)
            pred = data.get('label', 'Unknown')
            
            # ANIMATION LOGIC
            if pred in ["Good", "Elite"]:
                st.snow()
                st.toast("Great job!", icon="🎉")
            elif pred == "Average":
                st.toast("Room for improvement.", icon="⚠️")
            else:
                st.toast("Issues detected.", icon="🚨")

            st.markdown("---")
            row1_1, row1_2 = st.columns([1, 2])
            with row1_1:
                # [FIX] Updated chart parameter for new Streamlit version
                st.plotly_chart(create_gauge_chart(score, f"Quality: {pred}"), width="stretch")
            with row1_2:
                st.subheader("📊 Analysis Summary")
                m1, m2, m3 = st.columns(3)
                m1.metric("Sleep Score", f"{score}/100", delta=f"{score-70}")
                m2.metric("Stress Factor", f"{stress_level}/10", delta_color="inverse")
                m3.metric("Chronotype", data.get('chronotype', 'Bear'))
                st.info(f"**AI Insight:** Predicted quality: **{pred}**.")

            row2_1, row2_2 = st.columns([1, 1])
            with row2_1:
                st.markdown("### ⚖️ Life Balance")
                # [FIX] Updated chart parameter
                st.plotly_chart(create_radar_chart(payload), width="stretch")
            with row2_2:
                st.markdown("### 🩺 Recommendations")
                recs = data.get('recommendations', [])
                if recs:
                    with st.expander("💡 Improvement Plan", expanded=True):
                        for tip in recs:
                            st.success(f"• {tip}")
                else:
                    st.info("No recommendations found.")
        else:
            st.error(f"Server Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error(f"🚨 Connection Refused. Is backend running on Port 8001?")