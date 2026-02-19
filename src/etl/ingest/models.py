from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


def parse_timestamp(value: str) -> datetime:
    """
    Parse ISO-8601 timestamp strings like:
    - 2026-02-18T10:00:00Z
    - 2026-02-18T10:00:00+00:00
    """
    s = value.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


@dataclass(frozen=True)
class ObservationRecord:
    id: int
    timestamp: datetime
    site: str
    metrics: dict[str, float]
    source_file: str
    source_format: str  # "csv" or "json"
