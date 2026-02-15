import pandas as pd
import time
from sqlalchemy import create_engine
from urllib.parse import quote_plus  # <--- NEW IMPORT

# --- CONFIGURATION ---
DB_USER = "postgres"
DB_PASS = "DATABASIE_PASSWORD"
DB_HOST = "127.0.0.1"   # We use IP instead of 'localhost' for better Windows stability
DB_PORT = "5432"
DB_NAME = "nexus_db"

# Update this path if your file is named something else!
CSV_FILE_PATH = "data/paysim dataset.csv" 

# --- 1. ESTABLISH DATABASE CONNECTION ---
def get_db_engine():
    """
    Creates a connection bridge to the PostgreSQL database.
    """
    # We 'encode' the password. 
    encoded_pass = quote_plus(DB_PASS)
    
    # We use pg8000 driver which is safer for Windows
    url = f"postgresql+pg8000://{DB_USER}:{encoded_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    engine = create_engine(url)
    return engine

# --- 2. THE STREAMING LOGIC ---
def start_stream():
    engine = get_db_engine()
    print("🚀 Connecting to Nexus Database...")
    print(f"📂 Reading data from: {CSV_FILE_PATH}")
    print("------------------------------------------------")

    try:
        # chunksize=1 simulates real-time (1 transaction at a time)
        chunk_iterator = pd.read_csv(CSV_FILE_PATH, chunksize=1)
        
        for i, chunk in enumerate(chunk_iterator):
            
            # --- DATA TRANSFORMATION ---
            # Mapping columns EXACTLY as seen in your CSV screenshot
            chunk = chunk.rename(columns={
                'step': 'step',
                'type': 'type',
                'amount': 'amount',
                'nameOrig': 'name_orig',
                'oldbalanceOrg': 'old_balance_org',
                'newbalanceOrig': 'new_balance_orig',
                'nameDest': 'name_dest',
                'oldbalanceDest': 'old_balance_dest',
                'newbalanceDest': 'new_balance_dest',
                'isFraud': 'is_fraud',
                'isFlaggedFraud': 'is_flagged_fraud'
            })

            # --- INSERT INTO DATABASE ---
            chunk.to_sql('transaction_logs', engine, if_exists='append', index=False)
            
            # --- VISUALIZATION ---
            txn_type = chunk.iloc[0]['type']
            amount = chunk.iloc[0]['amount']
            sender = chunk.iloc[0]['name_orig']
            
            print(f" -> [STREAM] Transaction: {txn_type} | Amount: ${amount:,.2f} | Sender: {sender}")
            
            # Speed control: sleep 0.1s. Reduce to 0.01s if you want it faster.
            time.sleep(0.1)

    except FileNotFoundError:
        print(f"❌ Error: Could not find file at {CSV_FILE_PATH}")
        print("   Make sure the file name in the code matches the file in your 'data' folder!")
    except KeyboardInterrupt:
        print("\n🛑 Stream stopped by user.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    start_stream()