from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="modular_etl_pipeline",
    start_date=datetime(2026, 2, 19),
    schedule=None,
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=1)},
    tags=["etl", "local"],
) as dag:
    run_etl = BashOperator(
        task_id="run_etl",
        bash_command=(
            "python -m etl "
            "--config /opt/project/pipeline.toml "
            "--run-id {{ ts_nodash }} "
            "--log-level INFO"
        ),
    )
