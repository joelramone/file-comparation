# Vendor Config Sync Automation

Enterprise-grade automation system for synchronizing vendor configuration files from AWS S3 into an external application repository in GitHub.

## Runtime

- Python 3.12
- Jenkins pipeline
- AWS S3 + GitHub API

## Quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r automation/python/requirements.txt
./automation/scripts/run_sync.sh 10.11.0 --dry-run
```

## Configuration

- `automation/config/settings.yaml`: repository, S3, workspace.
- `automation/config/mapping.yaml`: source-to-destination mapping.

## Testing

```bash
PYTHONPATH=. pytest -q
```

## CI/CD

Use `automation/jenkins/Jenkinsfile` with Jenkins credentials:

- `github-token`
- `aws-access-key-id`
- `aws-secret-access-key`
