import React from "react";

const StatCard = ({ title, value }) => {
  return (
    <div
      style={{
        background: "#ffffff",
        borderRadius: "12px",
        padding: "20px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
        minWidth: "220px",
      }}
    >
      <p
        style={{
          fontSize: "14px",
          color: "#6b7280",
          marginBottom: "8px",
        }}
      >
        {title}
      </p>

      <h2
        style={{
          fontSize: "28px",
          fontWeight: "bold",
          color: "#111827",
          margin: 0,
        }}
      >
        {value}
      </h2>
    </div>
  );
};

export default StatCard;
