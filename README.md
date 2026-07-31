# Clinical Compass 🏥

An automated data pipeline that extracts, cleans, and loads GTA hospital nursing job postings into a structured PostgreSQL database — refreshed every week without lifting a finger.

## Why I Built This

Someone close to me is a nursing student navigating the frustrating process of finding clinical placements and job opportunities across GTA hospitals. Unlike tech or finance — where job boards, recruiting platforms, and career resources are abundant — healthcare is surprisingly underserved when it comes to centralized job discovery tools. Postings are scattered across individual hospital websites, updated inconsistently, and time-consuming to track manually. There's no "LinkedIn for nurses" that aggregates everything in one place.

I built Clinical Compass to close that gap — a pipeline that automatically pulls nursing postings from hospital career systems, filters out the noise, and loads clean, queryable data into a database. The goal is to make it easier to find relevant opportunities without spending hours clicking through hospital websites every week.

## What It Does

- Discovers nursing-related job postings from UHN (University Health Network) via their careers API
- Filters 200+ total postings down to relevant GTA nursing roles using keyword and location logic
- Loads cleaned postings into PostgreSQL with duplicate detection — new jobs get added, existing ones get skipped
- Runs automatically every Monday at 9am via Apache Airflow

## Pipeline Architecture

```text
UHN Careers API
      ↓
src/extract.py     # Pull all 200+ postings
      ↓
data/raw/          # Raw JSON saved locally
      ↓
src/clean.py       # Filter nursing GTA roles, handle nulls
      ↓
data/cleaned/      # Cleaned JSON
      ↓
src/load.py        # Load into PostgreSQL (ON CONFLICT DO NOTHING)
      ↓
nurse_job_postings database
```

Orchestrated by Apache Airflow — runs on a weekly schedule with full task-level monitoring and logging.

## Data Schema

    job_postings
    ├── id            TEXT PRIMARY KEY
    ├── title         TEXT
    ├── site          TEXT
    ├── employment    TEXT
    ├── department    TEXT
    └── ref_number    TEXT

## Stack

- **Python** — extraction, cleaning, and loading (`requests`, `psycopg2`)
- **PostgreSQL** — structured storage for cleaned job postings
- **Apache Airflow** — weekly pipeline orchestration and monitoring
- **UHN Careers API** — source of hospital job posting data

## Project Structure

    clinical-compass/
    ├── data/
    │   ├── raw/               # Raw API responses
    │   └── cleaned/           # Filtered and cleaned postings
    ├── src/
    │   ├── extract.py         # Pull postings from UHN API
    │   ├── clean.py           # Filter nursing GTA roles
    │   └── load.py            # Load into PostgreSQL
    └── requirements.txt

The Airflow DAG lives at `~/airflow/dags/nursing_pipeline.py` and runs the three scripts in sequence every Monday.

## How to Run It

### Prerequisites
- Python 3.x
- PostgreSQL (via Postgres.app on Mac)
- Apache Airflow

### Setup

1. Clone the repo
```bash
git clone https://github.com/daikevin335/clinical-compass.git
cd clinical-compass
```

2. Install dependencies
```bash
pip3 install -r requirements.txt
```

3. Create the database in psql
```sql
CREATE DATABASE nurse_job_postings;
\c nurse_job_postings
CREATE TABLE job_postings (
    id TEXT PRIMARY KEY,
    title TEXT,
    site TEXT,
    employment TEXT,
    department TEXT,
    ref_number TEXT
);
```

4. Run the pipeline manually
```bash
python3 src/extract.py
python3 src/clean.py
python3 src/load.py
```

5. Set up Airflow automation
```bash
export AIRFLOW_HOME=~/airflow
airflow db migrate
airflow standalone
```

Then copy `nursing_pipeline.py` to `~/airflow/dags/` and the pipeline will run every Monday at 9am.

## Limitations & Next Steps

- **Single source:** currently only pulls from UHN — expanding to Sunnybrook, SickKids, and Trillium is planned
- **Keyword filtering:** nursing role detection uses keyword matching which may miss some roles or include edge cases
- **User-facing filter layer:** a query interface letting users filter by employment type, department, or site is planned
- **Airflow on Mac only:** the current setup assumes Postgres.app and local Airflow — a future iteration would containerize with Docker for portability
