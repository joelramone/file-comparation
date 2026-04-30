"""Comparison engine between S3 release files and repository files."""

from __future__ import annotations

from pathlib import Path

from deepdiff import DeepDiff

from .hash_utils import sha256_file
from .models import CompareResult, FileRecord, FileStatus, MappingEntry
from .s3_client import S3ReleaseClient


class CompareEngine:
    def __init__(self, s3_client: S3ReleaseClient, workdir: Path) -> None:
        self.s3_client = s3_client
        self.workdir = workdir

    def compare(self, release: str, mappings: list[MappingEntry], repo_root: Path) -> CompareResult:
        records: list[FileRecord] = []
        download_root = self.workdir / release
        for mapping in mappings:
            s3_file = mapping.s3
            repo_path = repo_root / mapping.repo
            tmp_download = download_root / s3_file

            s3_exists = self.s3_client.file_exists(release, s3_file)
            repo_exists = repo_path.exists()

            if s3_exists:
                self.s3_client.download_file(release, s3_file, tmp_download)
                s3_hash = sha256_file(tmp_download)
            else:
                s3_hash = None

            repo_hash = sha256_file(repo_path) if repo_exists else None

            if s3_exists and not repo_exists:
                status = FileStatus.ADDED
            elif not s3_exists and repo_exists:
                status = FileStatus.REMOVED
            elif s3_hash and repo_hash:
                diff = DeepDiff({"h": s3_hash}, {"h": repo_hash}, ignore_order=True)
                status = FileStatus.MODIFIED if diff else FileStatus.UNCHANGED
            else:
                status = FileStatus.UNCHANGED

            records.append(
                FileRecord(
                    file=s3_file,
                    repo_path=mapping.repo,
                    s3_hash=s3_hash,
                    repo_hash=repo_hash,
                    status=status,
                )
            )
        return CompareResult(release=release, records=records)
