from __future__ import annotations

from typing import Iterable

import boto3
from botocore.client import BaseClient

from .exceptions import S3ReleaseNotFoundError
from .models import S3Config


class S3ReleaseClient:
    def __init__(self, config: S3Config, client: BaseClient | None = None) -> None:
        self._config = config
        self._client = client or boto3.client("s3")

    def get_release_files(self, release: str, filenames: Iterable[str]) -> dict[str, bytes]:
        data: dict[str, bytes] = {}
        for name in filenames:
            key = f"{self._config.release_prefix}/{release}/config/{name}"
            try:
                response = self._client.get_object(Bucket=self._config.bucket, Key=key)
            except self._client.exceptions.NoSuchKey as exc:  # type: ignore[attr-defined]
                raise S3ReleaseNotFoundError(f"Missing S3 key: s3://{self._config.bucket}/{key}") from exc
            data[name] = response["Body"].read()
        return data
