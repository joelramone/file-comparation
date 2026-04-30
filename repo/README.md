# Vendor Config Sync Automation

Enterprise-grade starter for synchronizing vendor configuration files from AWS S3 into a GitHub repository.

## Features

- Python 3.12 sync engine
- SHA256 deterministic comparison
- Strong typing with Pydantic models
- JSON structured logs
- Dry-run mode
- Release manifest generation
- Jenkins pipeline for branch, commit, push, and PR automation

## Project Structure

See `docs/architecture.md` for full component breakdown.

## Quick Start

```bash
cd repo
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r automation/python/requirements.txt
python3 -m automation.python.sync_engine --release 10.11.0 --bucket your-bucket --repo-root . --dry-run
```

## Tests

```bash
pytest -q
```
