"""Reads the two Excel files and loads them into the SQLite database sales.db."""
import sqlite3
import pandas as pd

# 1. Read Excel
customers = pd.read_excel("data/customers.xlsx")
orders = pd.read_excel("data/orders.xlsx")

# 2. Clean: lowercase column names so they match the SQL tables
customers.columns = customers.columns.str.lower()
orders.columns = orders.columns.str.lower()

# 3. Dates as text 'YYYY-MM-DD' (SQLite stores dates as text; this format filters correctly)
customers["join_date"] = customers["join_date"].dt.strftime("%Y-%m-%d")
orders["order_date"] = orders["order_date"].dt.strftime("%Y-%m-%d")

# 4. Check the data before loading
assert customers["customer_id"].is_unique, "Duplicate customer IDs found"
assert orders["order_id"].is_unique, "Duplicate order IDs found"
assert orders["customer_id"].isin(customers["customer_id"]).all(), "Order with unknown customer"

# 5. Create tables, then load: customers first (parent), orders second (child)
con = sqlite3.connect("sales.db")
con.executescript(open("schema.sql").read())
customers.to_sql("customers", con, if_exists="append", index=False)
orders.to_sql("orders", con, if_exists="append", index=False)
con.commit()

print("customers loaded:", con.execute("SELECT COUNT(*) FROM customers").fetchone()[0])
print("orders loaded   :", con.execute("SELECT COUNT(*) FROM orders").fetchone()[0])
con.close()
