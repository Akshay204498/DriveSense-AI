import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


def show_dashboard():

    

    st.markdown("""
    <div style="
    background:rgba(15,35,60,.75);
    padding:30px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,.15);
    text-align:center;
    box-shadow:0px 8px 20px rgba(0,0,0,.35);
    ">

    <h1 style="color:white;">
    🚦 DriveSense AI Dashboard
    </h1>

    <h3 style="color:white;">
    Traffic Sign Recognition Analytics
    </h3>

    <p style="color:white;">
    Real-Time Prediction Statistics & AI Performance
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    csv_file = "history/predictions.csv"

    if not os.path.exists(csv_file):
        st.error("Prediction history not found.")
        return

    history = pd.read_csv(csv_file)

    if history.empty:
        st.warning("No prediction history available.")
        return

    

    total_predictions = len(history)
    average_confidence = history["Confidence"].mean()
    top_sign = history["Traffic Sign"].mode()[0]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "📊 Total Predictions",
            total_predictions
        )

    with c2:
        st.metric(
            "🎯 Average Confidence",
            f"{average_confidence:.1f}%"
        )

    with c3:
        st.metric(
            "🏆 Most Detected Sign",
            top_sign
        )

    st.divider()

    
    st.subheader("📊 Top 10 Most Detected Traffic Signs")

    sign_counts = history["Traffic Sign"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10,6))

    ax.barh(
        sign_counts.index[::-1],
        sign_counts.values[::-1],
        edgecolor="black"
    )

    ax.set_xlabel("Number of Predictions")
    ax.set_ylabel("Traffic Sign")
    ax.set_title("Top 10 Traffic Signs")

    plt.tight_layout()

    st.pyplot(fig)

    st.divider()

    

    st.subheader("📈 Top 5 Prediction Distribution")

    top5 = history["Traffic Sign"].value_counts().head(5)

    fig2, ax2 = plt.subplots(figsize=(6,6))

    ax2.pie(
        top5.values,
        labels=top5.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax2.axis("equal")

    st.pyplot(fig2)

    st.divider()

    

    st.subheader("📌 Dashboard Insights")

    st.info(f"""
### Dashboard Summary

🏆 **Most Detected Sign:** {top_sign}

🎯 **Average Confidence:** {average_confidence:.2f}%

📊 **Total Predictions:** {total_predictions}
""")

    st.divider()

    

    st.subheader("📋 Latest Predictions")

    latest = history.sort_values(
        by=["Date", "Time"],
        ascending=False
    ).head(15)

    st.dataframe(
        latest,
        use_container_width=True,
        hide_index=True,
        height=400
    )