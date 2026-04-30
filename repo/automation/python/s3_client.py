"""S3 client wrapper."""

from __future__ import annotations

from pathlib import Path

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from .exceptions import S3ReleaseNotFoundError


class S3ReleaseClient:
    def __init__(self, bucket: str, base_prefix: str, client: BaseClient | None = None) -> None:
        self.bucket = bucket
        self.base_prefix = base_prefix.rstrip("/")
        self.client = client or boto3.client("s3")

    def release_prefix(self, release: str) -> str:
        return f"{self.base_prefix}/{release}/config"

    def file_key(self, release: str, filename: str) -> str:
        return f"{self.release_prefix(release)}/{filename}"

    def file_exists(self, release: str, filename: str) -> bool:
        key = self.file_key(release, filename)
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError as exc:
            if exc.response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 404:
                return False
            raise

    def download_file(self, release: str, filename: str, destination: Path) -> Path:
        key = self.file_key(release, filename)
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.client.download_file(self.bucket, key, str(destination))
        except ClientError as exc:
            if exc.response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 404:
                raise S3ReleaseNotFoundError(f"Missing S3 object: s3://{self.bucket}/{key}") from exc
            raise
        return destination
