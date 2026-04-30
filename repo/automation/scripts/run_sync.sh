#!/usr/bin/env bash
set -euo pipefail

: "${RELEASE_VERSION:?RELEASE_VERSION is required}"
: "${S3_BUCKET:?S3_BUCKET is required}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

python3 -m automation.python.sync_engine \
  --release "${RELEASE_VERSION}" \
  --bucket "${S3_BUCKET}" \
  --base-prefix "${S3_BASE_PREFIX:-elipse-releases}" \
  --repo-root "${REPO_ROOT}" \
  --mapping "automation/config/mapping.yaml" \
  ${DRY_RUN:+--dry-run}
