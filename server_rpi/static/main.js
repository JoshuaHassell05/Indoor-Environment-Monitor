 /* 
    Frontend logic for the Indoor Environment Monitor Dashboard 
        - Polls GET /api/readings every 3 seconds
        - Updates the dashboard with the latest readings
        - Applies risk styling via CSS classes on the "pill" element
 */
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


 // Main function to refresh dashboard data
 async function refreshDashboard(){
    try {
        const response = await fetch("/api/readings");
        const readings = await response.json();
        if (!readings.length){
            return;
        }
        const latest = readings[readings.length - 1];
        setText("temp", latest.temperature, 1);
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
// Initial load and periodic refresh every 3 seconds
refreshDashboard();
setInterval(refreshDashboard, 3000);