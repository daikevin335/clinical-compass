
-- job_postings: main table of cleaned nursing job records (1 row = 1 posting)
-- pipline_runs: pipeline run history/metrics for monitoring and debugging (1 row = 1 run)

-- Core buisness data used by app/query layer
CREATE TABLE IF NOT EXISTS job_postings (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    site TEXT NOT NULL,
    employment TEXT NOT NULL,
    department TEXT NOT NULL,
    ref_number TEXT NOT NULL
);

-- Operational metdata for ETL obersvability and run-tracking
CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id TEXT PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ NOT NULL,
    source TEXT NOT NULL,
    raw_total INTEGER,
    cleaned_total INTEGER NOT NULL,
    inserted_total INTEGER NOT NULL,
    skipped_total INTEGER NOT NULL,
    status TEXT NOT NULL
);