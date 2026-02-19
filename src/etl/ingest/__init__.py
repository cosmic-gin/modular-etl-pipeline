from __future__ import annotations

from etl.config import PipelineConfig
from etl.ingest.csv_reader import read_observations_csv
from etl.ingest.json_reader import read_observations_json
from etl.ingest.models import ObservationRecord


def ingest_all(cfg: PipelineConfig) -> list[ObservationRecord]:
    records: list[ObservationRecord] = []

    for p in cfg.csv_files:
        records.extend(read_observations_csv(p))

    for p in cfg.json_files:
        records.extend(read_observations_json(p))

    return records
