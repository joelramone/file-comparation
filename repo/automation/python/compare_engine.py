from __future__ import annotations

from pathlib import Path

from .hash_utils import sha256_bytes, sha256_file
from .models import FileComparison, FileStatus, MappingConfig
from .s3_client import S3Client


class CompareEngine:
    def __init__(self, s3_client: S3Client, mapping: MappingConfig) -> None:
        self.s3_client = s3_client
        self.mapping = mapping

    def compare_release(self, release: str, repo_root: Path) -> list[FileComparison]:
        results: list[FileComparison] = []
        for mapping_item in self.mapping.mappings:
            s3_data = self.s3_client.download_text(release, mapping_item.s3)
            s3_hash = sha256_bytes(s3_data)
            repo_file = repo_root / mapping_item.repo
            if not repo_file.exists():
                results.append(FileComparison(s3_file=mapping_item.s3, repo_file=mapping_item.repo, s3_hash=s3_hash, status=FileStatus.ADDED))
                continue
            repo_hash = sha256_file(repo_file)
            status = FileStatus.UNCHANGED if repo_hash == s3_hash else FileStatus.MODIFIED
            results.append(FileComparison(s3_file=mapping_item.s3, repo_file=mapping_item.repo, s3_hash=s3_hash, repo_hash=repo_hash, status=status))
        return results
