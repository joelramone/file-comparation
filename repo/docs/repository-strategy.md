# Repository Strategy

This repository is automation-only and intentionally excludes application `k8s/helm` files.

- Target repository URL, branch, and clone path are runtime configuration.
- File-level source and destination mappings are declarative in `mapping.yaml`.
- Multi-repository support is enabled by extending settings and iterating mappings per target repository.
