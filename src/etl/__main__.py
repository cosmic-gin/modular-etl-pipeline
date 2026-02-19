from __future__ import annotations

import argparse
import logging
from pathlib import Path

from etl.config import load_config
from etl.ingest import ingest_all
from etl.load import write_outputs
from etl.transform import normalize_records
from etl.utils.logging import setup_logging
from etl.validate import validate_records, write_validation_report

logger = logging.getLogger("etl")


def main() -> int:
    parser = argparse.ArgumentParser(description="Modular ETL pipeline (local entrypoint)")
    parser.add_argument("--config", default="pipeline.toml")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    setup_logging(args.log_level)
    cfg = load_config(Path(args.config))

    records = ingest_all(cfg)
    valid, issues = validate_records(cfg, records)

    logger.info(
        "Validation summary: total=%d valid=%d invalid=%d",
        len(records),
        len(valid),
        len(records) - len(valid),
    )

    validation_report_path = cfg.reports_dir / f"validation_report_{cfg.run_id}.json"
    write_validation_report(validation_report_path, cfg, len(records), len(valid), issues)
    logger.info("Wrote validation report: %s", validation_report_path)

    if issues:
        logger.error("Validation failed with %d issues", len(issues))
        return 2

    rows = normalize_records(valid)
    data_path, summary_path = write_outputs(cfg, rows)

    logger.info("Wrote processed data: %s", data_path)
    logger.info("Wrote run summary: %s", summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
