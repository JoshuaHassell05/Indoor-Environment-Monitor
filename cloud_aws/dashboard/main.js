 /* 
    Frontend logic for the Indoor Environment Monitor Dashboard 
        - Polls GET /api/readings every 3 seconds
        - Updates the dashboard with the latest readings
        - Applies risk styling via CSS classes on the "pill" element
 */

const API_BASE = "https://yc1b20bw9d.execute-api.us-east-1.amazonaws.com/Prod";
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
function setRisk(riskText, reasons = []) {
  const riskEL = document.getElementById("risk");
  if (!riskEL) return;

  riskEL.className = "pill";
  riskEL.textContent = riskText ?? "--";

  if (riskText === "SAFE") {
    riskEL.classList.add("safe");
  } else if (riskText === "ELEVATED") {
    riskEL.classList.add("elevated");
  } else if (riskText === "WARNING") {
    riskEL.classList.add("warning");
  }

  // Tooltip text
  if (Array.isArray(reasons) && reasons.length > 0) {
    riskEL.dataset.tooltip = reasons.join("\n");
  } else {
    riskEL.setAttribute("data-tooltip", "All sensor values within safe ranges");
  }
}

// Helper to format ISO timestamp strings into a more readable format 
function formatTimestamp(isoString) {
  if (!isoString) return "--";
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return "--";
  return date.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit"
  });
}

// Helper to format bucket labels for time series charts
function formatBucketLabel(t, range) {
  if (!t) return "--";

  // Convert "YYYY-MM-DD HH:MM" → ISO UTC
  const isoUtc = t.replace(" ", "T") + "Z";
  const d = new Date(isoUtc);

  if (range === "month") {
    return d.toLocaleDateString(undefined, {
      month: "short",
      day: "numeric"
    });
  }

  if (range === "week") {
    return d.toLocaleString(undefined, {
      weekday: "short",
      hour: "numeric"
    });
  }

  return d.toLocaleTimeString(undefined, {
    hour: "numeric",
    minute: "2-digit"
  });
}

// Helper to fetch time series data for charts
async function fetchSeries(range) {
  const res = await fetch(`${API_BASE}/api/readings?range=${encodeURIComponent(range)}`);
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

let tempGauge = null;  
let humGauge  = null;
let gasGauge  = null;

// Color functions for gauges based on value thresholds
function tempColorForF(tempF){
  if (tempF >= 86) return "#ff4d4d";      
  if (tempF >= 78) return "#ffd166";      
  if (tempF <= 60) return "#4dabf7";      
  return "#2ecc71";                        
}
function humColor(h){
  if (h >= 70 || h <= 25) return "#ff4d4d";   
  if (h >= 60 || h <= 30) return "#ffd166";   
  return "#2ecc71";                           
}
function gasColor(ohms){
  if (ohms <= 20000) return "#ff4d4d"; 
  if (ohms <= 30000) return "#ffd166"; 
  return "#2ecc71";                   
}

// Create a gauge chart using ApexCharts
function createGauge({
  elId,
  min,
  max,
  seed,
  unitFormatter,
  colorFn,
  toSeries = (raw) => raw,
}) { // toSeries converts raw value to 0..100 scale for gauge 
  const el = document.getElementById(elId);
  if (!el || typeof ApexCharts === "undefined") return null;

  let hasValue = false;
  let lastRaw = seed; 
  const options = { // see https://apexcharts.com/docs/chart-types/radialbar/
    series: [toSeries(seed)],
    chart: {
      height: 220,
      type: "radialBar",
      toolbar: { show: false }
    },
    plotOptions: { 
      radialBar: {
        startAngle: -135,
        endAngle: 135,
        hollow: { size: "70%" },
        track: { background: "#fff", strokeWidth: "95%" }, 
        dataLabels: {
          name: { show: false },
          value: {
            offsetY: 6,
            fontSize: "32px",
            formatter: () => hasValue ? unitFormatter(lastRaw) : "--" 
          }
        }
      }
    },
    yaxis: { min, max }, 
    fill: { type: "solid", colors: ["#bbb"] },
    stroke: { lineCap: "round" }
  };
  // Clear any existing content before rendering
  el.innerHTML = "";
  const chart = new ApexCharts(el, options);
  chart.render();

  return {
    // Update the gauge with a new raw value
    setValue(rawValue) {
      hasValue = true;
      lastRaw = rawValue;

      const seriesVal = toSeries(rawValue);
      const clamped = Math.min(max, Math.max(min, seriesVal));

      chart.updateSeries([clamped]);
      chart.updateOptions({ fill: { colors: [colorFn(rawValue)] } }, false, false);
    }
  };
}

// Refresh charts based on selected range
async function refreshChartRange() { 
    const range = document.getElementById("rangeSelect")?.value ?? "day";
    const series = await fetchSeries(range);
    const clean = series.filter(p => p.temp_avg != null || p.hum_avg != null || p.gas_avg != null);
    const labels = clean.map(p => formatBucketLabel(p.t, range));
    const tempsF = clean.map(p => (p.temp_avg == null ? null : celsiusToFahrenheit(p.temp_avg)));
    const hums   = clean.map(p => p.hum_avg);
    const gas    = clean.map(p => p.gas_avg);

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
    const res = await fetch(`${API_BASE}/api/latest`);
    const latest = await res.json();
    if (!latest?.timestamp) return;

    tempGauge?.setValue(
      celsiusToFahrenheit(latest.temperature)
    );

    humGauge?.setValue(latest.humidity);
    gasGauge?.setValue(latest.gas_resistance);

    setText("press", latest.pressure, 1);
    setText("time", formatTimestamp(latest.timestamp));
    setRisk(latest.risk, latest.risk_reasons);
  } catch (error) {
    console.error("Dashboard refresh failed:", error);
  }
}


// Event listener for range selection change
document.getElementById("rangeSelect")?.addEventListener("change", () => {
  refreshChartRange();
});

// Initialize gauges and start periodic refresh on DOM load
document.addEventListener("DOMContentLoaded", () => {
    tempGauge = createGauge({
        elId: "tempGauge",
        min: 40,
        max: 100,
        seed: 40,
        unitFormatter: v => `${Math.round(v)}°F`,
        colorFn: tempColorForF
    });

    humGauge = createGauge({
        elId: "humGauge",
        min: 0,
        max: 100,
        seed: 0,
        unitFormatter: v => `${Math.round(v)}%`,
        colorFn: humColor
    });

    const GAS_FULL_SCALE = 100000; 

    gasGauge = createGauge({
        elId: "gasGauge",
        min: 0,
        max: 100,                 
        seed: 0,
        unitFormatter: v => `${Math.round(v)}Ω`, 
        colorFn: gasColor,                    
        toSeries: (ohms) => (ohms / GAS_FULL_SCALE) * 100  
    });

    refreshDashboard();
    refreshChartRange();
    setInterval(refreshDashboard, 15000);   
    setInterval(refreshChartRange, 60000);  

});