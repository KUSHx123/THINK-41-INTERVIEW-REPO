from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import os

app = FastAPI(title="Customer and Orders API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for response schemas
class Customer(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    city: Optional[str]
    state: Optional[str]
    created_at: Optional[str]

class CustomerDetail(BaseModel):
    id: int
    name: str
    email: Optional[str]
    location: Optional[str]
    created_at: Optional[str]
    total_orders: int

class Order(BaseModel):
    order_id: int
    user_id: int
    order_date: Optional[str]
    order_amount: Optional[float]
    status: Optional[str]

class CustomerOrders(BaseModel):
    customer_id: int
    orders: List[Order]

# Utility functions to load data from CSV
def load_users_csv() -> pd.DataFrame:
    filepath = os.path.join(os.path.dirname(__file__), "users.csv")
    df = pd.read_csv(filepath)
    # Replace NaN with None for JSON serialization
    return df.where(pd.notna(df), None)

def load_orders_csv() -> pd.DataFrame:
    filepath = os.path.join(os.path.dirname(__file__), "orders.csv")
    df = pd.read_csv(filepath)
    return df.where(pd.notna(df), None)

# API endpoints

@app.get("/customers", response_model=List[Customer])
def get_customers(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    users_df = load_users_csv()
    users_page = users_df.iloc[skip : skip + limit]

    customers = []
    for user in users_page.to_dict(orient="records"):
        customers.append(Customer(
            id=int(user["id"]),
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            email=user.get("email"),
            city=user.get("city"),
            state=user.get("state"),
            created_at=user.get("created_at")
        ))

    return customers

@app.get("/customers/{customer_id}", response_model=CustomerDetail)
def get_customer(customer_id: int):
    users_df = load_users_csv()
    orders_df = load_orders_csv()

    user_row = users_df[users_df["id"] == customer_id]
    if user_row.empty:
        raise HTTPException(status_code=404, detail="Customer not found")

    user = user_row.iloc[0]
    total_orders = int(orders_df[orders_df["user_id"] == customer_id].shape[0])

    return CustomerDetail(
        id=int(user["id"]),
        name=f"{user['first_name']} {user['last_name']}",
        email=user.get("email"),
        location=f"{user.get('city')}, {user.get('state')}" if user.get("city") and user.get("state") else None,
        created_at=user.get("created_at"),
        total_orders=total_orders
    )

@app.get("/customers/{customer_id}/orders", response_model=CustomerOrders)
def get_orders_for_customer(customer_id: int):
    users_df = load_users_csv()
    orders_df = load_orders_csv()

    if users_df[users_df["id"] == customer_id].empty:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer_orders_df = orders_df[orders_df["user_id"] == customer_id]
    orders_list = []

    for order in customer_orders_df.to_dict(orient="records"):
        order_amount = order.get("order_amount")
        if order_amount is not None:
            try:
                order_amount = float(order_amount)
            except ValueError:
                order_amount = None
        orders_list.append(Order(
            order_id=int(order["order_id"]),
            user_id=int(order["user_id"]),
            order_date=order.get("order_date"),
            order_amount=order_amount,
            status=order.get("status")
        ))

    return CustomerOrders(
        customer_id=customer_id,
        orders=orders_list
    )

@app.get("/orders/{order_id}", response_model=Order)
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

    order_amount = order.get("order_amount")
    if order_amount is not None:
        try:
            order_amount = float(order_amount)
        except ValueError:
            order_amount = None

    return Order(
        order_id=int(order["order_id"]),
        user_id=int(order["user_id"]),
        order_date=order.get("order_date"),
        order_amount=order_amount,
        status=order.get("status")
    )
