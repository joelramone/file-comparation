"""Custom exceptions for synchronization workflow."""


class SyncError(Exception):
    """Base exception for sync workflow."""


class S3ReleaseNotFoundError(SyncError):
    """Raised when a release prefix or files do not exist in S3."""


class MappingValidationError(SyncError):
    """Raised when mapping configuration is invalid."""


class GitOperationError(SyncError):
    """Raised when a git operation fails."""
