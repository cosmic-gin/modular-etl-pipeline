from __future__ import annotations

from etl.ingest.models import ObservationRecord

COLUMNS = [
    "id",
    "timestamp",
    "site",
    "temp_c",
    "humidity",
    "source_file",
    "source_format",
]


def normalize_records(records: list[ObservationRecord]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for r in records:
        rows.append(
            {
                "id": r.id,
                "timestamp": r.timestamp.isoformat(),
                "site": r.site,
                "temp_c": r.metrics.get("temp_c"),
                "humidity": r.metrics.get("humidity"),
                "source_file": r.source_file,
                "source_format": r.source_format,
            }
        )

    return rows
