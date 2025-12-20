import json
import os
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB resource and table
ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["TABLE_NAME"])

# Function to fetch item from DynamoDB and return as JSON
def _json_default(o):
    if isinstance(o, Decimal):
        return float(o)
    raise TypeError(f"Type not serializable: {type(o)}")

# Helper function to create HTTP response
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
        # Serialize body to JSON
        "body": json.dumps(body, default=_json_default), 
    }

# Main Lambda handler function
def lambda_handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return _resp(200, {"ok": True})
    # Extract device_id from query parameters or use default
    qs = event.get("queryStringParameters") or {}
    device_id = (qs.get("device_id") if isinstance(qs, dict) else None) or os.environ.get("DEFAULT_DEVICE_ID", "device-1")
    # Query DynamoDB for the latest item for the given device_id
    res = table.query(
        KeyConditionExpression=Key("pk").eq(device_id),
        ScanIndexForward=False,
        Limit=1,
    )
    # Process the query result
    items = res.get("Items", [])
    if not items:
        return _resp(200, {})
    # Extract the first item and prepare the output
    it = items[0]
    out = {
        "timestamp": it.get("timestamp"),
        "temperature": it.get("temperature"),
        "humidity": it.get("humidity"),
        "pressure": it.get("pressure"),
        "gas_resistance": it.get("gas_resistance"),
        "risk": it.get("risk"),
        "risk_reasons": it.get("risk_reasons") or [],
        "device_id": device_id,
    }
    # Return the output as a JSON response
    return _resp(200, out)