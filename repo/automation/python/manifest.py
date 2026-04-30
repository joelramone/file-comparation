from __future__ import annotations

from pathlib import Path

from .models import ReleaseManifest


def write_manifest(path: Path, manifest: ReleaseManifest) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
