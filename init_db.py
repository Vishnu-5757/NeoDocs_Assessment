import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    db_name = os.getenv("DATABASE_NAME", "test_data.db")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            test_id TEXT PRIMARY KEY,
            patient_id TEXT NOT NULL,
            clinic_id TEXT NOT NULL,
            test_type TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database is initialized.")

if __name__ == "__main__":
    init_db()