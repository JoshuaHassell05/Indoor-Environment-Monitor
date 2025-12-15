def evaluate_risk(reading: dict) -> dict:
    temp_c = reading.get('temperature')
    humidity = reading.get('humidity')
    gas_ohms = reading.get('gas_resistance')
    if temp_c is None or humidity is None or gas_ohms is None:
        return {'risk': "Elevated", 'risk_reason': ["Missing one or more required sensor values"]
        }
    