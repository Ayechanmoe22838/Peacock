import os
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from sqlalchemy import create_engine, text
from app.core.config import settings

def wait_for_database(max_retries: int = 30, retry_interval: int = 2):
    """
    Waits for the MySQL database to become responsive before continuing startup.
    Compatible with Railway MySQL plugin, Docker Compose, and local environments.
    """
    db_display = settings.DATABASE_URL
    if "@" in db_display:
        db_display = db_display.split("@")[-1]
    
    print(f"⏳ Checking database connection to: {db_display}...")
    retries = 0
    while retries < max_retries:
        try:
            test_engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
            with test_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Database connection successful and healthy!")
            return True
        except Exception as e:
            retries += 1
            print(f"⚠️ Database not ready yet (attempt {retries}/{max_retries}): {e}")
            time.sleep(retry_interval)
    
    print("❌ Could not connect to database after maximum retries.")
    sys.exit(1)

if __name__ == "__main__":
    wait_for_database()
