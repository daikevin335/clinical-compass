import json 
import psycopg2

# Connect to psql
conn = psycopg2.connect(
    dbname = "nurse_job_postings",
    user = "kevindai"
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