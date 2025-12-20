import json
import os
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB resource and table
ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["TABLE_NAME"])

