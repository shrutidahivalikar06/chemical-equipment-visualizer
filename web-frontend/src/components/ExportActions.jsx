import React from "react";

const ExportActions = ({ summary }) => {
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
    <div
      style={{
        background: "#ffffff",
        borderRadius: "12px",
        padding: "20px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
        marginTop: "30px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        gap: "20px",
      }}
    >
      <h3
        style={{
          fontSize: "18px",
          fontWeight: "600",
          color: "#111827",
        }}
      >
        Export & Reports
      </h3>

      <div style={{ display: "flex", gap: "12px" }}>
        <button
          onClick={downloadSummaryJSON}
          style={{
            padding: "10px 16px",
            background: "#2563eb",
            color: "#ffffff",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: "500",
          }}
        >
          Download JSON
        </button>

        <button
          onClick={downloadPDFReport}
          style={{
            padding: "10px 16px",
            background: "#16a34a",
            color: "#ffffff",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: "500",
          }}
        >
          Download PDF
        </button>
      </div>
    </div>
  );
};

export default ExportActions;
