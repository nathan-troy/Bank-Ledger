import duckdb

conn = duckdb.connect("bank_ledger.db")

conn.execute("""
    INSERT OR IGNORE INTO Branches (branch_id, branch_name, city, county)
    SELECT
        ROW_NUMBER() OVER () as branch_id, -- Dynamic/unique ID generation (1, 2, 3, etc)
        branch_name,
        branch_city,
        branch_county
    FROM 'raw_banking_data.csv'
    GROUP BY branch_name, branch_city, branch_county; -- Removal of duplicate rows
""")

conn.execute("""
    INSERT OR IGNORE INTO Account_types (account_type_id, type_name, interest_rate, monthly_fee)
    SELECT
        ROW_NUMBER() OVER () AS account_type_id,
        account_type_name,
        account_interest_rate,
        account_monthly_fee
    FROM 'raw_banking_data.csv'
    GROUP BY account_type_name, account_interest_rate, account_monthly_fee;
""")

conn.execute("""
    INSERT OR IGNORE INTO Transaction_categories (category_id, category_name, budget_type)
    SELECT
        ROW_NUMBER() OVER () AS category_id,
        category_name,
        budget_type
    FROM 'raw_banking_data.csv'
    GROUP BY category_name, budget_type;
""")

conn.execute("""
    INSERT OR IGNORE INTO Customers (customer_id, branch_id, customer_name, customer_email)
    SELECT
        ROW_NUMBER() OVER () as customer_id,
        b.branch_id,
        csv.customer_name,
        csv.customer_email
    FROM 'raw_banking_data.csv' as csv
    JOIN Branches b
        ON csv.branch_name = b.branch_name
        AND csv.branch_city = b.city
    GROUP BY csv.customer_name, csv.customer_email, b.branch_id;
             
""")

conn.execute("""
    INSERT OR IGNORE INTO Accounts (account_id, customer_id, account_type_id, balance)
    SELECT
        ROW_NUMBER() OVER () as account_id,
        c.customer_id,
        t.account_type_id,
        csv.account_opening_balance
    FROM 'raw_banking_data.csv' as csv
    JOIN Customers c
        ON csv.customer_name = c.customer_name
        AND csv.customer_email = c.customer_email
    JOIN Account_types t
        ON csv.account_type_name = t.type_name
    GROUP BY c.customer_id, t.account_type_id, csv.account_opening_balance;
""")

conn.execute("""
    INSERT OR IGNORE INTO transactions (transaction_id, account_id, category_id, amount, transaction_date)
    SELECT
        csv.transaction_id,
        a.account_id,
        tc.category_id,
        csv.transaction_amount,
        csv.transaction_timestamp::TIMESTAMP
    FROM 'raw_banking_data.csv' as csv
    JOIN Customers c
        ON csv.customer_name = c.customer_name
        AND csv.customer_email = c.customer_email
    JOIN Accounts a
        ON c.customer_id = a.customer_id
    JOIN Transaction_categories tc
        ON csv.category_name = tc.category_name;
""")

print("\n Current Branches in Database")
print(conn.execute("SELECT * FROM Branches").fetchdf())

conn.close()