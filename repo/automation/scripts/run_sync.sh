#!/usr/bin/env bash
set -euo pipefail

RELEASE="${1:?usage: run_sync.sh <release> [--dry-run]}"
DRY_RUN="${2:-}"

python -m automation.python.sync_engine \
  --release "${RELEASE}" \
  --settings automation/config/settings.yaml \
  --mapping automation/config/mapping.yaml \
  ${DRY_RUN}
