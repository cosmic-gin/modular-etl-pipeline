from pathlib import Path

from etl.config import load_config


def test_load_config_smoke():
    cfg = load_config(Path("pipeline.toml"))
    assert cfg.name
    assert cfg.csv_files
    assert cfg.json_files
