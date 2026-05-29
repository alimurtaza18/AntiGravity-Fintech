import csv
import random
from datetime import datetime, timedelta

def generate_data(filename="transactions.csv", num_rows=5000):
    categories = ["Food & Dining", "Shopping", "Utilities", "Entertainment", "Travel", "Healthcare", "Groceries"]
    standard_locations = ["New York, USA", "London, UK", "Tokyo, Japan", "Paris, France", "Berlin, Germany", 
                          "Sydney, Australia", "Toronto, Canada", "San Francisco, USA", "Singapore", "Mumbai, India"]
    
    # We will generate a base start date around 30 days ago
    start_date = datetime.now() - timedelta(days=30)
    
    transactions = []
    
    # 1. First generate normal transactions
    for i in range(num_rows):
        txn_id = f"TXN{100000 + i}"
        user_id = f"USR{random.randint(1001, 1200)}" # 200 unique users
        
        # Normal amount: typical spending is between $5.00 and $300.00, slightly skewed to lower amounts
        amount = round(random.uniform(5.0, 300.0) if random.random() > 0.1 else random.uniform(300.0, 1500.0), 2)
        
        # Add random seconds to start_date to distribute transactions over 30 days
        random_seconds = random.randint(0, 30 * 24 * 60 * 60)
        timestamp = (start_date + timedelta(seconds=random_seconds)).strftime("%Y-%m-%d %H:%M:%S")
        
        category = random.choice(categories)
        location = random.choice(standard_locations)
        
        transactions.append({
            "Transaction_ID": txn_id,
            "User_ID": user_id,
            "Amount": amount,
            "Timestamp": timestamp,
            "Category": category,
            "Location": location
        })
        
    # 2. Inject specific anomalies at random indexes
    anomalies = [
        # Huge amounts (standard max is $1500, let's make these massive)
        {"Amount": 999999.99, "Location": "New York, USA", "Category": "Shopping", "reason": "Extremely huge transaction"},
        {"Amount": 500000.00, "Location": "London, UK", "Category": "Travel", "reason": "Extremely huge transaction"},
        {"Amount": 250000.00, "Location": "Tokyo, Japan", "Category": "Entertainment", "reason": "Extremely huge transaction"},
        
        # Weird locations
        {"Amount": 45.50, "Location": "Atlantis (Underwater)", "Category": "Food & Dining", "reason": "Fictional location"},
        {"Amount": 120.00, "Location": "Mars Colony Alpha", "Category": "Shopping", "reason": "Fictional location"},
        {"Amount": 15.00, "Location": "Null Island (0,0)", "Category": "Utilities", "reason": "Coordinate anomaly location"},
        {"Amount": 3000.00, "Location": "Deep Space Station 9", "Category": "Travel", "reason": "Fictional location"},
        
        # Both huge amount and weird location
        {"Amount": 750000.00, "Location": "Secret Bunker, Unknown", "Category": "Healthcare", "reason": "Huge amount and suspicious location"},
        {"Amount": 1234567.89, "Location": "The Moon", "Category": "Entertainment", "reason": "Huge amount and fictional location"},
    ]
    
    print(f"Injecting {len(anomalies)} pre-defined anomalies into the dataset...")
    
    # Choose unique random indices to replace with anomalies
    anomaly_indices = random.sample(range(num_rows), len(anomalies))
    
    for idx, anomaly in zip(anomaly_indices, anomalies):
        orig_txn = transactions[idx]
        # Keep original ID, User_ID, Timestamp, but overwrite Amount, Location, Category (if provided)
        orig_txn["Amount"] = anomaly["Amount"]
        orig_txn["Location"] = anomaly["Location"]
        if "Category" in anomaly:
            orig_txn["Category"] = anomaly["Category"]
        
        # Print for tracking
        print(f"Injected anomaly at index {idx}: ID={orig_txn['Transaction_ID']}, User={orig_txn['User_ID']}, Amount=${orig_txn['Amount']}, Location='{orig_txn['Location']}' ({anomaly['reason']})")
        
    # Write to CSV
    fields = ["Transaction_ID", "User_ID", "Amount", "Timestamp", "Category", "Location"]
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(transactions)
        
    print(f"Successfully generated {num_rows} transactions in '{filename}'!")

if __name__ == "__main__":
    generate_data("transactions.csv", 5000)
