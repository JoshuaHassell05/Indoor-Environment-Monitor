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