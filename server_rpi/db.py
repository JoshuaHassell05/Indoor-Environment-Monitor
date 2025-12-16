import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "readings.db"
def get_conn() -> sqlite3.Connection:
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
