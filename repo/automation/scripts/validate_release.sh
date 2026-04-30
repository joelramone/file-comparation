#!/usr/bin/env bash
set -euo pipefail

release="${1:-}"
if [[ -z "${release}" ]]; then
  echo "Usage: $0 <release-version>" >&2
  exit 2
fi

if [[ ! "${release}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Invalid release format: ${release}. Expected semver X.Y.Z" >&2
  exit 2
fi

echo "Release ${release} is valid"
