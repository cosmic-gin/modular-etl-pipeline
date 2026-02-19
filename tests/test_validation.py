from pathlib import Path

from etl.config import load_config
from etl.ingest import ingest_all
from etl.validate import validate_records


def test_validation_good_config_all_valid():
    cfg = load_config(Path("pipeline.toml"))
    records = ingest_all(cfg)
    valid, issues = validate_records(cfg, records)

    assert len(records) == 4
    assert len(valid) == 4
    assert issues == []


def test_validation_bad_config_has_issues():
    cfg = load_config(Path("pipeline_bad.toml"))
    records = ingest_all(cfg)
    valid, issues = validate_records(cfg, records)

    assert len(records) == 4
    assert len(valid) < 4
    assert len(issues) >= 2
