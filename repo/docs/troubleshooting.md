# Troubleshooting

## `mapping.yaml must contain top-level 'mappings'`
Ensure `automation/config/mapping.yaml` is valid YAML with the `mappings` key.

## Missing S3 object errors
Validate release path exists:
- `s3://<bucket>/elipse-releases/<release>/config/<filename>`

## No changes detected in Jenkins
Check if files in S3 and repository have identical SHA256 hash values.

## PR not created
Confirm `github-token` credential has `repo` scope and repository slug is correct.
