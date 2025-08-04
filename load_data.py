import pandas as pd
import sqlite3

# Load CSV files
users_df = pd.read_csv('users.csv')
orders_df = pd.read_csv('orders.csv')

# Connect to SQLite DB (creates ecommerce.db if not exists)
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
    created_at DATE
)''')

# Create orders table
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    order_date DATE,
    order_amount REAL,
    currency TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)''')

# Load data into tables
users_df.to_sql('users', conn, if_exists='replace', index=False)
orders_df.to_sql('orders', conn, if_exists='replace', index=False)

# Verify load
print("Sample Users:")
print(pd.read_sql_query("SELECT * FROM users LIMIT 5", conn))

print("\nSample Orders:")
print(pd.read_sql_query("SELECT * FROM orders LIMIT 5", conn))

# Close connection
conn.close()
