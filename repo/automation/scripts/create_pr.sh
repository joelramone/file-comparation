#!/usr/bin/env bash
set -euo pipefail

RELEASE_VERSION="${1:-}"
BASE_BRANCH="${2:-main}"
HEAD_BRANCH="upgrade/${RELEASE_VERSION}"

if [[ -z "${RELEASE_VERSION}" ]]; then
  echo "Usage: $0 <release-version> [base-branch]" >&2
  exit 1
fi

python3 - <<'PY'
import os
from automation.python.github_client import GitHubClient

release = os.environ["RELEASE_VERSION"]
base = os.environ["BASE_BRANCH"]
head = os.environ["HEAD_BRANCH"]
repo_url = os.environ.get("REPOSITORY_URL", "https://github.com/company/application-repo.git")
files = os.environ.get("CHANGED_FILES", "k8s/helm/*").split(",")

client = GitHubClient.from_repo_url(repo_url)
url = client.create_pull_request(
    title=client.build_pr_title(release),
    body=client.build_pr_body(release, files),
    head=head,
    base=base,
)
print(url)
PY
