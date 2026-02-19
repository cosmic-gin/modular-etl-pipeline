from pathlib import Path

from etl.config import load_config
from etl.ingest import ingest_all
from etl.transform import COLUMNS, normalize_records
from etl.validate import validate_records


def test_normalize_records_has_expected_columns():
    cfg = load_config(Path("pipeline.toml"))
    records = ingest_all(cfg)
    valid, issues = validate_records(cfg, records)
    assert issues == []

    rows = normalize_records(valid)
    assert len(rows) == 4
    assert list(rows[0].keys()) == COLUMNS
