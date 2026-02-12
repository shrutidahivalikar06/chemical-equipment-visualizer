import React from "react";

const ExportActions = ({ summary, fileName = "test.csv", fileSize = "2.4 KB", lastUpdated = "2 min ago" }) => {
  if (!summary) return null;

  const downloadSummaryJSON = () => {
    const blob = new Blob(
      [JSON.stringify(summary, null, 2)],
      { type: "application/json" }
    );
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "equipment_summary.json";
    link.click();
    URL.revokeObjectURL(url);
  };

  const downloadPDFReport = () => {
    window.open("http://127.0.0.1:8000/api/report/pdf/", "_blank");
  };

  return (
    <div className="card" style={{ padding: "24px" }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          paddingBottom: "20px",
          borderBottom: "1px solid #e9ecef",
          marginBottom: "20px",
        }}
      >
        <div
          style={{
            background: "#e7f5ff",
            borderRadius: "8px",
            padding: "8px 12px",
            display: "flex",
            alignItems: "center",
            gap: "8px",
          }}
        >
          <span style={{ fontSize: "14px", fontWeight: "500", color: "#1a73e8" }}>
            📄 {fileName}
          </span>
          <span style={{ fontSize: "12px", color: "#5f6b7a" }}>{fileSize}</span>
        </div>
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div>
          <h3
            style={{
              fontSize: "16px",
              fontWeight: "600",
              color: "#1a1e24",
              marginBottom: "4px",
            }}
          >
            Export & Actions
          </h3>
          <div style={{ display: "flex", gap: "16px", alignItems: "center" }}>
            <span style={{ fontSize: "13px", color: "#6c757d" }}>
              Last updated: {lastUpdated}
            </span>
            <span
              style={{
                fontSize: "13px",
                color: "#6c757d",
                display: "flex",
                alignItems: "center",
                gap: "4px",
              }}
            >
              <span style={{ color: "#40c057", fontSize: "16px" }}>●</span>
              File size: {fileSize}
            </span>
            <span
              style={{
                fontSize: "13px",
                color: "#40c057",
                display: "flex",
                alignItems: "center",
                gap: "4px",
              }}
            >
              <span>✓</span>
              Data validated
            </span>
          </div>
        </div>

        <div style={{ display: "flex", gap: "12px" }}>
          <button
            onClick={downloadPDFReport}
            style={{
              background: "#1a73e8",
              color: "#ffffff",
              padding: "10px 20px",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontWeight: "500",
              fontSize: "14px",
              display: "flex",
              alignItems: "center",
              gap: "8px",
            }}
            onMouseEnter={(e) => (e.target.style.background = "#1557b0")}
            onMouseLeave={(e) => (e.target.style.background = "#1a73e8")}
          >
            <span>📄</span>
            Download PDF Report
          </button>

          <button
            onClick={downloadSummaryJSON}
            style={{
              background: "#ffffff",
              color: "#1a73e8",
              border: "1px solid #1a73e8",
              padding: "10px 20px",
              borderRadius: "8px",
              cursor: "pointer",
              fontWeight: "500",
              fontSize: "14px",
              display: "flex",
              alignItems: "center",
              gap: "8px",
            }}
            onMouseEnter={(e) => {
              e.target.style.background = "#f0f7ff";
              e.target.style.borderColor = "#1557b0";
              e.target.style.color = "#1557b0";
            }}
            onMouseLeave={(e) => {
              e.target.style.background = "#ffffff";
              e.target.style.borderColor = "#1a73e8";
              e.target.style.color = "#1a73e8";
            }}
          >
            <span>📋</span>
            Download Summary (JSON)
          </button>
        </div>
      </div>

      <div
        style={{
          marginTop: "20px",
          paddingTop: "20px",
          borderTop: "1px solid #e9ecef",
          fontSize: "12px",
          color: "#adb5bd",
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <span>Chemical Equipment Parameter Visualizer - Interactive Prototype</span>
        <span>React.js + Tailwind CSS | Reference for PyQt5 Implementation</span>
      </div>
    </div>
  );
};

export default ExportActions;