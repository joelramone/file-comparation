# Architecture

This repository is an automation control plane focused on synchronizing vendor configuration files from S3 into an external application repository.

## Components

- `automation/python/config_loader.py`: loads and validates YAML config through Pydantic.
- `automation/python/s3_client.py`: fetches release artifacts from `s3://bucket/elipse-releases/<release>/config/`.
- `automation/python/compare_engine.py`: deterministic file comparison using SHA256 hashes.
- `automation/python/git_manager.py`: branch, commit, and push orchestration using GitPython.
- `automation/python/github_client.py`: GitHub REST API PR automation.
- `automation/python/sync_engine.py`: end-to-end orchestration, manifest generation, and structured logs.

## Design Principles

- Stateless execution per release.
- Strong typing with Pydantic models.
- Config-driven mappings.
- Dry-run support for safe validation.
- JSON logs ready for SIEM ingestion.
