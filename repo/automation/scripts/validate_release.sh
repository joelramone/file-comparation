#!/usr/bin/env bash
set -euo pipefail

RELEASE_VERSION="${1:-}"
if [[ ! "${RELEASE_VERSION}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Invalid release version. Expected semantic version (example: 10.11.0)." >&2
  exit 1
fi

echo "Release version is valid: ${RELEASE_VERSION}"
