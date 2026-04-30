#!/usr/bin/env bash
set -euo pipefail

RELEASE="${1:?usage: create_pr.sh <release>}"
export RELEASE
python - <<'PY'
import os
from pathlib import Path

from automation.python.config_loader import load_settings
from automation.python.github_client import GitHubClient

release = os.environ["RELEASE"]
settings = load_settings(Path("automation/config/settings.yaml"))
client = GitHubClient()
print(client.create_pull_request(
    repository_url=str(settings.github.repository_url),
    title=client.build_pr_title(release),
    body=client.build_pr_body(release, []),
    head=f"upgrade/{release}",
    base=settings.github.base_branch,
))
PY
