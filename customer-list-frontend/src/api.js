const BASE_URL = "http://localhost:8000"; // Replace with your backend URL

export async function fetchCustomers() {
  const response = await fetch(`${BASE_URL}/customers`);
  if (!response.ok) throw new Error("Failed to fetch customers");
  return response.json();
}

export async function fetchCustomerOrders(customerId) {
  const response = await fetch(`${BASE_URL}/customers/${customerId}/orders`);
  if (!response.ok) throw new Error("Failed to fetch orders");
  return response.json();
}
