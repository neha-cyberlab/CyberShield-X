
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "cybershield.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS security_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                username TEXT NOT NULL,
                severity TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS security_alerts (
                alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                username TEXT NOT NULL,
                severity TEXT NOT NULL,
                failed_attempts INTEGER NOT NULL,
                description TEXT NOT NULL
            )
        """)


if __name__ == "__main__":
    init_db()
    print("CyberShield X database initialized successfully.")
    print(f"Database location: {DB_PATH}")
