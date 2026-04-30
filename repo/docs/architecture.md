# Architecture

This repository provides a modular automation service to synchronize vendor configuration from S3 into an external application repository.

## Modules
- `sync_engine.py`: orchestration entrypoint.
- `s3_client.py`: release discovery and file download from S3.
- `compare_engine.py`: deterministic hash-based comparison.
- `git_manager.py`: clone, branch, commit, and push operations.
- `github_client.py`: pull request creation via GitHub REST API.
- `manifest.py`: release manifest generation.
- `logger.py`: structured JSON logging.

## Boundaries
The automation repository does not include application files. Application content is only modified inside cloned external repositories.
