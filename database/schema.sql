-- 1. Create the Table to hold transactions
-- We drop it first just in case it already exists (prevents errors if you run this twice)
DROP TABLE IF EXISTS transaction_logs;

CREATE TABLE transaction_logs (
    -- Unique ID for our database to track rows (Auto-incrementing)
    id SERIAL PRIMARY KEY,

    -- The 'time' unit from the simulation (1 step = 1 hour)
    step INT,

    -- The type of transaction (e.g., 'PAYMENT', 'CASH_OUT')
    type VARCHAR(20),

    -- The amount of money moved
    amount DECIMAL(15, 2),

    -- The Customer ID who sent the money (e.g., 'C12345')
    name_orig VARCHAR(50),

    -- Sender's balance BEFORE transaction
    old_balance_org DECIMAL(15, 2),

    -- Sender's balance AFTER transaction
    new_balance_orig DECIMAL(15, 2),

    -- The Recipient ID (who got the money)
    name_dest VARCHAR(50),

    -- Recipient's balance BEFORE transaction
    old_balance_dest DECIMAL(15, 2),

    -- Recipient's balance AFTER transaction
    new_balance_dest DECIMAL(15, 2),

    -- 1 = Actual Fraud (from the dataset), 0 = Legit
    is_fraud INT,

    -- 1 = Flagged by old system, 0 = Not flagged
    is_flagged_fraud INT,

    -- A timestamp for when YOUR system processed this row
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


SELECT * FROM transaction_logs;