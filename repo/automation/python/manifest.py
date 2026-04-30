from __future__ import annotations

import json
from pathlib import Path

from .models import FileComparison, Manifest


def build_manifest(release: str, dry_run: bool, comparisons: list[FileComparison]) -> Manifest:
    return Manifest(release=release, dry_run=dry_run, comparisons=comparisons)


def write_manifest(path: Path, manifest: Manifest) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
