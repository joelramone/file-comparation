"""Main synchronization engine CLI."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml

from .compare_engine import CompareEngine
from .exceptions import MappingValidationError
from .logger import get_logger
from .manifest import write_manifest
from .models import MappingEntry, SyncReport
from .s3_client import S3ReleaseClient

LOGGER = get_logger("sync_engine")


def load_mappings(path: Path) -> list[MappingEntry]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "mappings" not in data:
        raise MappingValidationError("mapping.yaml must contain top-level 'mappings'")
    return [MappingEntry.model_validate(item) for item in data["mappings"]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synchronize vendor release files from S3 into repo")
    parser.add_argument("--release", required=True)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--base-prefix", default="elipse-releases")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--mapping", default="automation/config/mapping.yaml")
    parser.add_argument("--workspace", default=".automation-work")
    parser.add_argument("--manifest", default=".automation-work/manifest.json")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def synchronize(compare: CompareEngine, mappings: list[MappingEntry], release: str, repo_root: Path, dry_run: bool) -> SyncReport:
    result = compare.compare(release=release, mappings=mappings, repo_root=repo_root)
    updated_files: list[Path] = []

    for record in result.changed:
        LOGGER.info({"release": release, "file": record.file, "status": record.status.value})
        src = compare.workdir / release / record.file
        dst = repo_root / record.repo_path

        if dry_run:
            continue

        if record.status.value == "removed":
            if dst.exists():
                dst.unlink()
                updated_files.append(record.repo_path)
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        updated_files.append(record.repo_path)

    return SyncReport(
        release=release,
        dry_run=dry_run,
        updated_files=updated_files,
        compare_summary=result.as_summary(),
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    workspace = (repo_root / args.workspace).resolve()
    mapping_path = (repo_root / args.mapping).resolve()

    try:
        mappings = load_mappings(mapping_path)
        s3_client = S3ReleaseClient(bucket=args.bucket, base_prefix=args.base_prefix)
        compare = CompareEngine(s3_client=s3_client, workdir=workspace)

        report = synchronize(compare, mappings, args.release, repo_root, args.dry_run)
        manifest_path = write_manifest(
            compare.compare(args.release, mappings, repo_root),
            source_prefix=f"s3://{args.bucket}/{args.base_prefix}/{args.release}/config",
            output_path=repo_root / args.manifest,
        )

        LOGGER.info({"event": "sync_completed", **report.model_dump(mode="json"), "manifest": str(manifest_path)})
        print(json.dumps(report.model_dump(mode="json")))
        return 0
    except Exception as exc:  # noqa: BLE001
        LOGGER.error({"event": "sync_failed", "error": str(exc)})
        return 1


if __name__ == "__main__":
    sys.exit(main())
