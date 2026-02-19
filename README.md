# Modular ETL Pipeline (Python • Docker • Airflow)

A small, production-style **modular ETL** project that ingests CSV/JSON observation data, validates it with **config-driven rules**, normalizes it into a consistent schema, and writes curated outputs (**Parquet preferred**). It also includes a local **Docker Compose** stack and an **Airflow DAG** to orchestrate runs.

## What it does

**Inputs:** `data/raw/` (CSV + JSON)

**Pipeline:**
1. **Ingest** — read CSV/JSON sources (optionally in parallel).
2. **Validate** — rule-based checks driven by `pipeline.toml`.
3. **Transform** — normalize heterogeneous records into one canonical schema.
4. **Load** — write curated dataset (**Parquet if `pyarrow` is available**, else CSV) plus JSON reports.

**Outputs:** `data/processed/`
- `validation_report_<run_id>.json`
- `observations_cleaned_<run_id>.parquet` (preferred) or `.csv`
- `run_summary_<run_id>.json`

## Key features

- `src/` layout packaging (`etl` module)
- Config-driven pipeline (`pipeline.toml`)
- `--run-id` CLI override (useful for Airflow orchestration and reproducible runs)
- Config paths resolve **relative to the TOML file** location (portable configs)
- JSON validation report (auditable + debug-friendly)
- Parquet output when `pyarrow` is installed
- Dockerized ETL service + local Airflow (webserver + scheduler + Postgres)
- Airflow DAG triggers the ETL using `{{ ts_nodash }}` as a `run_id`

## Repository layout

```text
src/etl/
  __main__.py            # CLI entrypoint: python -m etl
  config.py              # TOML config loader
  ingest/                # CSV/JSON readers + record models
  validate/              # validation rules + report models
  transform/             # normalization into canonical schema
  load/                  # writer (parquet preferred) + run summary
  utils/logging.py       # logging setup

dags/
  modular_etl_pipeline_dag.py

data/
  raw/
  processed/

docker/
  Dockerfile.etl
  Dockerfile.airflow

docker-compose.yml
pipeline.toml
pipeline_bad.toml

Requirements

Python 3.12+

Docker + Docker Compose (for containerized runs / Airflow)

Optional (recommended): pyarrow (enables Parquet output)

Quickstart (local Python)
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install .

Run the pipeline:

python -m etl --config pipeline.toml --run-id manual --log-level INFO

Run with a failing config (expected to exit with code 2 when validation fails):

python -m etl --config pipeline_bad.toml --run-id bad-run --log-level INFO

Lint + tests:

ruff check .
pytest -q
Configuration

The pipeline reads a TOML file (e.g., pipeline.toml). Common knobs:

pipeline.name, pipeline.run_id

paths.raw_dir, paths.processed_dir, paths.reports_dir

sources.csv_files, sources.json_files

validation thresholds (allowed_sites, numeric ranges, etc.)

ingest parallelism (max_workers)

Note: relative paths in the config are resolved relative to the TOML file location.

Docker: run the ETL service
docker compose build etl
docker compose run --rm etl

Outputs land in data/processed/ on the host (via bind mount).

Airflow (local via Docker Compose)
1) Configure credentials

Copy the example file and edit values:

cp .env.example .env

Example .env.example:

# Copy to .env and adjust values (DO NOT COMMIT .env)
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
_AIRFLOW_WWW_USER_FIRSTNAME=Airflow
_AIRFLOW_WWW_USER_LASTNAME=Admin
_AIRFLOW_WWW_USER_ROLE=Admin
_AIRFLOW_WWW_USER_EMAIL=airflow@example.com

# Match host user id so mounted volumes aren't owned by root
AIRFLOW_UID=50000

Valid roles include: Admin, User, Viewer, Op, Public.

2) Start Airflow
docker compose build
docker compose up airflow-init
docker compose up -d postgres airflow-webserver airflow-scheduler
docker compose ps

Open the UI: http://localhost:8080

Log in with the credentials from .env.

3) Trigger the DAG
docker compose exec airflow-webserver airflow dags list | grep modular_etl_pipeline
docker compose exec airflow-webserver airflow dags unpause modular_etl_pipeline
docker compose exec airflow-webserver airflow dags trigger modular_etl_pipeline

Each run writes outputs to data/processed/ with run_id={{ ts_nodash }}.

format this to a readme.md file..

Here’s a polished and structured `README.md` version of your detailed description. It’s formatted for clarity and ready to include in your repository’s root.

***

# Modular ETL Pipeline (Python · Docker · Airflow)

A **production-style modular ETL pipeline** built for local or containerized runs. It ingests CSV/JSON observation data, validates it with **config-driven rules**, normalizes it into a consistent schema, and outputs **curated datasets** (Parquet preferred).  
The project also includes a **Docker Compose** stack with **Airflow orchestration** for scheduled runs.

***

## 📦 Overview

**Inputs:**  
`data/raw/` — accepts both **CSV** and **JSON** sources.

**Pipeline stages:**
1. **Ingest** — Reads CSV/JSON sources (optionally in parallel).
2. **Validate** — Performs rule-based checks driven by `pipeline.toml`.
3. **Transform** — Normalizes heterogeneous data into a canonical schema.
4. **Load** — Writes curated datasets (Parquet if `pyarrow` is available, otherwise CSV) and detailed JSON reports.

**Outputs:**  
`data/processed/`
- `validation_report_<run_id>.json`
- `observations_cleaned_<run_id>.parquet` (preferred) or `.csv`
- `run_summary_<run_id>.json`

***

## ⚙️ Key Features

- Modular packaging under `src/etl/`
- Config-driven workflow (via `pipeline.toml`)
- `--run-id` CLI override for reproducible or Airflow-triggered runs
- Relative config paths (portable between environments)
- JSON validation reports for auditing and debugging
- Automatic Parquet output when `pyarrow` is available
- Dockerized ETL service
- Local Airflow with webserver, scheduler, and Postgres
- Airflow DAG using `{{ ts_nodash }}` as runtime identifier (`run_id`)

***

## 🗂️ Repository Layout

```text
src/etl/
  __main__.py            # CLI entrypoint: python -m etl
  config.py              # TOML config loader
  ingest/                # CSV/JSON readers + record models
  validate/              # Validation rules + report models
  transform/             # Normalization into canonical schema
  load/                  # Writer (Parquet preferred) + run summary
  utils/logging.py       # Logging setup

