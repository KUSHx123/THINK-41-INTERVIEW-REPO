from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow any frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_users_csv():
    filepath = os.path.join(os.path.dirname(__file__), "users.csv")
    df = pd.read_csv(filepath)
    return df

def load_orders_csv():
    filepath = os.path.join(os.path.dirname(__file__), "orders.csv")
    df = pd.read_csv(filepath)
    return df

@app.get("/customers")
def get_customers(skip: int = 0, limit: int = 10):
    users_df = load_users_csv()
    # Paginate
    users_page = users_df.iloc[skip : skip + limit]
    # Convert to dict list
    users_list = users_page.to_dict(orient="records")
    # Convert any numpy int64 to native int for JSON serialization
    for user in users_list:
        if isinstance(user.get("id"), (int, float)):
            user["id"] = int(user["id"])
    return users_list

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    users_df = load_users_csv()
    orders_df = load_orders_csv()

    user_row = users_df[users_df["id"] == customer_id]

    if user_row.empty:
        raise HTTPException(status_code=404, detail="Customer not found")

    user = user_row.iloc[0]

    # Count orders for this user id
    order_count = int(orders_df[orders_df["user_id"] == customer_id].shape[0])

    return {
        "id": int(user["id"]),
        "name": f"{user['first_name']} {user['last_name']}",
        "email": user["email"],
        "location": f"{user['city']}, {user['state']}",
        "created_at": user["created_at"],
        "total_orders": order_count
    }
