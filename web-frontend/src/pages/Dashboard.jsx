import React, { useState } from "react";
import UploadCard from "../components/UploadCard";
import StatCard from "../components/StatCard";
import EquipmentChart from "../components/EquipmentChart";
import DataPreviewTable from "../components/DataPreviewTable";
import ExportActions from "../components/ExportActions";

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [csvData, setCsvData] = useState([]);
  const [message, setMessage] = useState("");

  const handleFileChange = (file) => {
    setFile(file);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Upload CSV
      const uploadRes = await fetch("http://127.0.0.1:8000/api/upload/", {
        method: "POST",
        body: formData,
      });
      const uploadData = await uploadRes.json();
      setMessage(uploadData.message || "File uploaded successfully");

      // Fetch summary
      const summaryRes = await fetch("http://127.0.0.1:8000/api/summary/");
      const summaryData = await summaryRes.json();
      setSummary(summaryData);

      // Fetch data preview
      const dataRes = await fetch("http://127.0.0.1:8000/api/data/");
      const dataJson = await dataRes.json();
      setCsvData(dataJson.slice(0, 10));
    } catch (err) {
      console.error(err);
      setMessage("Upload failed");
    }
  };

  return (
    <div
      style={{
        padding: "30px",
        background: "#f9fafb",
        minHeight: "100vh",
        fontFamily: "Inter, Arial, sans-serif",
      }}
    >
      <h1
        style={{
          fontSize: "26px",
          fontWeight: "700",
          marginBottom: "20px",
          color: "#111827",
        }}
      >
        Chemical Equipment Parameter Visualizer
      </h1>

      {/* Upload Section */}
      <UploadCard
        onFileSelect={handleFileChange}
        onUpload={handleUpload}
        message={message}
      />

      {/* Stats */}
      {summary && (
        <>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "20px",
              marginTop: "30px",
            }}
          >
            <StatCard title="Total Equipment" value={summary.total_equipment} />
            <StatCard title="Avg Flowrate" value={summary.avg_flowrate} />
            <StatCard title="Avg Pressure" value={summary.avg_pressure} />
            <StatCard title="Avg Temperature" value={summary.avg_temperature} />
          </div>

          {/* Charts */}
          <EquipmentChart summary={summary} csvData={csvData} />

          {/* Table */}
          <DataPreviewTable csvData={csvData} />

          {/* Export */}
          <ExportActions summary={summary} />
        </>
      )}
    </div>
  );
};

export default Dashboard;
