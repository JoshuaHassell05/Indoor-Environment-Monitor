import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "readings.db"
def get_conn() -> sqlite3.Connection:
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Create the readings table if it does not exist."""
    conn = get_conn()
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