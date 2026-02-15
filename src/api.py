from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Initialize the App
app = FastAPI(title="Nexus Fraud Guard", version="1.0")

# 2. Load the Trained Brain (The Model)
# We load this ONCE when the server starts so it's fast.
try:
    model = joblib.load('models/fraud_model.pkl')
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("Did you run src/train_model.py first?")

# 3. Define the Input Format (What the Bank sends us)
class Transaction(BaseModel):
    amount: float
    old_balance_org: float
    new_balance_orig: float
    old_balance_dest: float
    new_balance_dest: float

# 4. The Prediction Endpoint
@app.post("/predict_fraud")
def predict(txn: Transaction):
    # Convert the incoming JSON to a DataFrame (the format the model expects)
    features = pd.DataFrame([[
        txn.amount, 
        txn.old_balance_org, 
        txn.new_balance_orig, 
        txn.old_balance_dest, 
        txn.new_balance_dest
    ]], columns=['amount', 'old_balance_org', 'new_balance_orig', 'old_balance_dest', 'new_balance_dest'])

    # Ask the model for a prediction
    # Result is -1 (Anomaly/Fraud) or 1 (Normal)
    prediction = model.predict(features)[0]
    
    if prediction == -1:
        return {
            "status": "BLOCKED", 
            "risk_score": "HIGH", 
            "reason": "Anomaly Detected by Isolation Forest"
        }
    else:
        return {
            "status": "APPROVED", 
            "risk_score": "LOW", 
            "reason": "Transaction looks normal"
        }