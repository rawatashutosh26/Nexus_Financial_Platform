# 🛡️ Nexus: Real-Time Financial Fraud Detection Platform

**Nexus** is an end-to-end financial intelligence platform designed to detect money laundering and fraud in high-velocity transaction streams. It ingests simulated banking logs, processes them via a live ETL pipeline, and uses an Isolation Forest Machine Learning model to flag anomalies in real-time.

<img width="1829" height="928" alt="Screenshot 2026-02-15 234345" src="https://github.com/user-attachments/assets/f264fb4e-693f-4e66-bc9b-504a8aa61115" />


## 🚀 Key Features

* **Real-Time Data Ingestion:** A Python-based engine that streams thousands of transactions into a PostgreSQL warehouse, simulating a live banking environment.
* **Machine Learning Fraud Detection:** Implements an **Isolation Forest** model (Scikit-Learn) to detect statistical outliers and "Account Takeover" patterns.
* **Live REST API:** A high-performance **FastAPI** microservice that serves risk predictions with <50ms latency.
* **Interactive Dashboard:** A **Streamlit** frontend for forensic analysis, allowing investigators to monitor live traffic and manually test suspicious transactions.

## 📸 Demo

### 1. Detecting High-Risk Fraud (Account Takeover)
The system automatically flags transactions that deviate from established user patterns (e.g., draining an account instantly).
<img width="1838" height="964" alt="Screenshot 2026-02-15 234307" src="https://github.com/user-attachments/assets/123e2c87-d16d-458c-8d43-a9d89e74df3c" />


### 2. Live Monitoring Dashboard
The dashboard updates every second, showing current transaction velocity and system health.
<img width="1829" height="928" alt="Screenshot 2026-02-15 234345" src="https://github.com/user-attachments/assets/45609dfb-dffb-4811-a20e-f60fd5c188aa" />


## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Database:** PostgreSQL
* **API Framework:** FastAPI
* **ML Engine:** Scikit-Learn (Isolation Forest)
* **Dashboard:** Streamlit & Plotly
* **Data Processing:** Pandas & SQLAlchemy

## 📂 Project Structure

```bash
nexus_financial_platform/
├── data/                   # Raw source data (PaySim dataset)
├── database/               # SQL Schema scripts
├── models/                 # Serialized ML models (.pkl)
├── screenshots/            # Demo images
├── src/
│   ├── api.py              # FastAPI Microservice
│   ├── dashboard.py        # Streamlit Frontend
│   ├── stream_engine.py    # Data Ingestion Engine
│   └── train_model.py      # ML Training Script
└── requirements.txt        # Dependencies
```
## ⚡ How to Run

### 1. Setup
```console
git clone [https://github.com/rawatashutosh26/Nexus_Financial_Platform.git]
cd nexus-financial-platform
pip install -r requirements.txt
```

### 2. Database
Ensure PostgreSQL is running and create the nexus_db database using the schema in database/. Update DB_PASS in the scripts with your credentials.

### 3. Run the System (3 Terminals)

**Terminal 1: Start the Data Stream**
```console
python src/stream_engine.py
```
**Terminal 2: Start the Fraud Detection API**
```console
uvicorn src.api:app --reload
```
**Terminal 3: Launch the Dashboard**
```console
streamlit run src/dashboard.py
```
