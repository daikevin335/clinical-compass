import json 
from datetime import datetime, timezone
from pathlib import Path

import requests

"""
Extracts UHN job postings from the careers API.

Basically:
- call the UHN jobs endpoint
- check for a successful HTTP response
- parse the JSON payload
- pull the 'data' list of job postings
- save raw postings to data/raw/uhn_jobs.json

Why this matters:
- raw API output is preserved before cleaning
- we keep an unmodified snapshot for debugging and traceability
"""



# --- API + output config --- 

UHN_URL = "https://forms.uhn.ca/UHNCareers/Home/GetAll?tcnt=201" 
RAW_DIR = Path("data/raw")
LATEST_OUTPUT = RAW_DIR / "uhn_jobs.json"
REQUEST_TIMEOUT_SECONDS = 30

# --- Fetch data from UHN API ---

def fetch_jobs(): 
    print(f"Fetching UHN job postings from {UHN_URL}...") 
    response = requests.get(UHN_URL, timeout = REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()

    payload = response.json()
    jobs = payload.get("data", [])

    # Guardrail: fail clearly if API response shape change
    if not isinstance(jobs, list):
        raise ValueError("Expected API response key 'data' to be a list")

    return jobs

# --- Save raw data (latest + timestaped snapshot) --- 

def save_raw_jobs(jobs):
    RAW_DIR.mkdir(parents = True, exist_ok = True)  

    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") # Unique timestamp string creation
    snapshot_output = RAW_DIR / f"uhn_jobs_{run_stamp}.json"

    with open(LATEST_OUTPUT, "w") as f:
        json.dump(jobs, f, indent=2)

    with open(snapshot_output, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved latest raw data to {LATEST_OUTPUT}")
    print(f"Saved snapshot raw data to {snapshot_output}")

# --- Script entrypoint --- 

if __name__ == "__main__":
    jobs = fetch_jobs()
    print(f"Jobs found: {len(jobs)}")
    save_raw_jobs(jobs)