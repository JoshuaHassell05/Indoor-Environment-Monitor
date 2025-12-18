 /* 
    Frontend logic for the Indoor Environment Monitor Dashboard 
        - Polls GET /api/readings every 3 seconds
        - Updates the dashboard with the latest readings
        - Applies risk styling via CSS classes on the "pill" element
 */

// Helper to convert Celsius to Fahrenheit
function celsiusToFahrenheit(celsius) {
  return (celsius * 9 / 5) + 32;
}
// Helper to set text content of an element, with optional number formatting
 function setText(elementId, value, decimals = null){
    const el = document.getElementById(elementId);
    if (!el) return;
    if (value === undefined || value === null){
        el.textContent = "--";
        return;
    }
    if (typeof value === "number" && decimals !== null){
        el.textContent = value.toFixed(decimals);
        return;
    }
    el.textContent = String(value);
 }

 // Helper to set risk text and apply corresponding CSS class
 function setRisk(riskText){
    const riskEL = document.getElementById("risk");
    if (!riskEL) return;
    // Reset to base class to avoid stale styling when risk changes
    riskEL.className = "pill";
    riskEL.textContent = riskText ?? "--";
    if (riskText === "SAFE"){
        riskEL.classList.add("safe");
    }
    else if (riskText === "ELEVATED"){
        riskEL.classList.add("elevated");
    }
    else if (riskText === "WARNING"){
        riskEL.classList.add("warning");
    }
 }

// Helper to format ISO timestamp strings into a more readable format 
function formatTimestamp(isoString) {
  if (!isoString) return "--";
  const date = new Date(isoString + "Z");
  return date.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit"
  });
}

// Helper to fetch time series data for charts
async function fetchSeries(range) {
  const res = await fetch(`/api/readings?range=${encodeURIComponent(range)}`);
  return await res.json();
}

let tempChart = null;
let humChart = null;
let gasChart = null;

function createLineChart(canvasId, label, color) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;

  const ctx = canvas.getContext("2d");
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label: label,
        data: [],
        tension: 0.25,
        borderColor: color,
        backgroundColor: color
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false
    }
  });
}

// Chart.js chart instance
async function refreshChartRange() {
    const range = document.getElementById("rangeSelect")?.value ?? "day";
    const series = await fetchSeries(range);
    const labels = series.map(p => formatTimestamp(p.timestamp));
    const tempsF = series.map(p => celsiusToFahrenheit(p.temperature));
    const hums = series.map(p => p.humidity);
    const gas = series.map(p => p.gas_resistance);
    if (!historyChart) createHistoryChart();
    if (!historyChart) return;
    historyChart.data.labels = labels;
    historyChart.data.datasets[0].data = tempsF;
    historyChart.data.datasets[1].data = hums;
    historyChart.data.datasets[2].data = gas;
    historyChart.update();
}

 // Main function to refresh dashboard data
async function refreshDashboard() {
  try {
    const response = await fetch("/api/readings");
    const readings = await response.json();
    if (!readings.length) return;
    const latest = readings[readings.length - 1];
    setText("temp", celsiusToFahrenheit(latest.temperature), 1);
    setText("hum", latest.humidity, 1);
    setText("press", latest.pressure, 1);
    setText("gas", latest.gas_resistance, 0);
    setText("time", formatTimestamp(latest.timestamp));
    setRisk(latest.risk);
    }
    catch (error){
        // Log error but do not disrupt periodic refresh
        console.error("Dashboard refresh failed:", error);
    }
}

// Event listener for range selection change
document.getElementById("rangeSelect")?.addEventListener("change", () => {
  refreshChartRange();
});
// Initial load and periodic refresh every 3 seconds
refreshDashboard();
refreshChartRange();
setInterval(refreshDashboard, 3000);