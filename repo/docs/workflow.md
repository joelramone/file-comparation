# Workflow

1. Validate release input (`X.Y.Z`).
2. Load settings and mapping YAML.
3. Clone/open target application repository.
4. Checkout base branch and create `upgrade/<release>`.
5. Download mapped files from S3 release path.
6. Compare source and destination files by SHA256.
7. Copy only changed files into `k8s/helm/` in the external repo.
8. Generate manifest under `.sync/<release>.json`.
9. Commit and push branch when changes exist.
10. Open pull request in GitHub.
