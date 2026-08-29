from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

PROJECT_ROOT = "/opt/clinical-compass"

with DAG(
    dag_id="nursing_pipeline",
    schedule="0 9 * * 1",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["clinical-compass", "etl", "nursing"],
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="python src/extract.py",
        cwd=PROJECT_ROOT,
    )

    clean = BashOperator(
        task_id="clean",
        bash_command="python src/clean.py",
        cwd=PROJECT_ROOT,
    )

    load = BashOperator(
        task_id="load",
        bash_command="python src/load.py",
        cwd=PROJECT_ROOT,
    )

    extract >> clean >> load
