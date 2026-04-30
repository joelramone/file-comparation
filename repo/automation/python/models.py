"""Typed models for sync workflow."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FileStatus(StrEnum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"


class MappingEntry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    s3: str = Field(min_length=1)
    repo: Path


class FileRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    file: str
    repo_path: Path
    s3_hash: str | None = None
    repo_hash: str | None = None
    status: FileStatus


class CompareResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    release: str
    records: list[FileRecord]

    @property
    def changed(self) -> list[FileRecord]:
        return [r for r in self.records if r.status != FileStatus.UNCHANGED]

    def as_summary(self) -> dict[str, Any]:
        counts = {status.value: 0 for status in FileStatus}
        for record in self.records:
            counts[record.status.value] += 1
        return {
            "release": self.release,
            "total": len(self.records),
            "changed": len(self.changed),
            "counts": counts,
        }


class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    release: str
    source_prefix: str
    generated_at: str
    records: list[FileRecord]


class SyncReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    release: str
    dry_run: bool
    updated_files: list[Path]
    compare_summary: dict[str, Any]