dags/
  modular_etl_pipeline_dag.py

data/
  raw/
  processed/

docker/
  Dockerfile.etl
  Dockerfile.airflow

docker-compose.yml
pipeline.toml
pipeline_bad.toml
```

***

## 🧰 Requirements

- **Python 3.12+**
- **Docker + Docker Compose** (for containerized/Airflow deployment)
- Optional but recommended: **pyarrow** for Parquet output

***

## 🚀 Quickstart (Local Python)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install .
```

### Run the pipeline
```bash
python -m etl --config pipeline.toml --run-id manual --log-level INFO
```

### Run with a failing config (expect exit code 2)
```bash
python -m etl --config pipeline_bad.toml --run-id bad-run --log-level INFO
```

### Lint & tests
```bash
ruff check .
pytest -q
```

***

## ⚙️ Configuration (`pipeline.toml`)

Define all pipeline settings in a TOML file (example: `pipeline.toml`).

**Common keys:**

- `pipeline.name`, `pipeline.run_id`
- `paths.raw_dir`, `paths.processed_dir`, `paths.reports_dir`
- `sources.csv_files`, `sources.json_files`
- Validation thresholds (allowed sites, numeric ranges, etc.)
- Ingest parallelism (`max_workers`)

> Note: Relative paths in the config resolve relative to the TOML file location (portable configs).

***

## 🐳 Dockerized ETL Service

Build and run locally:

```bash
docker compose build etl
docker compose run --rm etl
```

Processed outputs appear in `data/processed/` on the host (via bind mount).

***

## 🪶 Airflow (Local via Docker Compose)

### 1) Configure credentials

```bash
cp .env.example .env
```

**Example `.env.example`:**

```bash
# Airflow UI user
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
_AIRFLOW_WWW_USER_FIRSTNAME=Airflow
_AIRFLOW_WWW_USER_LASTNAME=Admin
_AIRFLOW_WWW_USER_ROLE=Admin
_AIRFLOW_WWW_USER_EMAIL=airflow@example.com

# Match host UID to avoid root-owned mounts
AIRFLOW_UID=50000
```

Valid roles: `Admin`, `User`, `Viewer`, `Op`, `Public`.

***

### 2) Start Airflow

```bash
docker compose build
docker compose up airflow-init
docker compose up -d postgres airflow-webserver airflow-scheduler
docker compose ps
```

Open the Airflow UI at:  
👉 [http://localhost:8080](http://localhost:8080)

Login using credentials from `.env`.

***

### 3) Trigger the DAG

```bash
docker compose exec airflow-webserver airflow dags list | grep modular_etl_pipeline
docker compose exec airflow-webserver airflow dags unpause modular_etl_pipeline
docker compose exec airflow-webserver airflow dags trigger modular_etl_pipeline
```

Each run writes outputs to `data/processed/`  
with `run_id = {{ ts_nodash }}`.

***
