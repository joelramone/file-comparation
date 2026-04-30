from __future__ import annotations

import os
from urllib.parse import urlparse

import requests

from .exceptions import GitHubError


class GitHubClient:
    def __init__(self, token: str | None = None) -> None:
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise GitHubError("Missing GITHUB_TOKEN")

    @staticmethod
    def _repo_slug(repository_url: str) -> str:
        parsed = urlparse(repository_url)
        path = parsed.path.strip("/")
        return path.removesuffix(".git")

    def create_pull_request(self, repository_url: str, title: str, body: str, head: str, base: str) -> str:
        slug = self._repo_slug(repository_url)
        api_url = f"https://api.github.com/repos/{slug}/pulls"
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json"}
        payload = {"title": title, "body": body, "head": head, "base": base}
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        if response.status_code >= 300:
            raise GitHubError(f"Failed creating PR: {response.status_code} {response.text}")
        return response.json()["html_url"]

    @staticmethod
    def build_pr_title(release: str) -> str:
        return f"chore: sync vendor config release {release}"

    @staticmethod
    def build_pr_body(release: str, changed_files: list[str]) -> str:
        files = "\n".join(f"- {item}" for item in changed_files)
        return f"Automated sync for release `{release}`.\n\nChanged files:\n{files}"
