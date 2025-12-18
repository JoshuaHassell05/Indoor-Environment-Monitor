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

// Helper to format bucket labels for time series charts
function formatBucketLabel(t) {
  if (!t) return "--";
  // Convert "YYYY-MM-DD HH:MM" into an ISO UTC string "YYYY-MM-DDTHH:MMZ"
  const isoUtc = t.replace(" ", "T") + "Z";
  return new Date(isoUtc).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
}

// Helper to fetch time series data for charts
async function fetchSeries(range) {
  const res = await fetch(`/api/readings?range=${encodeURIComponent(range)}`);
  return await res.json();
}

let tempChart = null;
let humChart = null;
let gasChart = null;

// Create a line chart using Chart.js
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

// Refresh charts based on selected range
async function refreshChartRange() { 
    const range = document.getElementById("rangeSelect")?.value ?? "day";
    const series = await fetchSeries(range);
    const labels = series.map(p => formatBucketLabel(p.t));
    const tempsF = series.map(p => celsiusToFahrenheit(p.temp_avg));
    const hums = series.map(p => p.hum_avg);
    const gas = series.map(p => p.gas_avg);
    if (!tempChart) tempChart = createLineChart("tempChart", "Temperature (°F)", "rgb(255, 99, 132)");
    if (!humChart)  humChart  = createLineChart("humChart",  "Humidity (%)",     "rgb(54, 162, 235)");
    if (!gasChart)  gasChart  = createLineChart("gasChart",  "Gas Resistance (Ω)","rgb(75, 192, 192)");
    if (tempChart){
      tempChart.data.labels = labels;
      tempChart.data.datasets[0].data = tempsF;
      tempChart.update();
    }
    if (humChart){
      humChart.data.labels = labels;
      humChart.data.datasets[0].data = hums;
      humChart.update();
    }
    if (gasChart){
      gasChart.data.labels = labels;
      gasChart.data.datasets[0].data = gas;
      gasChart.update();
    }
  }

 // Main function to refresh dashboard data
async function refreshDashboard() {
  try {
    const response = await fetch("/api/latest");
    const latest = await response.json();
    if (!latest || !latest.timestamp) return;
    setText("press", latest.pressure, 1);
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
setInterval(refreshChartRange, 9000);