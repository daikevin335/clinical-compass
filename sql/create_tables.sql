CREATE TABLE IF NOT EXISTS job_postings (
    id SERIAL PRIMARY KEY, 
    title TEXT NOT NULL,
    site TEXT NOT NULL, 
    employment TEXT NOT NULL,
    department TEXT NOT NULL,
    ref_number TEXT NOT NULL,
); 

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id TEXT PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ NOT NULL,
    source TEXT NOT NULL,
    raw_totoal INTEGER,
    cleaned_total INTEGER NOT NULL,
    inserted_total INTEGER NOT NULL,
    skipped_total INTEGER NOT NULL,
    status TEXT NOT NULL
);