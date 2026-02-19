from __future__ import annotations

import json
from pathlib import Path

from etl.ingest.models import ObservationRecord, parse_timestamp


def read_observations_json(path: Path) -> list[ObservationRecord]:
    raw = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(raw, list):
        raise ValueError(f"Expected a JSON list in {path}, got {type(raw).__name__}")

    records: list[ObservationRecord] = []
    for item in raw:
        record = ObservationRecord(
            id=int(item["id"]),
            timestamp=parse_timestamp(str(item["timestamp"])),
            site=str(item["site"]),
            metrics={"humidity": float(item["humidity"])},
            source_file=str(path),
            source_format="json",
        )
        records.append(record)

    return records
