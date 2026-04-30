# Workflow

1. Validate release version.
2. Clone external repository into `workspace.clone_dir`.
3. Checkout base branch and create `upgrade/<release>` branch.
4. Download mapped S3 files from `s3://<bucket>/<release_prefix>/<release>/config/`.
5. Compare hashes against target files in cloned repository.
6. Write changed files.
7. Commit and push branch.
8. Create pull request.
9. Persist `sync-manifest.json`.
