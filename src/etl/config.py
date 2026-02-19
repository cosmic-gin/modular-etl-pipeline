from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    name: str
    run_id: str

    raw_dir: Path
    processed_dir: Path
    reports_dir: Path

    csv_files: list[Path]
    json_files: list[Path]

    max_workers: int

    allowed_sites: list[str]
    temp_c_min: float
    temp_c_max: float
    humidity_min: float
    humidity_max: float

    output_format: str
    output_basename: str


def load_config(path: Path) -> PipelineConfig:
    with path.open("rb") as f:
        data = tomllib.load(f)

    base_dir = path.parent.resolve()

    def _resolve(p: str) -> Path:
        pp = Path(p)
        return pp if pp.is_absolute() else (base_dir / pp).resolve()

    v = data["validation"]
    out = data["output"]

    rt = data.get("runtime", {})
    max_workers = int(rt.get("max_workers", 1))

    return PipelineConfig(
        name=data["pipeline"]["name"],
        run_id=data["pipeline"]["run_id"],
        raw_dir=_resolve(data["paths"]["raw_dir"]),
        processed_dir=_resolve(data["paths"]["processed_dir"]),
        reports_dir=_resolve(data["paths"]["reports_dir"]),
        csv_files=[_resolve(p) for p in data["sources"]["csv_files"]],
        json_files=[_resolve(p) for p in data["sources"]["json_files"]],
        max_workers=max_workers,
        allowed_sites=list(v["allowed_sites"]),
        temp_c_min=float(v["temp_c_min"]),
        temp_c_max=float(v["temp_c_max"]),
        humidity_min=float(v["humidity_min"]),
        humidity_max=float(v["humidity_max"]),
        output_format=str(out["format"]),
        output_basename=str(out["output_basename"]),
    )
