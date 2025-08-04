from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import pandas as pd
import os

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load customers data
def load_users_csv():
    filepath = os.path.join(os.path.dirname(__file__), "users.csv")
    return pd.read_csv(filepath)

# Load orders data
def load_orders_csv():
    filepath = os.path.join(os.path.dirname(__file__), "orders.csv")
    return pd.read_csv(filepath)

# Get paginated list of customers
@app.get("/customers")
def get_customers(skip: int = 0, limit: int = 10):
    users_df = load_users_csv()
    users_page = users_df.iloc[skip: skip + limit]
    
    users_list = []
    for user in users_page.to_dict(orient="records"):
        users_list.append({
            "id": int(user["id"]),
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "city": user["city"],
            "state": user["state"],
            "created_at": user["created_at"]
        })

    return jsonable_encoder(users_list)

# Get customer details by ID
@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    users_df = load_users_csv()
    orders_df = load_orders_csv()

    user_row = users_df[users_df["id"] == customer_id]
    if user_row.empty:
        raise HTTPException(status_code=404, detail="Customer not found")

    user = user_row.iloc[0]
    order_count = int(orders_df[orders_df["user_id"] == customer_id].shape[0])

    return jsonable_encoder({
        "id": int(user["id"]),
        "name": f"{user['first_name']} {user['last_name']}",
        "email": user["email"],
        "location": f"{user['city']}, {user['state']}",
        "created_at": user["created_at"],
        "total_orders": order_count
    })

# Get all orders for a specific customer
@app.get("/customers/{customer_id}/orders")
def get_orders_for_customer(customer_id: int):
    users_df = load_users_csv()
    orders_df = load_orders_csv()

    if users_df[users_df["id"] == customer_id].empty:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer_orders = orders_df[orders_df["user_id"] == customer_id]
    orders_list = []

    for order in customer_orders.to_dict(orient="records"):
        orders_list.append({
            "order_id": int(order["order_id"]),
            "user_id": int(order["user_id"]),
            "order_date": order.get("order_date"),
            "order_amount": float(order.get("order_amount", 0)),
            "status": order.get("status")
        })

    return jsonable_encoder({
        "customer_id": customer_id,
        "orders": orders_list
    })

# Get details for a specific order
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    orders_df = load_orders_csv()
    users_df = load_users_csv()

    order_row = orders_df[orders_df["order_id"] == order_id]
    if order_row.empty:
        raise HTTPException(status_code=404, detail="Order not found")

    order = order_row.iloc[0]

    user_row = users_df[users_df["id"] == order["user_id"]]
    if user_row.empty:
        raise HTTPException(status_code=404, detail="Customer for this order not found")

    user = user_row.iloc[0]

    return jsonable_encoder({
        "order_id": int(order["order_id"]),
        "user_id": int(order["user_id"]),
        "customer_name": f"{user['first_name']} {user['last_name']}",
        "order_date": order.get("order_date"),
        "order_amount": float(order.get("order_amount", 0)),
        "status": order.get("status")
    })
