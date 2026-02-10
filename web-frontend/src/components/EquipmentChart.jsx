import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

const EquipmentChart = ({ data }) => {
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
          marginBottom: "20px",
          color: "#111827",
        }}
      >
        Equipment Type Distribution
      </h3>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="type" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#4f46e5" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EquipmentChart;
