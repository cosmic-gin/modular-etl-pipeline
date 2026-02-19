from pathlib import Path

from etl.config import load_config
from etl.ingest import ingest_all


def test_ingest_all_smoke():
    cfg = load_config(Path("pipeline.toml"))
    records = ingest_all(cfg)

    assert len(records) == 4
    assert {r.source_format for r in records} == {"csv", "json"}
    assert all(r.site for r in records)
    assert all(r.metrics for r in records)
