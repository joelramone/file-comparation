from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class FileStatus(str, Enum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"


class MappingItem(BaseModel):
    s3: str
    repo: str


class MappingConfig(BaseModel):
    mappings: List[MappingItem]


class GitHubSettings(BaseModel):
    repository_url: HttpUrl
    base_branch: str = "main"


class S3Settings(BaseModel):
    bucket: str
    release_prefix: str


class WorkspaceSettings(BaseModel):
    clone_dir: str


class Settings(BaseModel):
    github: GitHubSettings
    s3: S3Settings
    workspace: WorkspaceSettings


class FileComparison(BaseModel):
    s3_file: str
    repo_file: str
    s3_hash: Optional[str] = None
    repo_hash: Optional[str] = None
    status: FileStatus


class Manifest(BaseModel):
    release: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    dry_run: bool = False
    comparisons: List[FileComparison]


class SyncResult(BaseModel):
    release: str
    branch: str
    dry_run: bool
    changed_files: List[FileComparison]
    pr_url: Optional[str] = None
