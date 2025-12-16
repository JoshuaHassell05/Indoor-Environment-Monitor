import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "readings.db"