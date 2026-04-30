"""Manifest generation."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from .models import CompareResult, Manifest


def write_manifest(compare_result: CompareResult, source_prefix: str, output_path: Path) -> Path:
    manifest = Manifest(
        release=compare_result.release,
        source_prefix=source_prefix,
        generated_at=datetime.now(UTC).isoformat(),
        records=compare_result.records,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest.model_dump(mode="json"), indent=2), encoding="utf-8")
    return output_path
