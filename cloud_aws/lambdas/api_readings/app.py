import os
import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB resource and table
TABLE_NAME = os.environ.get("TABLE_NAME", "IndoorEnvReadings")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

# Helper function to create HTTP response with CORS headers
def _resp(status: int, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body, default=_json_default),
    }

# Helper for JSON serialization
def _json_default(o): 
    if isinstance(o, Decimal):
        return float(o)
    return str(o)

# Parse the range string and return corresponding time delta and bucket size
def _parse_range(range_str: str):
    if range_str == "week":
        return timedelta(days=7), timedelta(hours=6)
    if range_str == "month":
        return timedelta(days=30), timedelta(days=1)
    return timedelta(days=1), timedelta(minutes=15)

# Floor a datetime to the nearest bucket
def _floor_to_bucket(dt: datetime, bucket: timedelta) -> datetime:
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    seconds = int((dt - epoch).total_seconds())
    bucket_seconds = int(bucket.total_seconds())
    floored = (seconds // bucket_seconds) * bucket_seconds
    return epoch + timedelta(seconds=floored)

# Main Lambda handler function
def lambda_handler(event, context):
    # Handle CORS preflight request
    if event.get("httpMethod") == "OPTIONS":
        return _resp(200, {"ok": True})
    
    params = event.get("queryStringParameters") or {}
    range_str = (params.get("range") or "day").lower()
    device_id = params.get("device_id") or "device-1"
    window, bucket = _parse_range(range_str)
    now = datetime.now(timezone.utc)
    start = now - window

    # Prepare DynamoDB keys
    start_sk = start.isoformat()
    end_sk = now.isoformat()

     # Query DynamoDB for items in time range (paginated)
    items = []
    kwargs = {
        "KeyConditionExpression": Key("pk").eq(device_id) & Key("sk").between(start_sk, end_sk),
        "ScanIndexForward": True,  # ascending by time
    }

    while True:
        resp = table.query(**kwargs)
        items.extend(resp.get("Items", []))

        last_key = resp.get("LastEvaluatedKey")
        if not last_key:
            break
        kwargs["ExclusiveStartKey"] = last_key

    # Group into buckets and compute averages
    buckets = {}  
    for it in items:
        ts = it.get("sk")
        if not ts:
            continue

        try:
            dt = datetime.fromisoformat(ts)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
        except Exception:
            continue

        bdt = _floor_to_bucket(dt, bucket)
        label = bdt.strftime("%Y-%m-%d %H:%M")
        # Extract readings
        temp = it.get("temperature")
        hum = it.get("humidity")
        gas = it.get("gas_resistance")

        # Convert Decimal -> float when summing
        def to_float(x):
            if x is None:
                return None
            if isinstance(x, Decimal):
                return float(x)
            return float(x)

        temp = to_float(temp)
        hum = to_float(hum)
        gas = to_float(gas)

        if label not in buckets:
            buckets[label] = {
                "count": 0,
                "temp_sum": 0.0,
                "hum_sum": 0.0,
                "gas_sum": 0.0,
            }

        # Skip if any reading is missing
        if temp is None or hum is None or gas is None:
            continue

        buckets[label]["count"] += 1
        buckets[label]["temp_sum"] += temp
        buckets[label]["hum_sum"] += hum
        buckets[label]["gas_sum"] += gas

    # Prepare output list with averages
    out = []
    for label in sorted(buckets.keys()):
        c = buckets[label]["count"]
        if c == 0:
            out.append({"t": label, "temp_avg": None, "hum_avg": None, "gas_avg": None})
        else:
            out.append({
                "t": label,
                "temp_avg": buckets[label]["temp_sum"] / c,
                "hum_avg": buckets[label]["hum_sum"] / c,
                "gas_avg": buckets[label]["gas_sum"] / c,
            })
    return _resp(200, out)