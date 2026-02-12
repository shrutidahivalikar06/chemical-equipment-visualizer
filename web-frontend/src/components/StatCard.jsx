import React from "react";

const StatCard = ({ title, value, unit = "" }) => {
  const formattedValue = typeof value === "number"
    ? value.toLocaleString(undefined, {
        minimumFractionDigits: value % 1 === 0 ? 0 : 1,
        maximumFractionDigits: 1
      })
    : value;

  return (
    <div
      style={{
        background: "#ffffff",
        borderRadius: "12px",
        padding: "24px",
        boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
        border: "1px solid #e9ecef",
        transition: "transform 0.2s, box-shadow 0.2s",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.08)";
        e.currentTarget.style.transform = "translateY(-2px)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.boxShadow = "0 1px 3px rgba(0,0,0,0.1)";
        e.currentTarget.style.transform = "translateY(0)";
      }}
    >
      <p
        style={{
          fontSize: "13px",
          fontWeight: "600",
          color: "#6c757d",
          marginBottom: "8px",
          textTransform: "uppercase",
          letterSpacing: "0.5px",
        }}
      >
        {title}
      </p>

      <div style={{ display: "flex", alignItems: "baseline", gap: "8px" }}>
        <h2
          style={{
            fontSize: "32px",
            fontWeight: "700",
            color: "#1a1e24",
            margin: 0,
            lineHeight: 1.2,
          }}
        >
          {formattedValue}
        </h2>
        
        {unit && (
          <span
            style={{
              fontSize: "14px",
              fontWeight: "500",
              color: "#6c757d",
            }}
          >
            {unit}
          </span>
        )}
      </div>
    </div>
  );
};

export default StatCard;