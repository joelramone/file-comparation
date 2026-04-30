# Vendor Config Sync Automation

Production-ready starter automation for synchronizing vendor configuration files from AWS S3 into external GitHub application repositories.

## Quick start

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r automation/python/requirements.txt
pytest -q
automation/scripts/run_sync.sh 10.11.0 --dry-run
```

## Configuration
- `automation/config/settings.yaml`
- `automation/config/mapping.yaml`

## Design constraints
- No application files are stored in this repository.
- External application repository is cloned dynamically at runtime.
