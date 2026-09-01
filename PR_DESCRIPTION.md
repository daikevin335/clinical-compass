PR: Fix Airflow config, restore DAG, document login, and add run logs

Summary
- Restored `dags/nursing_pipeline.py` so Airflow mounts and runs the DAG inside the container.
- Updated `docker-compose.yml` to use `airflow standalone` startup for the official image and avoid mismatched custom auth overrides.
- Updated README with a note explaining where to find the generated standalone admin password and added `.venv/` to `.gitignore`.
- Captured the successful DAG run logs under `docs/logs/nursing_pipeline/manual__2026-09-01T06:11:57+00:00/`.

Why
- The webserver returned a 500 when triggering the DAG because the webserver saw DB records for a DAG but the source file was missing from the container. Restoring the DAG file fixed that.

Files changed
- docker-compose.yml
- README.md
- .gitignore
- dags/nursing_pipeline.py
- docs/logs/nursing_pipeline/manual__2026-09-01T06:11:57+00:00/{extract.log,clean.log,load.log}

Notes for reviewer
- Please confirm that the hardcoded example credentials in docker-compose.yml are acceptable for your use; if not, switch to a .env file and add that to .gitignore before merging.
- The standalone admin password file inside the container is at `/opt/airflow/standalone_admin_password.txt`.

How to test
1. docker compose up -d --force-recreate db
2. docker compose up -d --force-recreate airflow
3. Visit http://localhost:8080 and login as `admin` with the generated password from `/opt/airflow/standalone_admin_password.txt` in the airflow container.
4. Unpause and trigger the `nursing_pipeline` DAG and confirm a successful run. The run logs should appear under `docs/logs/...` for the run saved here.
