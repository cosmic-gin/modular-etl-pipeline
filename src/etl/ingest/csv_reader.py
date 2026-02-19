from __future__ import annotations

import csv
from pathlib import Path

from etl.ingest.models import ObservationRecord, parse_timestamp


def read_observations_csv(path: Path) -> list[ObservationRecord]:
    records: list[ObservationRecord] = []

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = ObservationRecord(
                id=int(row["id"]),
                timestamp=parse_timestamp(row["timestamp"]),
                site=str(row["site"]),
                metrics={"temp_c": float(row["temp_c"])},
                source_file=str(path),
                source_format="csv",
            )
            records.append(record)

    return records
