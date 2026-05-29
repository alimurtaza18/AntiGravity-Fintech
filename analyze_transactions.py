import csv
import math

def analyze(input_file="transactions.csv", output_file="high_risk_transactions.csv"):
    transactions = []
    
    # Read the transaction CSV
    with open(input_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse amount as float
            row["Amount"] = float(row["Amount"])
            transactions.append(row)
            
    num_txns = len(transactions)
    if num_txns == 0:
        print("No transactions found.")
        return
        
    # 1. Calculate average transaction amount
    total_amount = sum(t["Amount"] for t in transactions)
    mean_amount = total_amount / num_txns
    
    # 2. Calculate standard deviation
    variance = sum((t["Amount"] - mean_amount) ** 2 for t in transactions) / num_txns
    std_dev = math.sqrt(variance)
    
    # 3. Calculate total spending per category
    category_spending = {}
    for t in transactions:
        cat = t["Category"]
        category_spending[cat] = category_spending.get(cat, 0.0) + t["Amount"]
        
    # 4. Identify high-risk transactions (> 3 standard deviations from the average)
    high_risk_threshold = mean_amount + (3 * std_dev)
    low_risk_threshold = mean_amount - (3 * std_dev)
    
    high_risk_txns = []
    for t in transactions:
        # Check if amount is > mean + 3*std_dev or < mean - 3*std_dev
        if t["Amount"] > high_risk_threshold or t["Amount"] < low_risk_threshold:
            high_risk_txns.append(t)
            
    # Print results to console
    print("=== TRANSACTION ANALYSIS REPORT ===")
    print(f"Total Transactions Analyzed: {num_txns}")
    print(f"Average Transaction Amount: ${mean_amount:.2f}")
    print(f"Standard Deviation: ${std_dev:.2f}")
    print(f"High-Risk Upper Threshold (> 3 Std Dev): ${high_risk_threshold:.2f}")
    
    print("\n--- Total Spending Per Category ---")
    # Sort categories by total spending descending
    sorted_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)
    for cat, total in sorted_categories:
        print(f"  {cat}: ${total:,.2f}")
        
    print(f"\n--- High-Risk Transactions Found ({len(high_risk_txns)}) ---")
    for t in high_risk_txns:
        deviation = (t["Amount"] - mean_amount) / std_dev
        print(f"  ID: {t['Transaction_ID']} | User: {t['User_ID']} | Amount: ${t['Amount']:,.2f} | Location: {t['Location']} | Std Devs from Mean: {deviation:.2f}")
        
    # 5. Save high-risk flags into a new file
    if high_risk_txns:
        fields = ["Transaction_ID", "User_ID", "Amount", "Timestamp", "Category", "Location", "Deviation_StdDev"]
        with open(output_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for t in high_risk_txns:
                deviation = (t["Amount"] - mean_amount) / std_dev
                row_to_write = {
                    "Transaction_ID": t["Transaction_ID"],
                    "User_ID": t["User_ID"],
                    "Amount": t["Amount"],
                    "Timestamp": t["Timestamp"],
                    "Category": t["Category"],
                    "Location": t["Location"],
                    "Deviation_StdDev": round(deviation, 2)
                }
                writer.writerow(row_to_write)
        print(f"\nSuccessfully saved {len(high_risk_txns)} high-risk transactions to '{output_file}'!")
    else:
        print("\nNo high-risk transactions found to save.")

if __name__ == "__main__":
    analyze()
