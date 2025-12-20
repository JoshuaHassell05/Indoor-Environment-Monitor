import json
import os
from datetime import datetime, timezone
from decimal import Decimal
import boto3
from common.analytics import attach_risk_fields

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["TABLE_NAME"])

def _to_decimal(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return Decimal(str(x))
    return x

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