import json
import os
from datetime import datetime, timezone
from decimal import Decimal
import boto3
from common.analytics import attach_risk_fields

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["TABLE_NAME"])

# Helper to convert values to Decimal or None
def _to_decimal(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return Decimal(str(x))
    return x

# Helper function to create HTTP response with CORS headers
def _resp(status, body):
    allowed = os.environ.get("ALLOWED_ORIGIN", "*")
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": allowed,
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body),
    }

# Main Lambda handler function
def lambda_handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return _resp(200, {"ok": True})
    raw_body = event.get("body") or ""
    try:
        data = json.loads(raw_body) if isinstance(raw_body, str) else (raw_body or {})
    except Exception:
        return _resp(400, {"status": "error", "message": "Invalid JSON"})

    if not isinstance(data, dict) or not data:
        return _resp(400, {"status": "error", "message": "No data provided"})
    device_id = data.get("device_id") or os.environ.get("DEFAULT_DEVICE_ID", "device-1")
    ts = datetime.now(timezone.utc).isoformat()
    # Prepare reading dict
    reading = {
    "device_id": device_id,
    "timestamp": ts,
    "temperature": _to_decimal(data.get("temperature")),
    "humidity": _to_decimal(data.get("humidity")),
    "pressure": _to_decimal(data.get("pressure")),
    "gas_resistance": _to_decimal(data.get("gas_resistance")),
    }
    # Adds risk + reasons
    reading = attach_risk_fields(reading)
    # Store in DynamoDB
    item = {"pk": device_id, "sk": ts, **reading}
    table.put_item(Item=item)
    return _resp(200, {"status": "success"})