import React from "react";

const UploadCard = ({ onFileChange, onUpload, message }) => {
  return (
    <div
      style={{
        background: "#ffffff",
        borderRadius: "12px",
        padding: "24px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
        maxWidth: "500px",
        marginBottom: "30px",
      }}
    >
      <h2 style={{ marginBottom: "8px" }}>
        Chemical Equipment Parameter Visualizer
      </h2>

      <p style={{ color: "#6b7280", marginBottom: "16px" }}>
        Upload a CSV file to analyze chemical equipment parameters
      </p>

      <input
        type="file"
        accept=".csv"
        onChange={onFileChange}
        style={{
          display: "block",
          marginBottom: "16px",
        }}
      />

      <button
        onClick={onUpload}
        style={{
          backgroundColor: "#4f46e5",
          color: "#ffffff",
          padding: "10px 18px",
          borderRadius: "8px",
          border: "none",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        Upload CSV
      </button>

      {message && (
        <p style={{ marginTop: "12px", color: "#065f46" }}>
          {message}
        </p>
      )}
    </div>
  );
};

export default UploadCard;
