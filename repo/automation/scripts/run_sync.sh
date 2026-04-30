#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

RELEASE_VERSION="${1:-}"
DRY_RUN_FLAG="${2:-}"

if [[ -z "${RELEASE_VERSION}" ]]; then
  echo "Usage: $0 <release-version> [--dry-run]" >&2
  exit 1
fi

python3 -m automation.python.sync_engine \
  --release "${RELEASE_VERSION}" \
  --settings "${REPO_ROOT}/automation/config/settings.yaml" \
  --mapping "${REPO_ROOT}/automation/config/mapping.yaml" \
  ${DRY_RUN_FLAG}
