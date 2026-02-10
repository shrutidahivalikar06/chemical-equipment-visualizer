import React, { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  ScatterChart,
  Scatter
} from "recharts";

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [csvData, setCsvData] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("⚠️ Please select a CSV file before uploading");
      return;
    }

    setLoading(true);
    setMessage("Uploading and analyzing CSV...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Upload CSV
      const uploadRes = await fetch("http://127.0.0.1:8000/api/upload/", {
        method: "POST",
        body: formData,
      });
      const uploadData = await uploadRes.json();

      if (uploadRes.ok) {
        setMessage(uploadData.message || "File uploaded successfully");
        setCsvData(uploadData.data_preview || []);
      } else {
        setMessage(uploadData.error || "Upload failed");
        setCsvData([]);
      }

      // Fetch summary
      const summaryRes = await fetch("http://127.0.0.1:8000/api/summary/");
      const summaryData = await summaryRes.json();
      setSummary(summaryData);

    } catch (error) {
      console.error(error);
      setMessage("❌ Upload failed. Please check backend server.");
      setCsvData([]);
    } finally {
      setLoading(false);
    }
  };

  // Bar chart data
  const equipmentChartData = summary?.type_distribution
    ? Object.entries(summary.type_distribution).map(([type, count]) => ({
        type,
        count,
      }))
    : [];

  // Scatter chart data
  const scatterData = csvData.map((item) => ({
    pressure: Number(item.pressure || 0),
    temperature: Number(item.temperature || 0),
  }));

  const downloadSummary = () => {
    if (!summary) return;
    const blob = new Blob([JSON.stringify(summary, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "equipment_summary.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadPdfReport = () => {
    window.open("http://127.0.0.1:8000/api/report/pdf/", "_blank");
  };

  return (
    <div className="container" style={{ padding: "20px" }}>
      <h1>Chemical Equipment Parameter Visualizer</h1>

      <div className="card" style={{ padding: "10px", marginBottom: "20px" }}>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button
          onClick={handleUpload}
          disabled={loading}
          style={{ marginLeft: "10px" }}
        >
          {loading ? "Processing..." : "Upload CSV"}
        </button>
        {message && <p style={{ marginTop: "10px" }}>{message}</p>}
      </div>

      {summary && (
        <>
          <div className="stats" style={{ display: "flex", gap: "20px", marginBottom: "20px" }}>
            <div className="stat-card">
              <h4>Total Equipment</h4>
              <p>{summary.total_equipment}</p>
            </div>
            <div className="stat-card">
              <h4>Avg Purchase Year</h4>
              <p>{summary.avg_purchase_year}</p>
            </div>
          </div>

          <div className="card" style={{ marginBottom: "20px" }}>
            <button onClick={downloadSummary} style={{ marginRight: "10px" }}>
              Download JSON
            </button>
            <button onClick={downloadPdfReport}>Download PDF</button>
          </div>

          <div className="card" style={{ marginBottom: "20px" }}>
            <h3>Equipment Type Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={equipmentChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="type" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#4f46e5" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="card" style={{ marginBottom: "20px" }}>
            <h3>Pressure vs Temperature</h3>
            <ResponsiveContainer width="100%" height={300}>
              <ScatterChart>
                <CartesianGrid />
                <XAxis dataKey="pressure" name="Pressure" />
                <YAxis dataKey="temperature" name="Temperature" />
                <Tooltip />
                <Scatter data={scatterData} fill="#ef4444" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>

          {csvData.length > 0 && (
            <div className="card">
              <h3>CSV Preview (First 10 Rows)</h3>
              <table border="1" cellPadding="5" cellSpacing="0">
                <thead>
                  <tr>
                    {Object.keys(csvData[0]).map((key) => (
                      <th key={key}>{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {csvData.map((row, idx) => (
                    <tr key={idx}>
                      {Object.values(row).map((val, i) => (
                        <td key={i}>{val}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default App;
