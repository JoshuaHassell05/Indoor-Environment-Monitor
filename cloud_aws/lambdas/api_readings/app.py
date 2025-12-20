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