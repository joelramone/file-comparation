#!/usr/bin/env bash
set -euo pipefail

RELEASE="${1:?usage: validate_release.sh <release>}"
[[ "${RELEASE}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || {
  echo "Invalid release format: ${RELEASE}" >&2
  exit 2
}

echo "Release ${RELEASE} is valid"
