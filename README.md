# Clinical Compass 🏥

An automated data pipeline that extracts, cleans, and loads GTA hospital nursing job postings into a structured PostgreSQL database — refreshed every week without lifting a finger.

## Why I Built This

Someone close to me is a nursing student navigating the frustrating process of finding clinical placements and job opportunities across GTA hospitals. Unlike tech or finance — where job boards, recruiting platforms, and career resources are abundant — healthcare is surprisingly underserved when it comes to centralized job discovery tools. Postings are scattered across individual hospital websites, updated inconsistently, and time-consuming to track manually. There's no "LinkedIn for nurses" that aggregates everything in one place.

I built Clinical Compass to close that gap — a pipeline that automatically pulls nursing postings from hospital career systems, filters out the noise, and loads clean, queryable data into a database. The goal is to make it easier to find relevant opportunities without spending hours clicking through hospital websites every week.

## What It Does

- Discovers nursing-related job postings from UHN (University Health Network) via their careers API
- Filters 190+ total postings down to relevant GTA nursing roles using keyword and location logic
- Loads cleaned postings into PostgreSQL with duplicate detection — new jobs get added, existing ones get skipped
- Saves timestamped raw snapshots on every run for traceability and debugging
- Runs automatically every Monday at 9am via Apache Airflow
- Fully containerized with Docker — one command starts everything

## Pipeline Architecture

```text
UHN Careers API
      ↓
src/extract.py        # Pull all 190+ postings + save timestamped snapshot
      ↓
data/raw/             # Raw JSON saved locally (latest + timestamped)
      ↓
src/clean.py          # Filter nursing GTA roles, handle nulls
      ↓
data/cleaned/         # Cleaned JSON
      ↓
src/load.py           # Load into PostgreSQL (ON CONFLICT DO NOTHING)
      ↓
nurse_job_postings database
```

Orchestrated by Apache Airflow running in Docker — weekly schedule with full task-level monitoring, logging, and run history.

## Stack

- **Python** — extraction, cleaning, loading, and filtering (`requests`, `psycopg2`)
- **PostgreSQL** — structured storage for both job postings and Airflow metadata
- **Apache Airflow** — weekly pipeline orchestration and monitoring
- **Docker & Docker Compose** — fully containerized, reproducible deployment
- **UHN Careers API** — source of hospital job posting data

## Project Structure

    clinical-compass/
    ├── dags/
    │   └── nursing_pipeline.py    # Airflow DAG — extract → clean → load
    ├── data/
    │   ├── raw/                   # Raw API responses + timestamped snapshots
    │   └── cleaned/               # Filtered and cleaned postings
    ├── docs/
    │   └── logs/                  # Saved Airflow task logs from pipeline runs
    ├── sql/
    │   └── create_tables.sql      # Database schema
    ├── src/
    │   ├── extract.py             # Pull postings from UHN API
    │   ├── clean.py               # Filter nursing GTA roles
    │   ├── load.py                # Load into PostgreSQL
    │   ├── filter.py              # Interactive job filter script
    │   └── wait_for_db.py         # Waits for Postgres to be ready before connecting
    ├── docker-compose.yml         # Defines db, app, and airflow-webserver services
    ├── Dockerfile                 # App container image
    └── requirements.txt

## Data Schema

    job_postings
    ├── id            TEXT PRIMARY KEY
    ├── title         TEXT
    ├── site          TEXT
    ├── employment    TEXT
    ├── department    TEXT
    └── ref_number    TEXT

## How to Run It

### Prerequisites
- Docker and Docker Compose
- Git

### Setup

1. Clone the repo
```bash
git clone https://github.com/daikevin335/clinical-compass.git
cd clinical-compass
```

2. Create a `.env` file with your credentials

CC_DB_NAME=nurse_job_postings
CC_DB_USER=youruser
CC_DB_PASSWORD=yourpassword
AIRFLOW_ADMIN_PASSWORD=yourairflowpassword


3. Start all services
```bash
docker compose up -d --build
```

This starts three containers:
- `db` — PostgreSQL database
- `app` — runs the ETL pipeline once on startup
- `airflow-webserver` — Airflow UI and scheduler

4. Access the Airflow UI

http://localhost:8080
Username: admin
Password: (whatever you set as AIRFLOW_ADMIN_PASSWORD in .env)



5. Trigger the pipeline manually or let it run on its Monday schedule

### Useful Docker commands

```bash
# Check running containers
docker ps

# View logs for a specific container
docker logs -f clinical-compass-airflow-webserver-1

# Trigger DAG manually
docker exec clinical-compass-airflow-webserver-1 airflow dags trigger nursing_pipeline

# Check database
docker exec clinical-compass-db-1 psql -U youruser -d nurse_job_postings -c "SELECT COUNT(*) FROM job_postings;"
```

### Filter jobs interactively

```bash
python3 src/filter.py
```

Filter by site, department, and employment type to find relevant postings.

## Limitations & Next Steps

- **Single source:** currently only pulls from UHN — expanding to Sunnybrook, SickKids, and Trillium is planned
- **Keyword filtering:** nursing role detection uses keyword matching which may miss some roles or include edge cases
- **Web interface:** a browser-based filter UI is planned so anyone can search postings without running scripts
- **Additional hospitals:** Sunnybrook and SickKids block automated requests — alternative data sources are being explored