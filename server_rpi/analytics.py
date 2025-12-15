def evaluate_risk(reading: dict) -> dict:
    temp_c = reading.get('temperature')
    humidity = reading.get('humidity')
    gas_ohms = reading.get('gas_resistance')
    if temp_c is None or humidity is None or gas_ohms is None:
        return {'risk': "Elevated", 'risk_reason': ["Missing one or more required sensor values"]
        }
    reasons = []
    if humidity >= 70:
        reasons.append("High Humidity (>= 70%)")
    elif humidity <= 25:
        reasons.append("Very Low Humidity (<= 25%)")
    if temp_c >= 28:
        reasons.append("High Temperature (>= 28°C)")
    elif temp_c <= 16:
        reasons.append("Low Temperature (<= 16°C)")
    if gas_ohms <= 20000:
        reasons.append("Poor Air Quality (Gas Resistance <= 20kΩ)")
    elif gas_ohms <= 30000:
        reasons.append("Moderate Air Quality (Gas Resistance <= 30kΩ)")
    severe = False
    if humidity >= 80 or humidity <= 20:
        severe = True
    if temp_c >= 30 or temp_c <= 14:
        severe = True
    if gas_ohms <= 20000:
        severe = True
    if not reasons:
        return {'risk': "SAFE", 'risk_reason': ["All sensor values within safe ranges"]}
    if severe:
        return {'risk': "WARNING", 'risk_reason': reasons}
    return {'risk': "ELEVATED", 'risk_reason': reasons}

    