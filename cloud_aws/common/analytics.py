"""
Risk evaluation logic for environmental sensor readings.
"""
def evaluate_risk(reading: dict) -> dict:
    temp_c = reading.get('temperature')
    humidity = reading.get('humidity')
    gas_ohms = reading.get('gas_resistance')
    try:
        if temp_c is not None:
            temp_c = float(temp_c)
        if humidity is not None:
            humidity = float(humidity)
        if gas_ohms is not None:
            gas_ohms = float(gas_ohms)
    except Exception:
        return {
            'risk': "ELEVATED",
            'risk_reasons': ["Invalid sensor value types"]
        }

    if temp_c is None or humidity is None or gas_ohms is None:
        return {
            'risk': "ELEVATED",
            'risk_reasons': ["Missing one or more required sensor values"]
        }

    reasons = []
    if humidity >= 70:
        reasons.append("High Humidity")
    elif humidity <= 25:
        reasons.append("Very Low Humidity")

    if temp_c >= 30.0:
        reasons.append("High Temperature")
    elif temp_c >= 25.6:
        reasons.append("Warm Temperature")
    elif temp_c <= 15.6:
        reasons.append("Low Temperature")

    if gas_ohms <= 20000:
        reasons.append("Poor Air Quality")
    elif gas_ohms <= 30000:
        reasons.append("Moderate Air Quality")

    severe = (
        humidity >= 80 or humidity <= 20 or
        temp_c >= 30.0 or temp_c <= 15.6 or
        gas_ohms <= 20000
    )

    if not reasons:
        return {
            'risk': "SAFE",
            'risk_reasons': ["All sensor values within safe ranges"]
        }

    if severe:
        return {'risk': "WARNING", 'risk_reasons': reasons}

    return {'risk': "ELEVATED", 'risk_reasons': reasons}


def attach_risk_fields(reading: dict) -> dict:
    risk_info = evaluate_risk(reading)
    reading['risk'] = risk_info['risk']
    reading['risk_reasons'] = risk_info['risk_reasons']
    return reading
