# Workflow

## Local execution

```bash
python3 -m pip install -r automation/python/requirements.txt
python3 -m automation.python.sync_engine \
  --release 10.11.0 \
  --bucket your-bucket \
  --repo-root .
```

## Dry-run execution

```bash
python3 -m automation.python.sync_engine \
  --release 10.11.0 \
  --bucket your-bucket \
  --repo-root . \
  --dry-run
```

## CI pipeline execution

Use `automation/jenkins/Jenkinsfile` with required credentials:
- `vendor-s3-bucket-name`
- `github-token`
