import React from "react";

const DataPreviewTable = ({ csvData, totalRows = 247 }) => {
  if (!csvData || csvData.length === 0) return null;

  return (
    <div className="card" style={{ padding: "24px" }}>
      <div
        style={{
          borderBottom: "1px solid #e9ecef",
          paddingBottom: "16px",
          marginBottom: "20px",
        }}
      >
        <h3
          style={{
            fontSize: "16px",
            fontWeight: "600",
            color: "#1a1e24",
            marginBottom: "4px",
          }}
        >
          Data Preview
        </h3>
        <p
          style={{
            fontSize: "14px",
            color: "#6c757d",
            margin: 0,
          }}
        >
          Showing first 10 rows of {totalRows.toLocaleString()} total equipment records
        </p>
      </div>

      <div
        style={{
          overflowX: "auto",
          borderRadius: "8px",
        }}
      >
        <table style={{ marginTop: 0 }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left" }}>EQUIPMENT NAME</th>
              <th style={{ textAlign: "left" }}>TYPE</th>
              <th style={{ textAlign: "right" }}>FLOWRATE (L/MIN)</th>
              <th style={{ textAlign: "right" }}>PRESSURE (BAR)</th>
              <th style={{ textAlign: "right" }}>TEMPERATURE (°C)</th>
            </tr>
          </thead>
          <tbody>
            {csvData.slice(0, 10).map((row, index) => (
              <tr
                key={index}
                style={{
                  background: index % 2 === 0 ? "#ffffff" : "#fafbfc",
                  cursor: "pointer",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = "#f1f3f5";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = index % 2 === 0 ? "#ffffff" : "#fafbfc";
                }}
              >
                <td style={{ fontWeight: "500", color: "#1a1e24" }}>
                  {row["EQUIPMENT NAME"] || row.equipment_name || row.name || ""}
                </td>
                <td>
                  {row.TYPE || row.type || ""}
                </td>
                <td style={{ textAlign: "right", fontFamily: "monospace" }}>
                  {typeof row["FLOWRATE (L/MIN)"] === "number"
                    ? row["FLOWRATE (L/MIN)"].toFixed(1)
                    : row.FLOWRATE || row.flowrate || ""}
                </td>
                <td style={{ textAlign: "right", fontFamily: "monospace" }}>
                  {typeof row["PRESSURE (BAR)"] === "number"
                    ? row["PRESSURE (BAR)"].toFixed(1)
                    : row.PRESSURE || row.pressure || ""}
                </td>
                <td style={{ textAlign: "right", fontFamily: "monospace" }}>
                  {typeof row["TEMPERATURE (°C)"] === "number"
                    ? row["TEMPERATURE (°C)"].toFixed(1)
                    : row.TEMPERATURE || row.temperature || ""}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataPreviewTable;