import json 
from pathlib import Path

"""
Cleans the raw UHN job data.

Basically:
- load raw JSON from data/raw/uhn_jobs.json
- keep only nursing-related roles
- keep only GTA hospitals
- normalize missing values
- write cleaned jobs to data/cleaned/uhn_jobs.json

Why this matters:
- reduces the dataset to relevant jobs before loading to Postgres
- avoids storing noisy or irrelevant postings
"""

# Load raw data
raw_path = Path("data/raw/uhn_jobs.json")
cleaned_path = Path("data/cleaned/uhn_jobs.json")

jobs = json.load(open('data/raw/uhn_jobs.json'))
print(f"Raw jobs: {len(jobs)}")

# --- Filter 1: Nursing related roles only ---

nurse_keywords = ['nurse', 
                  'nursing', 
                  'rpn', 
                  'clinical coordinator',
                  'patient care',
                  'clinical extern',
                  'student nurse',
                  'nurse extern',
                  'nurse practitioner']

def is_nursing_role(job):
    title = job['name'].lower()
    return any(keyword in title for keyword in nurse_keywords)

# --- Filter 2: GTA region only ---

excluded_sites = ['barrie', 
                  'oshawa', 
                  'hamilton', 
                  'oakville', 
                  'vaughan',
                  'brampton',
                  'missisauga']

def is_gta_hospital(job):
    site = job['site'].lower()
    # Keep UHN core hospitals, exclude Altum outlying locations
    return not any(city in site for city in excluded_sites)

# --- Clean and filter --- 
cleaned = []

for job in jobs:
    # Basic data quality checks
    if not job.get("name"):
        continue
    if not job.get("site"):
        continue

    if not is_nursing_role(job):
        continue
    if not is_gta_hospital(job):
        continue

    cleaned.append({
        "id": job["id"],
        "title": job["name"],
        "site": job["site"],
        "employment": job["employment"] if job.get("employment") else "Not Specified",
        "department": job["department"] if job.get("department") else "Not Specified", 
        "ref_number": job["refNumber"] if job.get("refNumber") else "Not Specified"
    })

print(f"Cleaned Jobs: {len(cleaned)}") 

# Save clean data
cleaned_path.parent.mkdir(parents = True, exist_ok = True)

with open(cleaned_path, "w") as f:
    json.dump(cleaned, f, indent = 2)

print("Saved to data/cleaned/uhn_jobs.json")