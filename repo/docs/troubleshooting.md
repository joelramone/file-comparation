# Troubleshooting

## Missing AWS credentials
Ensure Jenkins or runtime has `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and region.

## GitHub authentication failures
Set `GITHUB_TOKEN` with repository write and pull request permissions.

## No changes detected
Validate `mapping.yaml` paths and verify S3 release content exists.

## Branch already exists
The pipeline recreates branch using `git checkout -B`; ensure remote permissions allow force updates.
