import requests
import json
from pathlib import Path

# --- UHN Jobs API --- 

UHN_URL = "https://forms.uhn.ca/UHNCareers/Home/GetAll?tcnt=201" 

print("Fetching UHN job postings")
response = requests.get(UHN_URL)

if response.status_code != 200:
    print("ERROR:", response.status_code)
    exit()

data = response.json()
jobs = data['data']
print(f"Jobs found: {len(jobs)}")

# Save raw data
output_path = Path("data/raw/uhn_jobs.json")
output_path.parent.mkdir(parents = True, exist_ok = True)

with open(output_path, "w") as f:
    json.dump(jobs, f, indent = 2)

print("Saved to data/raw/uhn_jobs.json")