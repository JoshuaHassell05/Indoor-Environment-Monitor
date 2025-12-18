import sqlite3
import json
from pathlib import Path

"""
Database module for storing and retrieving sensor readings using SQLite.
"""

DB_PATH = Path(__file__).resolve().parent / "readings.db"
def get_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Create the readings table if it does not exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                pressure REAL,
                gas_resistance REAL,
                risk TEXT,
                risk_reasons TEXT
            )
            """
        )
        conn.commit()


def insert_reading(reading: dict) -> None:
    """Inserts a sensor reading into the database."""
    reasons_json = json.dumps(reading.get('risk_reasons', []))
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO readings(
                timestamp,
                temperature,
                humidity,
                pressure,
                gas_resistance,
                risk,
                risk_reasons
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,           
            (
                reading['timestamp'],
                reading.get('temperature'),
                reading.get('humidity'),
                reading.get('pressure'),
                reading.get('gas_resistance'),
                reading.get('risk'),
                reasons_json
            )
        )
        conn.commit()

def fetch_series(range_key: str = "day") -> list[dict]:
    """Return a time series of aggregated sensor readings.
    range_key controls:
    - "day": last 24 hours, bucket by 5 minutes
    - "week": last 7 days, bucket by 1 hour
    - "month": last 30 days, bucket by 1 day
    """
    if range_key == "day":
        since_modifier = "-1 day"
        bucket_fmt = "%Y-%m-%d %H:%M"   
        bucket_step = 5                
    elif range_key == "week":
        since_modifier = "-7 days"
        bucket_fmt = "%Y-%m-%d %H:00"   
        bucket_step = None
    else:  # "month"
        since_modifier = "-30 days"
        bucket_fmt = "%Y-%m-%d"         
        bucket_step = None

    # We filter to a window (day/week/month), then group readings into time buckets.
    with get_connection() as conn:
        if bucket_step is None:
            rows = conn.execute(
                f"""
                SELECT
                  strftime('{bucket_fmt}', timestamp) AS t,
                  AVG(temperature) AS temp_avg,
                  AVG(humidity) AS hum_avg,
                  AVG(gas_resistance) AS gas_avg
                FROM readings
                WHERE datetime(timestamp) >= datetime('now', ?)
                GROUP BY t
                ORDER BY t ASC;
                """,
                (since_modifier,),
            ).fetchall()
        else:
            # For 5-minute buckets, we group by "hour + floor(minute/5)*5".
            rows = conn.execute(
                """
                SELECT
                  -- Build a bucket label like "YYYY-MM-DD HH:MM" where MM is 00,05,10,...55
                  strftime('%Y-%m-%d %H:', timestamp) ||
                  printf('%02d', (CAST(strftime('%M', timestamp) AS INTEGER) / 5) * 5) AS t,
                  AVG(temperature) AS temp_avg,
                  AVG(humidity) AS hum_avg,
                  AVG(gas_resistance) AS gas_avg
                FROM readings
                WHERE datetime(timestamp) >= datetime('now', ?)
                GROUP BY t
                ORDER BY t ASC;
                """,
                (since_modifier,),
            ).fetchall()

    # Convert sqlite rows to normal Python dicts 
    series = []
    for r in rows:
        series.append(
            {
                "t": r["t"],
                "temp_avg": r["temp_avg"],
                "hum_avg": r["hum_avg"],
                "gas_avg": r["gas_avg"],
            }
        )
    return series
    