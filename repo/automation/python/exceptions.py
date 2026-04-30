class SyncError(Exception):
    """Base synchronization error."""


class ConfigError(SyncError):
    """Configuration loading or validation error."""


class S3Error(SyncError):
    """S3 operation error."""


class GitError(SyncError):
    """Git operation error."""


class GitHubError(SyncError):
    """GitHub API operation error."""
