from __future__ import annotations

import csv
import json
import logging
from collections import Counter
from pathlib import Path

from etl.config import PipelineConfig
from etl.transform.normalize import COLUMNS

logger = logging.getLogger("etl.load")


def write_outputs(cfg: PipelineConfig, rows: list[dict[str, object]]) -> tuple[Path, Path]:
    cfg.processed_dir.mkdir(parents=True, exist_ok=True)
    cfg.reports_dir.mkdir(parents=True, exist_ok=True)

    base = f"{cfg.output_basename}_{cfg.run_id}"
    desired = cfg.output_format.lower().strip()

    summary_file = cfg.reports_dir / f"run_summary_{cfg.run_id}.json"

    if desired == "parquet":
        parquet_path = cfg.processed_dir / f"{base}.parquet"
        data_path = _try_write_parquet(parquet_path, rows)
        summary_path = _write_summary(summary_file, cfg, rows, data_path)
        return data_path, summary_path

    # explicit CSV
    data_path = cfg.processed_dir / f"{base}.csv"
    _write_csv(data_path, rows)
    summary_path = _write_summary(summary_file, cfg, rows, data_path)
    return data_path, summary_path


def _try_write_parquet(path: Path, rows: list[dict[str, object]]) -> Path:
    try:
        import pandas as pd  # optional dependency

        df = pd.DataFrame(rows, columns=COLUMNS)
        df.to_parquet(path, index=False)
        logger.info("Wrote parquet: %s", path)
        return path
    except Exception as e:
        logger.warning("Parquet write failed (%s). Falling back to CSV.", e)

    fallback = path.with_suffix(".csv")
    _write_csv(fallback, rows)
    logger.info("Wrote csv fallback: %s", fallback)
    return fallback


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _write_summary(
    path: Path,
    cfg: PipelineConfig,
    rows: list[dict[str, object]],
    data_path: Path,
) -> Path:
    fmt_counts = Counter(r["source_format"] for r in rows)

    payload = {
        "pipeline": {"name": cfg.name, "run_id": cfg.run_id},
        "output": {"path": str(data_path), "format": data_path.suffix.lstrip(".")},
        "counts": {"rows": len(rows), "by_source_format": dict(fmt_counts)},
        "columns": COLUMNS,
    }

    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.info("Wrote run summary: %s", path)
    return path
