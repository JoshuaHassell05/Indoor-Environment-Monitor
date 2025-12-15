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
    riskEL.className = "pill";
    riskEL.textContent = riskText ?? "--";
    if (riskText === "Safe"){
        riskEL.classList.add("safe");
    }
    else if (riskText === "ELEVATED"){
        riskEL.classList.add("elevated");
    }
    else if (riskText === "WARNING"){
        riskEL.classList.add("warning");
    }
 }