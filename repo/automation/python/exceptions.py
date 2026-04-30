class SyncError(Exception):
    """Base exception for synchronization failures."""


class ConfigurationError(SyncError):
    """Raised when settings or mappings are invalid."""


class S3ReleaseNotFoundError(SyncError):
    """Raised when release data is missing in S3."""


class GitOperationError(SyncError):
    """Raised when a git operation fails."""


class GitHubAPIError(SyncError):
    """Raised when GitHub API request fails."""
