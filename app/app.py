import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Lottery Prediction AI", layout="wide")

@st.cache_resource
def load_assets():
    model = joblib.load('lottery_model.pkl')
    features = joblib.load('model_features.pkl')
    test_data = pd.read_csv('../data/lottery_test.csv', index_col=0)

    return model, features, test_data

try:
    model, feature_cols, test_df = load_assets()
except FileNotFoundError:
    st.error("File model atau data tidak ditemukan!")
    st.stop()

st.title("AI Lottery Prediction")
st.markdown("Random Forest dengan pendekatan Time-Series Rolling Window.")

st.sidebar.header("Sidebar")
available_dates = test_df.index.unique()
selected_date = st.sidebar.selectbox("Pilih Tanggal:", available_dates)

def get_prediction(date):
    row = test_df.loc[[date]] 
    X_input = row[feature_cols]
    y_true_cols = [c for c in test_df.columns if 'num_' in c]
    y_true_row = row[y_true_cols].values.flatten()
    true_balls = np.where(y_true_row == 1)[0] + 1
    
    probs = model.predict_proba(X_input)
    probs_matrix = np.array([p[:, 1] for p in probs]).T
    top_6_indices = np.argsort(probs_matrix[0])[-6:][::-1]
    pred_balls = top_6_indices + 1
    
    return pred_balls, true_balls

if st.sidebar.button("Prediksi"):
    pred_balls, true_balls = get_prediction(selected_date)

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Prediksi")
        html_pred = ""

        for ball in pred_balls:
            if ball in true_balls:
                html_pred += f"<span style='background-color:#28a745; color:white; padding:10px; border-radius:50%; margin:5px; font-weight:bold; font-size:20px'>{ball}</span>"
            else:
                html_pred += f"<span style='background-color:#6c757d; color:white; padding:10px; border-radius:50%; margin:5px; font-weight:bold; font-size:20px'>{ball}</span>"
        st.markdown(html_pred, unsafe_allow_html=True)

    with col2:
        st.subheader("Aktual")
        html_true = ""

        for ball in true_balls:
            html_true += f"<span style='border: 2px solid #007bff; color:#007bff; padding:10px; border-radius:50%; margin:5px; font-weight:bold; font-size:20px'>{ball}</span>"
        st.markdown(html_true, unsafe_allow_html=True)
        
    st.divider()
    matches = set(pred_balls).intersection(set(true_balls))
    jml_benar = len(matches)
    
    st.metric("Akurasi Prediksi Hari Ini", f"{jml_benar} Benar dari 6")
    
    if jml_benar >= 3:
        st.success("Model berhasil menebak 3 angka atau lebih!")
    elif jml_benar >= 1:
        st.info("Model berhasil menebak beberapa pola.")
    else:
        st.warning("Model kesulitan menebak pola")

else:
    st.info("Silakan pilih tanggal terlebih dahulu")