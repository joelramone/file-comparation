# Architecture

The system is composed of modular components under `automation/python`:

- `s3_client.py`: AWS S3 abstraction for release file checks and downloads.
- `compare_engine.py`: deterministic comparison engine using SHA256 checksums.
- `sync_engine.py`: orchestration CLI for compare + synchronize + manifest.
- `manifest.py`: immutable JSON manifest generation for every run.
- `logger.py`: structured JSON logging.
- `models.py`: strongly typed Pydantic domain models.

## Data Flow

1. Jenkins triggers the process with a release version.
2. Sync engine loads `automation/config/mapping.yaml`.
3. Compare engine downloads mapped files from S3 into workspace.
4. Hashes are calculated and statuses are computed (`added|removed|modified|unchanged`).
5. On non-dry runs, changed files are copied into `k8s/helm`.
6. A manifest is written to `.automation-work/manifest.json`.
7. Jenkins commits, pushes, and opens a PR.
