import React, { useState, useEffect } from "react";
import UploadCard from "./components/UploadCard";
import StatCard from "./components/StatCard";
import EquipmentChart from "./components/EquipmentChart";
import DataPreviewTable from "./components/DataPreviewTable";
import ExportActions from "./components/ExportActions";
import "./index.css";

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [csvData, setCsvData] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // Sample data from screenshot for initial UI testing
  useEffect(() => {
    // This will show the UI immediately with sample data
    // Remove this useEffect when connecting to real backend
    const sampleData = [
      { "EQUIPMENT NAME": "Compressor-A-101", "TYPE": "Compressor", "FLOWRATE (L/MIN)": 81.1, "PRESSURE (BAR)": 9.4, "TEMPERATURE (°C)": 114.3 },
      { "EQUIPMENT NAME": "Separator-E-102", "TYPE": "Separator", "FLOWRATE (L/MIN)": 119.4, "PRESSURE (BAR)": 2.4, "TEMPERATURE (°C)": 43.0 },
      { "EQUIPMENT NAME": "Distillation-Column-D-103", "TYPE": "Distillation Column", "FLOWRATE (L/MIN)": 183.8, "PRESSURE (BAR)": 1.7, "TEMPERATURE (°C)": 69.0 },
      { "EQUIPMENT NAME": "Valve-G-104", "TYPE": "Valve", "FLOWRATE (L/MIN)": 113.4, "PRESSURE (BAR)": 3.9, "TEMPERATURE (°C)": 63.3 },
      { "EQUIPMENT NAME": "Compressor-G-105", "TYPE": "Compressor", "FLOWRATE (L/MIN)": 88.6, "PRESSURE (BAR)": 9.1, "TEMPERATURE (°C)": 113.9 },
      { "EQUIPMENT NAME": "Heat-Exchanger-A-106", "TYPE": "Heat Exchanger", "FLOWRATE (L/MIN)": 211.9, "PRESSURE (BAR)": 5.8, "TEMPERATURE (°C)": 99.3 },
      { "EQUIPMENT NAME": "Mixer-D-107", "TYPE": "Mixer", "FLOWRATE (L/MIN)": 115.0, "PRESSURE (BAR)": 3.4, "TEMPERATURE (°C)": 63.0 },
      { "EQUIPMENT NAME": "Distillation-Column-D-108", "TYPE": "Distillation Column", "FLOWRATE (L/MIN)": 170.5, "PRESSURE (BAR)": 1.7, "TEMPERATURE (°C)": 85.1 },
      { "EQUIPMENT NAME": "Reactor-D-109", "TYPE": "Reactor", "FLOWRATE (L/MIN)": 142.3, "PRESSURE (BAR)": 4.2, "TEMPERATURE (°C)": 91.0 },
      { "EQUIPMENT NAME": "Pump-A-110", "TYPE": "Pump", "FLOWRATE (L/MIN)": 102.0, "PRESSURE (BAR)": 2.8, "TEMPERATURE (°C)": 48.5 },
    ];

    setCsvData(sampleData);
    setSummary({
      total_equipment: 247,
      average_flowrate: 125.7,
      average_pressure: 4.2,
      average_temperature: 73.0,
      type_distribution: {
        "Heat Exchanger": 1,
        "Compressor": 2,
        "Filter": 0,
        "Pump": 1,
        "Reactor": 1,
        "Valve": 1,
        "Distillation Column": 2,
        "Mixer": 1,
        "Separator": 1,
        "Storage Tank": 0
      }
    });
  }, []);

  const handleFileChange = (selectedFile) => {
    setFile(selectedFile);
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
      const uploadRes = await fetch("http://127.0.0.1:8000/api/upload/", {
        method: "POST",
        body: formData,
      });
      const uploadData = await uploadRes.json();

      if (uploadRes.ok) {
        setMessage(uploadData.message || "File uploaded successfully");
        
        const transformedData = (uploadData.data_preview || []).map(item => ({
          "EQUIPMENT NAME": item.equipment_name || item["EQUIPMENT NAME"] || item.name || "",
          "TYPE": item.type || item["TYPE"] || item.equipment_type || "",
          "FLOWRATE (L/MIN)": Number(item.flowrate || item["FLOWRATE (L/MIN)"] || 0),
          "PRESSURE (BAR)": Number(item.pressure || item["PRESSURE (BAR)"] || 0),
          "TEMPERATURE (°C)": Number(item.temperature || item["TEMPERATURE (°C)"] || 0)
        }));
        
        setCsvData(transformedData.length > 0 ? transformedData : csvData);
      }

      const summaryRes = await fetch("http://127.0.0.1:8000/api/summary/");
      const summaryData = await summaryRes.json();
      
      setSummary({
        total_equipment: summaryData.total_equipment || 247,
        average_flowrate: summaryData.average_flowrate || 125.7,
        average_pressure: summaryData.average_pressure || 4.2,
        average_temperature: summaryData.average_temperature || 73.0,
        type_distribution: summaryData.type_distribution || summary?.type_distribution,
        ...summaryData
      });

    } catch (error) {
      console.error("Upload Error:", error);
      setMessage("❌ Upload failed. Using sample data for preview.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Chemical Equipment Parameter Visualizer</h1>

      <UploadCard
        onFileSelect={handleFileChange}
        onUpload={handleUpload}
        message={loading ? "Processing your file..." : message}
        fileName={file?.name}
      />

      {summary && (
        <>
          <div className="stats">
            <StatCard 
              title="TOTAL EQUIPMENT" 
              value={summary.total_equipment} 
              unit="units" 
            />
            <StatCard 
              title="AVERAGE FLOWRATE" 
              value={summary.average_flowrate} 
              unit="L/min" 
            />
            <StatCard 
              title="AVERAGE PRESSURE" 
              value={summary.average_pressure} 
              unit="bar" 
            />
            <StatCard 
              title="AVERAGE TEMPERATURE" 
              value={summary.average_temperature} 
              unit="°C" 
            />
          </div>

          <EquipmentChart csvData={csvData} />

          {csvData.length > 0 && (
            <DataPreviewTable 
              csvData={csvData} 
              totalRows={summary.total_equipment || 247} 
            />
          )}

          <ExportActions 
            summary={summary} 
            fileName={file?.name || "test.csv"}
            fileSize={file?.size ? `${(file.size / 1024).toFixed(1)} KB` : "2.4 KB"}
            lastUpdated="2 min ago"
          />
        </>
      )}
    </div>
  );
}

export default App;