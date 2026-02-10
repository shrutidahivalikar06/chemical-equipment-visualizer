import React, { useState } from "react";

const UploadCSV = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  // The upload function
  const uploadCSV = async () => {
    if (!file) {
      setMessage("Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/upload/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("Upload Response:", data);
      setMessage(data.message || data.error);
    } catch (error) {
      console.error("Upload Error:", error);
      setMessage("Upload failed. Check console for details.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Upload Equipment CSV</h2>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={uploadCSV} style={{ marginLeft: "10px" }}>
        Upload
      </button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default UploadCSV;
