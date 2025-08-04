import React, { useEffect, useState } from "react";
import { fetchCustomers } from "./api";
import CustomerCard from "./components/CustomerCard";
import SearchBar from "./components/SearchBar";
import "./App.css";

function App() {
  const [customers, setCustomers] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadCustomers() {
      try {
        const data = await fetchCustomers();
        const withOrderCount = data.map((cust) => ({
          ...cust,
          orderCount: cust.orders ? cust.orders.length : 0,
        }));
        setCustomers(withOrderCount);
        setFiltered(withOrderCount);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    }
    loadCustomers();
  }, []);

  useEffect(() => {
    const filteredData = customers.filter((cust) =>
      `${cust.name} ${cust.email}`.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFiltered(filteredData);
  }, [searchTerm, customers]);

  if (loading) return <p>Loading customers...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="app-container">
      <h1>Customer List</h1>
      <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
      <div className="customer-grid">
        {filtered.map((cust) => (
          <CustomerCard key={cust.id} customer={cust} />
        ))}
      </div>
    </div>
  );
}

export default App;
