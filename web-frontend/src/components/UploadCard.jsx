import React from "react";

const UploadCard = ({ onFileSelect, onUpload, message, fileName = null }) => {
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    onFileSelect(selectedFile);
  };

  return (
    <div className="card" style={{ padding: "28px" }}>
      <h2
        style={{
          fontSize: "20px",
          fontWeight: "600",
          color: "#1a1e24",
          marginBottom: "8px",
        }}
      >
        Chemical Equipment Parameter Visualizer
      </h2>

      <p
        style={{
          color: "#6c757d",
          fontSize: "15px",
          marginBottom: "24px",
          lineHeight: "1.5",
        }}
      >
        Upload Chemical Equipment Data
        <br />
        <span style={{ fontSize: "14px" }}>
          Upload a CSV file containing equipment parameters to generate analytical summaries and visualizations
        </span>
      </p>

      <div
        style={{
          background: "#f8f9fa",
          borderRadius: "8px",
          padding: "16px",
          marginBottom: "24px",
          border: "1px solid #e9ecef",
        }}
      >
        <ul
          style={{
            listStyle: "none",
            padding: 0,
            margin: 0,
            fontSize: "13px",
            color: "#495057",
          }}
        >
          <li style={{ marginBottom: "8px", display: "flex", alignItems: "center", gap: "8px" }}>
            <span style={{ color: "#40c057" }}>✓</span> CSV format only
          </li>
          <li style={{ marginBottom: "8px", display: "flex", alignItems: "center", gap: "8px" }}>
            <span style={{ color: "#40c057" }}>✓</span> Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature
          </li>
          <li style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <span style={{ color: "#40c057" }}>✓</span> Maximum file size: 10MB
          </li>
        </ul>
      </div>

      <div
        style={{
          border: "2px dashed #ced4da",
          borderRadius: "12px",
          padding: "32px",
          textAlign: "center",
          background: "#fafbfc",
          cursor: "pointer",
          transition: "border-color 0.2s, background 0.2s",
          marginBottom: "16px",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.borderColor = "#1a73e8";
          e.currentTarget.style.background = "#f0f7ff";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.borderColor = "#ced4da";
          e.currentTarget.style.background = "#fafbfc";
        }}
        onClick={() => document.getElementById("fileInput").click()}
      >
        <input
          id="fileInput"
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          style={{ display: "none" }}
        />
        <div style={{ fontSize: "32px", marginBottom: "12px" }}>📄</div>
        <p
          style={{
            fontSize: "16px",
            fontWeight: "600",
            color: "#1a1e24",
            marginBottom: "4px",
          }}
        >
          Choose CSV File
        </p>
        <p style={{ fontSize: "14px", color: "#6c757d" }}>
          or drag and drop your file here
        </p>
      </div>

      {fileName && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            padding: "12px",
            background: "#f8f9fa",
            borderRadius: "8px",
            marginBottom: "16px",
          }}
        >
          <span style={{ fontSize: "20px" }}>📄</span>
          <div style={{ flex: 1 }}>
            <span style={{ fontSize: "14px", fontWeight: "500", color: "#1a1e24" }}>
              {fileName}
            </span>
          </div>
          <span style={{ fontSize: "12px", color: "#6c757d" }}>Selected</span>
        </div>
      )}

      <button
        onClick={onUpload}
        style={{
          background: "#1a73e8",
          color: "#ffffff",
          padding: "12px 24px",
          borderRadius: "8px",
          border: "none",
          cursor: "pointer",
          fontWeight: "500",
          fontSize: "15px",
          width: "100%",
          transition: "background 0.2s",
        }}
        onMouseEnter={(e) => (e.target.style.background = "#1557b0")}
        onMouseLeave={(e) => (e.target.style.background = "#1a73e8")}
      >
        Upload CSV
      </button>

      {message && (
        <p
          style={{
            marginTop: "16px",
            padding: "12px",
            background: message.includes("❌") ? "#ffe3e3" : "#d3f9d8",
            color: message.includes("❌") ? "#c92a2a" : "#2b8e3c",
            borderRadius: "8px",
            fontSize: "14px",
            display: "flex",
            alignItems: "center",
            gap: "8px",
          }}
        >
          <span>{message.includes("❌") ? "⚠️" : "✓"}</span>
          {message}
        </p>
      )}
    </div>
  );
};

export default UploadCard;