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
