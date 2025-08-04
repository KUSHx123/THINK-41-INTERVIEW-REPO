import React, { useState, useEffect } from "react";

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch customers from API
  const fetchCustomers = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("http://localhost:8000/customers");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setCustomers(data);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  // Filter customers by name or email based on search term
  const filteredCustomers = customers.filter(
    (cust) =>
      (cust.name && cust.name.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (cust.email && cust.email.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div style={{ maxWidth: 900, margin: "auto", padding: 20 }}>
      <h1>Customer List</h1>

      <input
        type="text"
        placeholder="Search by name or email..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{ padding: 8, width: "100%", marginBottom: 20, fontSize: 16 }}
      />

      {loading && <p>Loading customers...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {!loading && !error && (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
          }}
        >
          <thead>
            <tr>
              <th style={thStyle}>Name</th>
              <th style={thStyle}>Email</th>
              <th style={thStyle}>Total Orders</th>
            </tr>
          </thead>
          <tbody>
            {filteredCustomers.length === 0 && (
              <tr>
                <td colSpan="3" style={{ textAlign: "center", padding: 20 }}>
                  No customers found.
                </td>
              </tr>
            )}
            {filteredCustomers.map((cust) => (
              <tr key={cust.id}>
                <td style={tdStyle}>{cust.name}</td>
                <td style={tdStyle}>{cust.email}</td>
                <td style={tdStyle}>{cust.total_orders}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

const thStyle = {
  borderBottom: "2px solid #ddd",
  textAlign: "left",
  padding: "10px",
  backgroundColor: "#f2f2f2",
};

const tdStyle = {
  borderBottom: "1px solid #ddd",
  padding: "10px",
};

export default CustomerList;
