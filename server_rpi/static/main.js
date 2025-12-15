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
