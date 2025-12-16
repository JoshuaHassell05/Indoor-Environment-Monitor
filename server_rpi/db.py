import sqlite3
import json
from pathlib import Path
"""Database module for storing and retrieving sensor readings using SQLite."""
DB_PATH = Path(__file__).resolve().parent / "readings.db"
def get_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Create the readings table if it does not exist."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            data TEXT NOT NULL
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

def fetch_recent_readings(limit: int = 100) -> list[dict]:
    """Fetches the most recent sensor readings from the database."""
    limit = max(1, min(limit, 1000))  # Clamp limit between 1 and 1000
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT 
                timestamp,
                temperature,
                humidity,
                pressure,
                gas_resistance,
                risk,
                risk_reasons
            FROM readings
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()
        rows = list(reversed(rows))
        results = []
        for row in rows:
            try: 
                reasons = json.loads(row['risk_reasons'] or '[]')
            except json.JSONDecodeError:
                reasons = []
            results.append({
                'timestamp': row['timestamp'],
                'temperature': row['temperature'],
                'humidity': row['humidity'],
                'pressure': row['pressure'],
                'gas_resistance': row['gas_resistance'],
                'risk': row['risk'],
                'risk_reasons': reasons
            })
        return results