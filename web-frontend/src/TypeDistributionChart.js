import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function TypeDistributionChart({ data }) {
  if (!data) return null;

  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(data),
      },
    ],
  };

  return (
    <div style={{ width: "600px", marginTop: "30px" }}>
      <h3>Equipment Type Distribution</h3>
      <Bar data={chartData} />
    </div>
  );
}

export default TypeDistributionChart;
