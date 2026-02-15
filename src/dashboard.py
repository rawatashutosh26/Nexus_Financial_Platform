import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/predict_fraud"
DB_USER = "postgres"
DB_PASS = "Rawat9640@"  # Your Password
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "nexus_db"

# --- DATABASE CONNECTION ---
def get_db_connection():
    encoded_pass = quote_plus(DB_PASS)
    url = f"postgresql+pg8000://{DB_USER}:{encoded_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)

# --- PAGE SETUP ---
st.set_page_config(page_title="Nexus Fraud Guard", page_icon="🛡️", layout="wide")

st.title("🛡️ Nexus Financial Intelligence Platform")
st.markdown("Real-time transaction monitoring and fraud detection system.")

# --- SIDEBAR: MANUAL FRAUD CHECK ---
st.sidebar.header("🕵️‍♂️ Manual Investigator")
st.sidebar.write("Input transaction details to check for fraud:")

amt = st.sidebar.number_input("Amount ($)", value=1000.0)
old_org = st.sidebar.number_input("Sender Old Balance", value=1000.0)
new_org = st.sidebar.number_input("Sender New Balance", value=0.0)
old_dest = st.sidebar.number_input("Receiver Old Balance", value=0.0)
new_dest = st.sidebar.number_input("Receiver New Balance", value=1000.0)

if st.sidebar.button("Check Risk"):
    # payload matches the class in api.py
    payload = {
        "amount": amt,
        "old_balance_org": old_org,
        "new_balance_orig": new_org,
        "old_balance_dest": old_dest,
        "new_balance_dest": new_dest
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()
        
        if result["status"] == "BLOCKED":
            st.sidebar.error(f"🚨 BLOCKED! Risk: {result['risk_score']}")
        else:
            st.sidebar.success(f"✅ APPROVED. Risk: {result['risk_score']}")
            
    except Exception as e:
        st.sidebar.error(f"Error connecting to API: {e}")

# --- MAIN DASHBOARD: LIVE STATS ---
# We use a placeholder to update metrics dynamically
placeholder = st.empty()

# Refresh Loop (simulates live monitoring)
for seconds in range(200):
    engine = get_db_connection()
    
    # 1. Fetch Live Stats
    with engine.connect() as conn:
        # Get total count
        count_df = pd.read_sql("SELECT count(*) as count FROM transaction_logs", conn)
        total_txns = count_df.iloc[0]['count']
        
        # Get recent transactions for the chart
        recent_df = pd.read_sql("SELECT * FROM transaction_logs ORDER BY id DESC LIMIT 100", conn)

    with placeholder.container():
        # KPI Metrics
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="Total Transactions Processed", value=f"{total_txns:,}")
        kpi2.metric(label="Current Stream Velocity", value="1 txn/sec")
        kpi3.metric(label="System Status", value="🟢 ONLINE")

        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Transaction Volume (Live)")
            fig = px.line(recent_df, x='id', y='amount', title="Recent Transaction Amounts")
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("📝 Recent Logs")
            st.dataframe(recent_df[['type', 'amount', 'name_orig']].head(10))
            
    # Refresh every 1 second
    time.sleep(1)