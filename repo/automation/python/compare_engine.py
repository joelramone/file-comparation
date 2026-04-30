from __future__ import annotations

from pathlib import Path

from .hash_utils import sha256_bytes, sha256_file
from .models import FileDiff, FileMapping, FileStatus


def compare_files(source_name: str, source_content: bytes, destination_path: Path) -> FileDiff:
    source_hash = sha256_bytes(source_content)
    if not destination_path.exists():
        return FileDiff(
            source=source_name,
            destination=destination_path,
            status=FileStatus.ADDED,
            source_sha256=source_hash,
            destination_sha256=None,
        )

    destination_hash = sha256_file(destination_path)
    status = FileStatus.UNCHANGED if destination_hash == source_hash else FileStatus.MODIFIED
    return FileDiff(
        source=source_name,
        destination=destination_path,
        status=status,
        source_sha256=source_hash,
        destination_sha256=destination_hash,
    )


def compare_release(source_files: dict[str, bytes], mappings: list[FileMapping], repo_root: Path) -> list[FileDiff]:
    diffs: list[FileDiff] = []
    for mapping in mappings:
        destination = repo_root / mapping.repo
        source = source_files[mapping.s3]
        diffs.append(compare_files(mapping.s3, source, destination))
    return sorted(diffs, key=lambda d: d.source)
