import React from "react";

const DataPreviewTable = ({ data }) => {
  if (!data || data.length === 0) return null;

  return (
    <div
      style={{
        background: "#ffffff",
        borderRadius: "12px",
        padding: "20px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
        marginTop: "30px",
      }}
    >
      <h3
        style={{
          fontSize: "18px",
          fontWeight: "600",
          marginBottom: "15px",
          color: "#111827",
        }}
      >
        CSV Data Preview (First 10 Rows)
      </h3>

      <div
        style={{
          overflowX: "auto",
          maxHeight: "300px",
          overflowY: "auto",
        }}
      >
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            fontSize: "14px",
          }}
        >
          <thead>
            <tr style={{ background: "#f3f4f6" }}>
              {Object.keys(data[0]).map((key) => (
                <th
                  key={key}
                  style={{
                    padding: "10px",
                    borderBottom: "1px solid #e5e7eb",
                    textAlign: "left",
                    fontWeight: "600",
                    color: "#374151",
                  }}
                >
                  {key}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                {Object.values(row).map((value, i) => (
                  <td
                    key={i}
                    style={{
                      padding: "10px",
                      borderBottom: "1px solid #e5e7eb",
                      color: "#4b5563",
                    }}
                  >
                    {value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataPreviewTable;
