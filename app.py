import streamlit as st
from PIL import Image
from predict import predict_image
from dashboard import show_dashboard
from pdf_report import generate_pdf
import pandas as pd
from datetime import datetime
import os
import base64



st.set_page_config(
    page_title="DriveSense AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)



def add_bg():

    with open("images/background.png", "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
<style>

/* ---------- Background ---------- */

.stApp{{
background-image:
linear-gradient(
rgba(0,0,0,.65),
rgba(0,0,0,.65)),
url("data:image/png;base64,{encoded}");

background-size:cover;
background-position:center;
background-repeat:no-repeat;
background-attachment:fixed;
}}

/* ---------- Main Container ---------- */

.block-container{{
padding-top:2rem;
padding-bottom:2rem;
}}

/* ---------- Text ---------- */

h1,h2,h3,h4,h5,h6,p,label,span,div{{
color:white;
}}

/* ---------- Glass Cards ---------- */

.feature-card{{
background:rgba(15,35,60,.78);
backdrop-filter:blur(12px);
padding:22px;
border-radius:18px;
border:1px solid rgba(255,255,255,.18);
box-shadow:0 8px 20px rgba(0,0,0,.35);
color:white;
}}

/* ---------- Metrics ---------- */

[data-testid="metric-container"]{{
background:rgba(15,35,60,.78);
backdrop-filter:blur(12px);
border-radius:15px;
padding:15px;
border:1px solid rgba(255,255,255,.18);
}}

/* ---------- Buttons ---------- */

.stButton>button{{
width:100%;
height:52px;
border:none;
border-radius:12px;
background:#1565C0;
color:white;
font-size:18px;
font-weight:bold;
}}

.stButton>button:hover{{
background:#0D47A1;
}}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{{
background:rgba(10,20,40,.92);
backdrop-filter:blur(12px);
}}

/* ---------- DataFrame ---------- */

[data-testid="stDataFrame"]{{
background:rgba(15,35,60,.82);
border-radius:15px;
}}
/* ============================= */
/* File Uploader */
/* ============================= */

[data-testid="stFileUploader"]{{
    background:rgba(20,30,50,.75);
    border:2px dashed #4FC3F7;
    border-radius:15px;
    padding:20px;
}}

[data-testid="stFileUploader"] *{{
    color:white !important;
}}

.stDownloadButton > button{{
    width:100%;
    height:50px;
    background:#1976D2;
    color:white;
    font-size:17px;
    font-weight:bold;
    border-radius:10px;
    border:none;
}}

.stDownloadButton > button:hover{{
    background:#0D47A1;
    color:white;
}}

[data-testid="stFileUploader"] button{{
    background:#1565C0 !important;
    color:white !important;
    border-radius:8px;
}}

[data-testid="stFileUploaderDropzone"]{{
    background:rgba(20,30,50,.75) !important;
    border:2px dashed #42A5F5 !important;
    color:white !important;
}}

[data-testid="stFileUploaderDropzone"] *{{
    color:white !important;
}}

.stDownloadButton button p{{
    color:white !important;
}}

.stDownloadButton button span{{
    color:white !important;
}}

</style>
""",
        unsafe_allow_html=True,
    )

add_bg()



st.sidebar.image(
    "https://img.icons8.com/color/96/traffic-jam.png",
    width=100
)

st.sidebar.markdown("# 🚗 DriveSense AI")

st.sidebar.markdown("---")

st.sidebar.success("🟢 AI System Online")
st.sidebar.info("🧠 CNN Model Loaded")
st.sidebar.success("🎤 Voice Alert Ready")
st.sidebar.info("📷 Camera Detection Ready")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📂 Navigation",
    [
        "🏠 Home",
        "🔍 Predict",
        "📊 Dashboard",
        "📜 History",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 👨‍💻 Developer")
st.sidebar.write("**Akshay Biju**")
st.sidebar.caption("Department of Data Science")

st.sidebar.markdown("---")

st.sidebar.caption("DriveSense AI")
st.sidebar.caption("Version 2.1")



if menu == "🏠 Home":

    st.markdown("""
<div style="
background:rgba(15,35,60,0.75);
backdrop-filter:blur(15px);
padding:40px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.2);
text-align:center;
box-shadow:0px 8px 25px rgba(0,0,0,0.35);
">

<h1 class="main-title">🚗 DriveSense AI</h1>

<p class="sub-title">
AI Powered Traffic Sign Recognition & Driver Assistance System
</p>

</div>
""", unsafe_allow_html=True)

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🎯 Accuracy", "98.7%")
    c2.metric("🚦 Classes", "43")
    c3.metric("🧠 Model", "CNN")
    c4.metric("⚡ Status", "Ready")

    st.write("")

    

    st.subheader("🟢 AI System Status")

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.success("📷 Camera\n\nReady")

    with s2:
        st.success("🧠 CNN Model\n\nLoaded")

    with s3:
        st.success("🎤 Voice Alerts\n\nActive")

    with s4:
        st.success("⚡ System\n\nOnline")

    st.write("")

    

    a, b, c = st.columns(3)

    with a:

        st.markdown("""
<div class="feature-card">
<h3>🚦 Traffic Sign Detection</h3>

Detects and classifies 43 traffic signs using a deep learning CNN model.

</div>
""", unsafe_allow_html=True)

    with b:

        st.markdown("""
<div class="feature-card">
<h3>🚗 Driver Assistance</h3>

Provides intelligent recommendations and voice alerts for high-risk traffic signs.

</div>
""", unsafe_allow_html=True)

    with c:

        st.markdown("""
<div class="feature-card">
<h3>📊 Prediction History</h3>

Stores prediction history for analytics, reporting, and performance tracking.

</div>
""", unsafe_allow_html=True)

    st.write("")

   


elif menu == "🔍 Predict":

    st.markdown("""
<div style="
background:rgba(15,35,60,.78);
padding:30px;
border-radius:18px;
border:1px solid rgba(255,255,255,.18);
text-align:center;
box-shadow:0px 8px 20px rgba(0,0,0,.35);
">

<h2 style="color:white;">
🚦 AI Traffic Sign Recognition
</h2>

<p style="color:white;font-size:18px;">
Upload a traffic sign image and let the CNN model identify it instantly.
</p>

</div>
""", unsafe_allow_html=True)

    st.write("")

    uploaded_file = st.file_uploader(
        "📤 Upload Traffic Sign Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        left, right = st.columns([1,1])

        

        with left:

            st.subheader("🖼 Uploaded Image")

            st.image(
                image,
                use_container_width=True
            )

        

        with right:

            st.subheader("🤖 AI Analysis")

            st.info("""
### 🧠 AI Status

1. CNN Model : Loaded

2. Input Size : 128 × 128

3. Traffic Sign Classes : 43

4. Prediction Engine : Ready
""")

            if st.button("🚀 Start AI Analysis"):

                with st.spinner("🚀 Running CNN Model... Please wait..."):

                    result = predict_image(image)

                current_date = datetime.now().strftime("%d-%m-%Y")
                current_time = datetime.now().strftime("%I:%M:%S %p")

                os.makedirs("history", exist_ok=True)

                csv_file = "history/predictions.csv"

                new_prediction = pd.DataFrame({

                    "Date":[current_date],
                    "Time":[current_time],
                    "Traffic Sign":[result["sign"]],
                    "Confidence":[round(result["confidence"],2)]

                })

                if os.path.exists(csv_file):

                    history = pd.read_csv(csv_file)

                    history = pd.concat(
                        [history,new_prediction],
                        ignore_index=True
                    )

                else:

                    history = new_prediction

                history.to_csv(csv_file,index=False)

                st.success("✅ AI Analysis Completed Successfully")

                st.divider()

                st.markdown("""
## 🤖 AI Prediction Result

The uploaded traffic sign has been successfully analyzed by the CNN model.
""")

                c1, c2 = st.columns(2)

                with c1:

                    st.metric(
                        "🚦 Traffic Sign",
                        result["sign"]
                    )

                    st.metric(
                        "🎯 Confidence",
                        f"{result['confidence']:.2f}%"
                    )

                with c2:

                    st.metric(
                        "⚠ Risk Level",
                        result["risk"]
                    )

                    st.metric(
                        "📅 Date",
                        current_date
                    )

                st.divider()

                

                if result["confidence"] >= 95:

                    st.success("🟢 Excellent Detection Accuracy")

                elif result["confidence"] >= 85:

                    st.info("🔵 Very Good Detection Accuracy")

                elif result["confidence"] >= 70:

                    st.warning("🟡 Moderate Detection Accuracy")

                else:

                    st.error("🔴 Low Detection Accuracy")

                st.subheader("📈 Prediction Confidence")

                st.progress(result["confidence"]/100)

                if result["confidence"] >= 95:
                    st.success("Prediction Reliability : Excellent")

                elif result["confidence"] >= 85:
                    st.info("Prediction Reliability : Very Good")

                elif result["confidence"] >= 70:
                    st.warning("Prediction Reliability : Moderate")

                else:
                    st.error("Prediction Reliability : Low")

                st.write(
                    f"Confidence Score : **{result['confidence']:.2f}%**"
                )

                st.caption(
                    f"Generated on {current_date} at {current_time}"
                )

                st.divider()

                left_box, right_box = st.columns(2)

                with left_box:

                    st.warning(f"""
### 🚗 Driver Recommendation

{result["action"]}
""")

                with right_box:

                    st.info(f"""
### 📘 Traffic Rule

{result["rule"]}
""")

                st.divider()

                pdf_path = generate_pdf(result)

                with open(pdf_path,"rb") as pdf_file:

                    st.download_button(
                        "📄 Download AI Report",
                        pdf_file,
                        file_name="DriveSense_Report.pdf",
                        mime="application/pdf"
                    )


elif menu == "📊 Dashboard":

    show_dashboard()



elif menu == "📜 History":

    st.markdown("""
<div style="
background:rgba(15,35,60,.78);
padding:30px;
border-radius:18px;
border:1px solid rgba(255,255,255,.18);
text-align:center;
box-shadow:0px 8px 20px rgba(0,0,0,.35);
">

<h2 style="color:white;">
📜 Prediction History
</h2>

<p style="color:white;">
Manage all AI predictions generated by DriveSense AI.
</p>

</div>
""", unsafe_allow_html=True)

    st.write("")

    csv_file = "history/predictions.csv"

    if os.path.exists(csv_file):

        history = pd.read_csv(csv_file)

        if history.empty:

            st.warning("No prediction history available.")

        else:

            total = len(history)
            avg = history["Confidence"].mean()
            top = history["Traffic Sign"].mode()[0]

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    "📊 Total Predictions",
                    total
                )

            with m2:
                st.metric(
                    "🎯 Average Confidence",
                    f"{avg:.2f}%"
                )

            with m3:
                st.metric(
                    "🏆 Most Detected",
                    top
                )

            st.divider()

            st.subheader("🔍 Search Prediction")

            search = st.text_input(
                "",
                placeholder="Search Traffic Sign..."
            )

            if search:

                history = history[
                    history["Traffic Sign"].str.contains(
                        search,
                        case=False,
                        na=False
                    )
                ]

            st.dataframe(
                history.sort_values(
                    by=["Date","Time"],
                    ascending=False
                ),
                use_container_width=True,
                hide_index=True,
                height=420
            )

            st.divider()

            c1, c2 = st.columns(2)

            with c1:

                st.download_button(
                    "📥 Download CSV",
                    history.to_csv(index=False),
                    file_name="Prediction_History.csv",
                    mime="text/csv"
                )

            with c2:

                if st.button("🗑 Clear History"):

                    pd.DataFrame(
                        columns=[
                            "Date",
                            "Time",
                            "Traffic Sign",
                            "Confidence"
                        ]
                    ).to_csv(csv_file,index=False)

                    st.success("History Cleared Successfully")

                    st.rerun()

    else:

        st.error("Prediction history not found.")

else:

    st.markdown("""
<div style="
background:rgba(15,35,60,.78);
padding:35px;
border-radius:20px;
border:1px solid rgba(255,255,255,.18);
text-align:center;
box-shadow:0px 8px 25px rgba(0,0,0,.35);
">

<h1 style="color:white;">
🚗 DriveSense AI
</h1>

<h3 style="color:white;">
AI Powered Traffic Sign Recognition & Driver Assistance System
</h3>

<p style="color:white;font-size:18px;">
Recognizing traffic signs using Deep Learning for safer driving.
</p>

</div>
""", unsafe_allow_html=True)

    st.write("")

    
    st.header("📌 Project Overview")

    st.write("""

DriveSense AI is an AI-powered Traffic Sign Recognition System developed using a Convolutional Neural Network (CNN).

The system automatically detects traffic signs from uploaded images or live camera input and provides:

1. Traffic Sign Recognition

2. Driver Recommendations

3. Road Safety Rules

4. Risk Level Detection

5. Prediction Confidence

6. Prediction History

7. Dashboard Analytics

8. PDF Report Generation

""")

    st.divider()

    

    st.header("🚀 Core Features")

    c1, c2 = st.columns(2)

    with c1:

        st.info("""
### 🤖 AI Features

1. CNN Traffic Sign Recognition

2. 43 Traffic Sign Classes

3. Real-Time Camera Detection

4. Voice Alert Support

5. Confidence Analysis

6. Risk Detection
""")

    with c2:

        st.success("""
### 📊 Smart Features

1. Driver Recommendation

2. Prediction History

3. Analytics Dashboard

4. PDF Report Generation

5. Interactive UI

6. Fast AI Prediction
""")

    st.divider()

   
    st.header("🧠 AI Model")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Dataset", "GTSRB")
    m2.metric("Classes", "43")
    m3.metric("Model", "CNN")
    m4.metric("Accuracy", "98.7%")

    st.divider()

    

    st.header("🛠 Technology Stack")

    t1, t2, t3 = st.columns(3)

    with t1:

        st.success("""
### Programming

1. Python

2. NumPy

3. Pandas

4. OpenCV
""")

    with t2:

        st.info("""
### Deep Learning

1. TensorFlow

2. Keras

3. CNN

4. Pillow
""")

    with t3:

        st.warning("""
### Interface

1. Streamlit

2. Matplotlib

3. PDF Reports

4. Analytics Dashboard
""")

    st.divider()

    

    st.header("🔄 AI Workflow")

    st.markdown("""

1️⃣ Upload Traffic Sign Image

⬇️

2️⃣ Image Preprocessing

⬇️

3️⃣ CNN Prediction

⬇️

4️⃣ Confidence Calculation

⬇️

5️⃣ Risk Analysis

⬇️

6️⃣ Driver Recommendation

⬇️

7️⃣ Save Prediction History

⬇️

8️⃣ Generate PDF Report

""")

    st.divider()

    

    st.header("👨‍💻 Developer")

    st.success("""

Name : **Akshay Biju**

Department : **Data Science**

Project : **DriveSense AI**

Technology : **Deep Learning | Computer Vision | Streamlit**

""")

    st.divider()

    st.caption(
        "© 2026 DriveSense AI | Built using Python, TensorFlow, OpenCV & Streamlit"
    )