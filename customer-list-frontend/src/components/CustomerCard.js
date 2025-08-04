import React from "react";

const CustomerCard = ({ customer }) => {
  return (
    <div className="customer-card">
      <h3>{customer.name}</h3>
      <p>Email: {customer.email}</p>
      <p>Order Count: {customer.orderCount}</p>
    </div>
  );
};

export default CustomerCard;
