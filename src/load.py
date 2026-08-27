import os
import json 
import psycopg2

"""
Loads cleaned job postings into PostgreSQL.

Basically:
- connect to nurse_job_postings
- read cleaned JSON
- insert each posting into job_postings
- ignore duplicates using ON CONFLICT (id) DO NOTHING
- commit changes and close the DB connection

Why this matters:
- keeps data in a queryable database
- prevents duplicate records on repeated runs

NOTES:
- os.getenv(...) means "read from enivornment variables if available"   
"""


# Connect to psql
 
conn = psycopg2.connect(
    dbname = os.getenv("CC_DB_NAME", "nurse_job_postings"),
    user = os.getenv("CC_DB_USER", "kevindai"),
    password = os.getenv("CC_DB_PASSWORD"),
    host = os.getenv("CC_DB_HOST", "localhost"), 
    port = os.getenv("CC_DB_PORT", "5432")
)
cursor = conn.cursor()

# Load cleaned data

jobs = json.load(open('data/cleaned/uhn_jobs.json'))
print(f"Jobs to load: {len(jobs)}")

# Insert each job

for job in jobs:
    cursor.execute("""
        INSERT INTO job_postings (id, title, site, employment, department, ref_number)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        job['id'],
        job['title'],
        job['site'],
        job['employment'],
        job['department'],
        job['ref_number']
    ))

conn.commit()
cursor.close()
conn.close()

print("Jobs loaded.")