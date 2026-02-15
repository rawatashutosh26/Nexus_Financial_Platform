import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sklearn.ensemble import IsolationForest
import joblib  # Helps us save the model to a file

# --- CONFIGURATION ---
DB_USER = "postgres"
DB_PASS = "Rawat9640@"  # Your Password
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "nexus_db"

def get_db_engine():
    encoded_pass = quote_plus(DB_PASS)
    url = f"postgresql+pg8000://{DB_USER}:{encoded_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)

def train_ai():
    print("🤖 Connecting to Database to fetch training data...")
    engine = get_db_engine()
    
    # 1. Fetch Data
    # We grab the relevant numeric columns for training.
    # We LIMIT to 50,000 rows to keep training fast for this demo.
    query = """
    SELECT amount, old_balance_org, new_balance_orig, old_balance_dest, new_balance_dest 
    FROM transaction_logs 
    LIMIT 50000;
    """
    df = pd.read_sql(query, engine)
    
    print(f"📊 Loaded {len(df)} transactions for training.")
    
    if len(df) < 100:
        print("❌ Not enough data! Let the stream_engine.py run longer (aim for 1000+ rows).")
        return

    # 2. Feature Engineering (Optional but good)
    # The model learns better if we give it clean numeric data.
    # 'X' is the data the model studies.
    X = df[['amount', 'old_balance_org', 'new_balance_orig', 'old_balance_dest', 'new_balance_dest']]

    # 3. Initialize the Model (The Brain)
    # contamination=0.01 means we expect roughly 1% of data to be fraud (anomalies).
    print("🧠 Training Isolation Forest Model...")
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    
    # 4. Train
    model.fit(X)
    
    # 5. Save the Brain
    # We save the trained model to a file so the API can use it later without retraining.
    joblib.dump(model, 'models/fraud_model.pkl')
    
    print("✅ Model trained and saved to 'models/fraud_model.pkl'")
    print("   This model is now ready to detect fraud in real-time!")

if __name__ == "__main__":
    train_ai()