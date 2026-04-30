from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class FileStatus(str, Enum):
    ADDED = "added"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"
    REMOVED = "removed"


class GitHubConfig(BaseModel):
    repository_url: HttpUrl
    base_branch: str = "main"


class S3Config(BaseModel):
    bucket: str
    release_prefix: str


class WorkspaceConfig(BaseModel):
    clone_dir: Path


class Settings(BaseModel):
    github: GitHubConfig
    s3: S3Config
    workspace: WorkspaceConfig


class FileMapping(BaseModel):
    s3: str
    repo: Path


class MappingConfig(BaseModel):
    mappings: list[FileMapping]


class FileHash(BaseModel):
    path: Path
    sha256: str


class FileDiff(BaseModel):
    source: str
    destination: Path
    status: FileStatus
    source_sha256: str
    destination_sha256: str | None = None


class ReleaseManifest(BaseModel):
    release: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    changes: list[FileDiff]


class SyncResult(BaseModel):
    release: str
    branch: str
    changed_files: list[Path]
    pr_url: str | None = None
    dry_run: bool = False


class LogEvent(BaseModel):
    event: str
    release: str | None = None
    file: str | None = None
    status: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)
