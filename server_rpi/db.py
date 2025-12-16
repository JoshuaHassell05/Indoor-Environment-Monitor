import sqlite3
import json
from pathlib import Path

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