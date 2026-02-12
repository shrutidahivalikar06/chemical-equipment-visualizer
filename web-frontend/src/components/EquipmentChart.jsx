import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

const EquipmentChart = ({ csvData }) => {
  const allEquipmentTypes = [
    "Heat Exchanger",
    "Compressor",
    "Filter",
    "Pump",
    "Reactor",
    "Valve",
    "Distillation Column",
    "Mixer",
    "Separator",
    "Storage Tank",
  ];

  const calculateCounts = () => {
    if (!csvData || csvData.length === 0) {
      return allEquipmentTypes.map((name) => ({ name, count: 0 }));
    }

    const counts = {};
    allEquipmentTypes.forEach((type) => {
      counts[type] = 0;
    });

    csvData.forEach((item) => {
      const type = item.TYPE || item.type;
      if (type && counts.hasOwnProperty(type)) {
        counts[type] += 1;
      }
    });

    return allEquipmentTypes.map((name) => ({
      name,
      count: counts[name],
    }));
  };

  const chartData = calculateCounts();
  
  const COLORS = [
    "#4dabf7", "#40c057", "#fab005", "#ff8787", 
    "#7950f2", "#ff922b", "#15aabf", "#e64980", 
    "#20c997", "#adb5bd"
  ];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div
          style={{
            background: "white",
            padding: "8px 12px",
            border: "1px solid #e9ecef",
            borderRadius: "6px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
          }}
        >
          <p style={{ margin: 0, fontSize: "14px", color: "#1a1e24" }}>
            <strong>{payload[0].payload.name}</strong>
          </p>
          <p style={{ margin: "4px 0 0", fontSize: "13px", color: "#495057" }}>
            Count: <strong>{payload[0].value}</strong>
          </p>
        </div>
      );
    }
    return null;
  };

  const valveData = chartData.find((d) => d.name === "Valve");

  return (
    <div className="card" style={{ padding: "24px" }}>
      <div
        style={{
          borderBottom: "1px solid #e9ecef",
          paddingBottom: "16px",
          marginBottom: "24px",
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
          Equipment Type Distribution
        </h3>
      </div>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "16px",
          marginBottom: "24px",
          paddingBottom: "16px",
          borderBottom: "1px solid #e9ecef",
        }}
      >
        {chartData.map((item, index) => (
          <div
            key={item.name}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
            }}
          >
            <div
              style={{
                width: "12px",
                height: "12px",
                borderRadius: "3px",
                background: COLORS[index % COLORS.length],
              }}
            />
            <span style={{ fontSize: "14px", color: "#495057" }}>
              {item.name}
            </span>
          </div>
        ))}
      </div>

      {valveData && (
        <div
          style={{
            fontSize: "14px",
            color: "#495057",
            marginBottom: "16px",
            padding: "12px",
            background: "#f8f9fa",
            borderRadius: "6px",
            display: "inline-block",
          }}
        >
          <strong style={{ color: "#1a1e24" }}>Valve count:</strong> {valveData.count}
        </div>
      )}

      <div style={{ width: "100%", height: "350px" }}>
        <ResponsiveContainer>
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 120, bottom: 5 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              horizontal={true}
              vertical={false}
              stroke="#e9ecef"
            />
            <XAxis
              type="number"
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: "#6c757d" }}
              domain={[0, 32]}
              ticks={[0, 8, 16, 24, 32]}
            />
            <YAxis
              type="category"
              dataKey="name"
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 13, fill: "#495057", fontWeight: 500 }}
              width={110}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar
              dataKey="count"
              radius={[0, 4, 4, 0]}
              barSize={24}
            >
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default EquipmentChart;