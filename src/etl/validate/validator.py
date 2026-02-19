from __future__ import annotations

import json
from pathlib import Path

from etl.config import PipelineConfig
from etl.ingest.models import ObservationRecord
from etl.validate.models import ValidationIssue


def validate_records(
    cfg: PipelineConfig, records: list[ObservationRecord]
) -> tuple[list[ObservationRecord], list[ValidationIssue]]:
    valid: list[ObservationRecord] = []
    issues: list[ValidationIssue] = []

    for r in records:
        record_issues: list[ValidationIssue] = []

        # Common rules
        if r.id <= 0:
            record_issues.append(_issue(r, "id", "must be > 0"))

        if not r.site:
            record_issues.append(_issue(r, "site", "must be non-empty"))
        elif r.site not in cfg.allowed_sites:
            record_issues.append(_issue(r, "site", f"must be one of {cfg.allowed_sites}"))

        # Source-specific metric rules
        if r.source_format == "csv":
            record_issues.extend(_check_range(r, "temp_c", cfg.temp_c_min, cfg.temp_c_max))
        elif r.source_format == "json":
            record_issues.extend(
                _check_range(r, "humidity", cfg.humidity_min, cfg.humidity_max)
            )
        else:
            record_issues.append(_issue(r, "source_format", "unknown source_format"))

        if record_issues:
            issues.extend(record_issues)
        else:
            valid.append(r)

    return valid, issues


def write_validation_report(
    path: Path,
    cfg: PipelineConfig,
    total_records: int,
    valid_records: int,
    issues: list[ValidationIssue],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "pipeline": {"name": cfg.name, "run_id": cfg.run_id},
        "counts": {
            "total": total_records,
            "valid": valid_records,
            "invalid": total_records - valid_records,
        },
        "issues": [i.to_dict() for i in issues],
    }

    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _issue(r: ObservationRecord, field: str, message: str) -> ValidationIssue:
    return ValidationIssue(
        record_id=r.id,
        source_file=r.source_file,
        source_format=r.source_format,
        field=field,
        message=message,
    )


def _check_range(
    r: ObservationRecord, key: str, min_v: float, max_v: float
) -> list[ValidationIssue]:
    if key not in r.metrics:
        return [_issue(r, f"metrics.{key}", "is required")]

    value = r.metrics[key]
    if not (min_v <= value <= max_v):
        return [_issue(r, f"metrics.{key}", f"must be between {min_v} and {max_v}")]
    return []
