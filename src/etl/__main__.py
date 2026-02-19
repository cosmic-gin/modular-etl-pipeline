from __future__ import annotations

import argparse
import logging
from pathlib import Path

from etl.config import load_config
from etl.ingest import ingest_all
from etl.utils.logging import setup_logging

logger = logging.getLogger("etl")


def main() -> int:
    parser = argparse.ArgumentParser(description="Modular ETL pipeline (local entrypoint)")
    parser.add_argument("--config", default="pipeline.toml")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    setup_logging(args.log_level)
    cfg = load_config(Path(args.config))

    records = ingest_all(cfg)
    logger.info("Ingested %d records", len(records))
    logger.info("First record: %s", records[0] if records else None)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
