import os
import sys
import time
import psycopg2

"""
wait_for_db.py

This script waits until PostgreSQL is ready before the app continues.
We use this in Docker because Postgres may take a few seconds to start,
and the app should not try to connect too early.
"""

# --- Config ---
# Reads database connection values from environment variables.
# In docker, these willl be set automatically by docker-compose.
# In local dev, the defaults are used iif the variables aren't set. 

host = os.getenv("CC_DB_HOST", "localhost")
port = os.getenv("CC_DB_PORT", "5432")
dbname = os.getenv("CC_DB_NAME", "nurse_job_postings")
user = os.getenv("CC_DB_USER", "kevindai")
password = os.getenv("CC_DB_PASSWORD")

print(f"Waiting for database {user}@{host}:{port}/{dbname} ...")

# --- Retry ---
RETRIES = 30
SLEEP_SECONDS = 2

# Try to connect to Postgres repeadtly.
# If database is not ready, wait and retry 
for attempt in range(RETRIES):
    try:
        # Try to open connection
        # If successs; Postgres is accepting connections
        conn = psycopg2.connect(dbname = dbname, user = user, password = password, host = host, port = port)
        conn.close()

        print("\nDatabase is available")
        sys.exit(0)

    except Exception:
        # If connection fails, not ready yet
        print(".", end = "", flush = True)
        time.sleep(SLEEP_SECONDS)

print("\nTimed out waiting for the database to become available")
sys.exit(1)