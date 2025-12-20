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
