# THINK-41 Interview Project

This repository contains the code and resources developed for the THINK-41 interview assignment. The project implements a RESTful API backend using FastAPI to manage customers and orders data, supporting pagination, filtering, and detailed retrieval of customer and order information.

---

## Features

- REST API built with FastAPI  
- CORS enabled for frontend integration  
- Supports pagination for customer listing  
- Retrieve detailed customer information including order counts  
- Fetch all orders for a specific customer  
- Fetch details for a specific order  
- Data loaded from CSV files (`users.csv` and `orders.csv`)  
- Handles missing values gracefully  
- JSON responses properly encoded  

---

## Getting Started

### Prerequisites

- Python 3.10+ (recommended)  
- pip (Python package installer)  

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/KUSHx123/THINK-41-INTERVIEW-REPO.git
   cd THINK-41-INTERVIEW-REPO/api
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Linux/macOS
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the API Server

Run the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

By default, the API will be accessible at:  
`http://127.0.0.1:8000`

---

## API Endpoints

### GET `/customers`

Retrieve a paginated list of customers.

- Query Parameters:  
  - `skip` (int, default=0): Number of customers to skip (offset).  
  - `limit` (int, default=10): Maximum number of customers to return.

Example:  
`GET /customers?skip=0&limit=20`

---

### GET `/customers/{customer_id}`

Retrieve detailed information for a specific customer by their ID.

Example:  
`GET /customers/123`

---

### GET `/customers/{customer_id}/orders`

Retrieve all orders for a specific customer.

Example:  
`GET /customers/123/orders`

---

### GET `/orders/{order_id}`

Retrieve details for a specific order by its ID.

Example:  
`GET /orders/456`

---

## Project Structure

```
api/
├── main.py          # FastAPI application code
├── users.csv        # Customers data file
├── orders.csv       # Orders data file
├── requirements.txt # Python dependencies
└── README.md        # This file
```

---

## Notes

- The API reads data directly from CSV files on each request, which is suitable for demo or interview purposes but not optimized for production.  
- NaN values in the CSV are converted to `null` in JSON responses.  
- CORS is enabled for all origins to facilitate frontend integration.

---

## Contact

For any queries or feedback, please contact:  
**Kush Sinha**  
Email: [Your Email Address]  
GitHub: [https://github.com/KUSHx123](https://github.com/KUSHx123)

---

Thank you for reviewing this project!
