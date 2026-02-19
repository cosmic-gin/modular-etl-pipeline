from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ValidationIssue:
    record_id: int
    source_file: str
    source_format: str
    field: str
    message: str

    def to_dict(self) -> dict:
        return asdict(self)
