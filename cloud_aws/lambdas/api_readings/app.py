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