from __future__ import annotations

from dataclasses import dataclass

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from .exceptions import S3Error


@dataclass
class S3Client:
    bucket: str
    release_prefix: str

    def __post_init__(self) -> None:
        self._client = boto3.client("s3")

    def object_key(self, release: str, filename: str) -> str:
        return f"{self.release_prefix}/{release}/config/{filename}"

    def download_text(self, release: str, filename: str) -> bytes:
        key = self.object_key(release, filename)
        try:
            response = self._client.get_object(Bucket=self.bucket, Key=key)
            return response["Body"].read()
        except (ClientError, BotoCoreError) as exc:
            raise S3Error(f"Failed downloading s3://{self.bucket}/{key}") from exc

    def list_releases(self) -> list[str]:
        prefix = f"{self.release_prefix}/"
        try:
            response = self._client.list_objects_v2(Bucket=self.bucket, Prefix=prefix, Delimiter="/")
        except (ClientError, BotoCoreError) as exc:
            raise S3Error("Failed listing release versions") from exc
        releases: list[str] = []
        for item in response.get("CommonPrefixes", []):
            value = item["Prefix"].removeprefix(prefix).strip("/")
            if value:
                releases.append(value)
        return sorted(releases)
