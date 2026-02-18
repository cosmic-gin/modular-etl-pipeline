from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    name: str
    raw_dir: Path
    processed_dir: Path
    reports_dir: Path
    csv_files: list[Path]
    json_files: list[Path]
    output_format: str


def load_config(path: Path) -> PipelineConfig:
    with path.open("rb") as f:
        data = tomllib.load(f)

    return PipelineConfig(
        name=data["pipeline"]["name"],
        raw_dir=Path(data["paths"]["raw_dir"]),
        processed_dir=Path(data["paths"]["processed_dir"]),
        reports_dir=Path(data["paths"]["reports_dir"]),
        csv_files=[Path(p) for p in data["sources"]["csv_files"]],
        json_files=[Path(p) for p in data["sources"]["json_files"]],
        output_format=data["output"]["format"],
    )
