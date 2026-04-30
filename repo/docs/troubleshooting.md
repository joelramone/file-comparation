# Troubleshooting

## Common issues

### Missing AWS credentials
Ensure Jenkins injects `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

### Missing GitHub token
Set `GITHUB_TOKEN` in pipeline credentials and ensure `repo` scope.

### No changes detected
If all hashes match, no commit or PR is created.

### Invalid mapping path
Check `automation/config/mapping.yaml` paths target `k8s/helm/`.

### Branch push denied
Validate token permissions for branch creation and push policies.
