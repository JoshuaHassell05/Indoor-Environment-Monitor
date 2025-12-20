import json
import os
from datetime import datetime, timezone
from decimal import Decimal
import boto3
from common.analytics import attach_risk_fields