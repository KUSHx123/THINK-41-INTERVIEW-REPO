import pandas as pd
import sqlite3

# Load CSV files into DataFrames
users_df = pd.read_csv('users.csv')
orders_df = pd.read_csv('orders.csv')

# Connect to SQLite DB (creates file if not exists)
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    created_at TEXT
)
''')

# Create orders table
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    order_date TEXT,
    order_amount REAL,
    currency TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# Load data into tables (replace if table already exists)
users_df.to_sql('users', conn, if_exists='replace', index=False)
orders_df.to_sql('orders', conn, if_exists='replace', index=False)

# ✅ Verify the data was loaded
print("✅ Sample Users:")
print(pd.read_sql_query("SELECT * FROM users LIMIT 5", conn))

print("\n✅ Sample Orders:")
print(pd.read_sql_query("SELECT * FROM orders LIMIT 5", conn))

# ✅ Row counts
user_count = pd.read_sql_query("SELECT COUNT(*) as total FROM users", conn).iloc[0, 0]
order_count = pd.read_sql_query("SELECT COUNT(*) as total FROM orders", conn).iloc[0, 0]

print(f"\n✅ Total Users: {user_count}")
print(f"✅ Total Orders: {order_count}")

# Close the connection
conn.close()
