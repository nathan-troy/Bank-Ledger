import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

first_names = ["Nathan", "Joseph", "Ross", "Kyle", "Martin", "Henry", "William", "John", "Mary", "Jane", "Peter", "Bruce", "Clark", "Homer", "Jared", "Zach", "Chris", "Lyle", "Jeremy", "Harry", "Oscar", "Aaron", "Anthony", "Ian", "Emily", "Sarah", "Maria", "Alexia", "Sam", "Annabelle", "Franklin", "Michael", "George"]
last_names = ["Smith", "Williams", "Johnson", "Brown", "Jones", "Hadel", "Smyth", "Doe", "Simpson", "Gregors", "West", "Parker", "Wayne", "Jackson", "Porter", "Troy", "Orwell", "Clinton", "Bush", "Reagan", "Graham", "Brent", "Morgan"]

branches = [
    {"name": "Thames Capital", "city": "London", "county": "Greater London"},
    {"name": "Northern Hub", "city": "Manchester", "county": "Greater Manchester"},
    {"name": "Midlands Core", "city": "Birmingham", "county": "West Midlands"},
    {"name": "Caledonian Square", "city": "Edinburgh", "county": "City of Edinburgh"}
]

account_types = [
    {"name": "Standard Checking", "rate": 0.00, "fee": 0.00},
    {"name": "High-Yield Savings", "rate": 4.50, "fee": 5.00},
    {"name": "Student Checking", "rate": 0.01, "fee": 0.00}
]

categories = [
    {"name": "Groceries", "budget": "Essential"},
    {"name": "Coffee Shops", "budget": "Discretionary"},
    {"name": "Utilities", "budget": "Essential"},
    {"name": "Streaming Services", "budget": "Discretionary"},
    {"name": "Gas & Fuel", "budget": "Essential"}
]

num_transactions = 5000
num_unique_customers = 100

customer_pool = []
for i in range(num_unique_customers):
    fname = np.random.choice(first_names)
    lname = np.random.choice(last_names)
    branch = np.random.choice(branches)
    acc_type = np.random.choice(account_types)

    customer_pool.append({
        "customer_name": f"{fname} {lname}",
        "customer_email": f"{fname.lower()}.{lname.lower()}{i}@gmail.com",
        "branch_name": branch["name"],
        "branch_city": branch["city"],
        "branch_county": branch["county"],
        "account_type_name": acc_type["name"],
        "interest_rate": acc_type["rate"],
        "monthly_fee": acc_type["fee"],
        "initial_balance": round(np.random.uniform(500, 10000), 2)
    })

start_date = datetime(2026, 1, 1)
raw_rows = []

for txn_id in range(1000, 1000 + num_transactions):
    cust = np.random.choice(customer_pool)
    categ = np.random.choice(categories)

    amount = round(np.random.uniform(-150.00, 300.00), 2)
    if amount == 0: amount = -10.50

    random_days = np.random.randint(0, 90)
    txn_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d %H:%M:%S")

    raw_rows.append({
        "transaction_id": f"TXN{txn_id}",
        "customer_name": cust["customer_name"],
        "customer_email": cust["customer_email"],
        "branch_name": cust["branch_name"],
        "branch_city": cust["branch_city"],
        "branch_county": cust["branch_county"],
        "account_type_name": cust["account_type_name"],
        "account_interest_rate": cust["interest_rate"],
        "account_monthly_fee": cust["monthly_fee"],
        "account_opening_balance": cust["initial_balance"],
        "transaction_amount": amount,
        "transaction_timestamp": txn_date,
        "category_name": categ["name"],
        "budget_classification": categ["name"] if np.random.rand() > 0.1 else None, # There will be some occasional messy/null data throughout to clean
        "budget_type": categ["budget"]
    })

df = pd.DataFrame(raw_rows)
df.to_csv("raw_banking_data.csv", index=False)