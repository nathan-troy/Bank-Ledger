import duckdb
import sys

conn = duckdb.connect("bank_ledger.db")

errors_found = 0

def run_test(test_name, query, expected_count):
    global errors_found
    try:
        result = conn.execute(query).fetchone()[0]
        if result == expected_count:
            print(f"Passed: {test_name}")
        else:
            print(f"Failed: {test_name} (Found {result} unexpected records, expected {expected_count})")
            errors_found += 1
    except Exception as e:
        print(f"Critical Error: {test_name}: {str(e)}", )
        errors_found += 1

# Data Quality Testing
orphan_txns_query = """
    SELECT COUNT(*)
    FROM transactions t
    LEFT JOIN Accounts a ON t.account_id = a.account_id
    WHERE a.account_id IS NULL;
"""

run_test("Orphan Transactions Check", orphan_txns_query, expected_count=0)

invalid_cat_query = """
    SELECT COUNT(*)
    FROM transactions
    WHERE category_id IS NULL OR category_id NOT IN (SELECT category_id FROM Transaction_categories);
"""

run_test("Transactions Category Referential Integrity Check", invalid_cat_query, expected_count=0)

volume_query = "SELECT COUNT(*) FROM transactions;"
run_test("Historical Transaction Volume Verification", volume_query, expected_count=5000)

negative_balance_query = "SELECT COUNT(*) FROM Accounts WHERE balance < 0;"
run_test("Negative Account Balance Safeguard Check", negative_balance_query, expected_count=0)

duplicate_email_query = """
    SELECT COUNT(*) FROM (
        SELECT customer_email FROM Customers GROUP BY customer_email HAVING COUNT(*) > 1
        ) as sub
"""
run_test("Customer Email Uniqueness Check", duplicate_email_query, expected_count=0)

# Exit Control
if errors_found == 0:
    conn.close()
    sys.exit(0) #Success
else:
    conn.close()
    sys.exit(1) # Triggers failure flags in automated runs