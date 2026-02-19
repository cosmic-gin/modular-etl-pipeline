# 🚀 Modular ETL Pipeline (Python · Docker · Airflow)

A **production-style modular ETL pipeline** built with clean architecture, containerization, and orchestration in mind.

This project ingests CSV/JSON observation data, validates it using **config-driven rules**, normalizes it into a consistent schema, and outputs **curated datasets** (Parquet preferred).  
It also includes a **Docker Compose stack with Apache Airflow** for orchestration.

---

## 📌 Overview

### 📥 Inputs
Located in:
data/raw/

Supported formats:
- CSV
- JSON

---

### 🔄 Pipeline Stages

1️⃣ **Ingest**  
Reads CSV and JSON sources (optionally in parallel).

2️⃣ **Validate**  
Applies rule-based validation driven by `pipeline.toml`.

3️⃣ **Transform**  
Normalizes heterogeneous records into a canonical schema.

4️⃣ **Load**  
Writes curated outputs:
- **Parquet** (if `pyarrow` is available)
- Fallback to CSV otherwise  
- Generates structured JSON reports

---

## 📤 Outputs

All outputs are written to:
data/processed/


Generated files:

- `validation_report_<run_id>.json`
- `observations_cleaned_<run_id>.parquet` *(preferred)* or `.csv`
- `run_summary_<run_id>.json`

Each execution is uniquely identified by a `run_id`.

---

## ⚙️ Key Features

✅ Modular architecture under `src/etl/`  
✅ Config-driven pipeline (`pipeline.toml`)  
✅ CLI `--run-id` override (useful for Airflow)  
✅ Relative-path config resolution  
✅ Structured JSON validation reports  
✅ Parquet support via `pyarrow`  
✅ Dockerized ETL execution  
✅ Local Airflow stack (Webserver + Scheduler + Postgres)  
✅ DAG-triggered runs using `{{ ts_nodash }}` as `run_id`

---

## 🧰 Requirements

🐍 Python 3.12+

🐳 Docker + Docker Compose (for containerized runs / Airflow)

📦 Optional but recommended: pyarrow (for Parquet output)

## 🖥️ Quickstart (Local Python)

Create a virtual environment:
```
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install .
```
Run the pipeline:
```
python -m etl --config pipeline.toml --run-id manual --log-level INFO
```

Run with failing config (expected exit code = 2):
```
python -m etl --config pipeline_bad.toml --run-id bad-run --log-level INFO
```

Lint & Test:
```
ruff check .
pytest -q
```

⚙️ Configuration

The pipeline reads a TOML configuration file (e.g., `pipeline.toml`).

Common configuration options:

- pipeline.name
- pipeline.run_id
- paths.raw_dir
- paths.processed_dir
- paths.reports_dir
- sources.csv_files
- sources.json_files
- Validation thresholds (allowed_sites, numeric ranges, etc.)
- Ingestion parallelism (max_workers)

### 📌 Note:
Relative paths are resolved relative to the TOML file location.

## 🐳 Docker: Run ETL Service

Build and execute:
```
docker compose build etl
docker compose run --rm etl
```
Outputs will appear in:
```
data/processed/
```
## 🌬️ Airflow (Local via Docker Compose)
### 1️⃣ Configure Credentials

Copy the example:
```
cp .env.example .env
```
Example ` .env.example `:
```
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
_AIRFLOW_WWW_USER_FIRSTNAME=Airflow
_AIRFLOW_WWW_USER_LASTNAME=Admin
_AIRFLOW_WWW_USER_ROLE=Admin
_AIRFLOW_WWW_USER_EMAIL=airflow@example.com

# Match host UID so mounted volumes aren't owned by root
AIRFLOW_UID=50000
```
Valid roles:
```
Admin, User, Viewer, Op, Public
```
## 2️⃣ Start Airflow
```
docker compose build
docker compose up airflow-init
docker compose up -d postgres airflow-webserver airflow-scheduler
docker compose ps
```
Open the UI:
```
Open the UI:
```

## 3️⃣ Trigger the DAG
```
docker compose exec airflow-webserver airflow dags list | grep modular_etl_pipeline
docker compose exec airflow-webserver airflow dags unpause modular_etl_pipeline
docker compose exec airflow-webserver airflow dags trigger modular_etl_pipeline
```
Each DAG run writes outputs using:
```
run_id = {{ ts_nodash }}
```
Files appear in:
```
data/processed/
```
## 🧪 CI Integration

GitHub Actions runs:

- Ruff (lint)
- Pytest
- Docker build validation (optional on push to main)

Ensures code quality and reproducibility.

👨‍💻 Author

Built as a modular, production-style ETL demonstration project using:

- Python 3.12
- Docker
- Apache Airflow
- Postgres
- Parquet (pyarrow)

Built with ❤️ for clean data engineering workflows.
