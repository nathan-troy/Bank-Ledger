import duckdb

conn = duckdb.connect("bank_ledger.db")

conn.execute("""
    CREATE TABLE IF NOT EXISTS Branches (
            branch_id INTEGER PRIMARY KEY,
            branch_name VARCHAR NOT NULl,
            city VARCHAR NOT NULL,
            county VARCHAR NOT NULL
        );
             
    CREATE TABLE IF NOT EXISTS Account_types (
            account_type_id INTEGER PRIMARY KEY,
            type_name VARCHAR NOT NULL,
            interest_rate DECIMAL(5, 2) NOT NULL,
            monthly_fee DECIMAL(5, 2) NOT NULL
        );
             
    CREATE TABLE IF NOT EXISTS Transaction_categories (
            category_id INTEGER PRIMARY KEY,
            category_name VARCHAR NOT NULL,
            budget_type VARCHAR NOT NULL
        );
             
    CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY,
            branch_id INTEGER REFERENCES Branches(branch_id),
            customer_name VARCHAR NOT NULL,
            customer_email VARCHAR NOT NULL
        );
             
    CREATE TABLE IF NOT EXISTS Accounts (
            account_id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES Customers(customer_id),
            account_type_id INTEGER REFERENCES Account_types(account_type_id),
            balance DECIMAL(15,2) NOT NULL
        );
             
    CREATE TABLE IF NOT EXISTS transactions (
            transaction_id VARCHAR PRIMARY KEY,
            account_id INTEGER REFERENCES Accounts(account_id),
            category_id INTEGER REFERENCES Transaction_categories(category_id),
            amount DECIMAL(15,2) NOT NULL,
            transaction_date TIMESTAMP NOT NULL
        );
 """)

conn.close()