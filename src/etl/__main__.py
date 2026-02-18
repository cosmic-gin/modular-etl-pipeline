from __future__ import annotations

import argparse
import logging
from pathlib import Path

from etl.config import load_config
from etl.utils.logging import setup_logging

logger = logging.getLogger("etl")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Modular ETL pipeline (local entrypoint)"
    )
    parser.add_argument("--config", default="pipeline.toml")
    parser.add_argument("--log-level", default="INFO")

    args = parser.parse_args()

    setup_logging(args.log_level)

    cfg = load_config(Path(args.config))

    logger.info("Loaded config: name=%s output_format=%s", cfg.name, cfg.output_format)
    logger.info("CSV sources: %s", cfg.csv_files)
    logger.info("JSON sources: %s", cfg.json_files)
    logger.info("Step 2 complete: entrypoint + config + logging are working.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
