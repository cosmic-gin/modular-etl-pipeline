from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from etl.config import PipelineConfig
from etl.ingest.csv_reader import read_observations_csv
from etl.ingest.json_reader import read_observations_json
from etl.ingest.models import ObservationRecord

logger = logging.getLogger("etl.ingest")


def ingest_all(cfg: PipelineConfig) -> list[ObservationRecord]:
    """
    Read all configured sources.
    Uses threads for I/O-bound parallelism when cfg.max_workers > 1.
    Output order is deterministic: CSV files in listed order, then JSON files in listed order.
    """
    if cfg.max_workers <= 1:
        return _ingest_sequential(cfg)

    records: list[ObservationRecord] = []
    csv_paths = list(cfg.csv_files)
    json_paths = list(cfg.json_files)

    with ThreadPoolExecutor(max_workers=cfg.max_workers) as ex:
        csv_futures = {p: ex.submit(read_observations_csv, p) for p in csv_paths}
        json_futures = {p: ex.submit(read_observations_json, p) for p in json_paths}

        # preserve order
        for p in csv_paths:
            records.extend(_result_or_raise(p, csv_futures[p]))

        for p in json_paths:
            records.extend(_result_or_raise(p, json_futures[p]))

    return records


def _ingest_sequential(cfg: PipelineConfig) -> list[ObservationRecord]:
    records: list[ObservationRecord] = []
    for p in cfg.csv_files:
        records.extend(read_observations_csv(p))
    for p in cfg.json_files:
        records.extend(read_observations_json(p))
    return records


def _result_or_raise(path: Path, future) -> list[ObservationRecord]:
    try:
        return future.result()
    except Exception:
        logger.exception("Failed to ingest file: %s", path)
        raise
