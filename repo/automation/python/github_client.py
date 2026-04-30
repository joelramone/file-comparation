from __future__ import annotations

import os

import requests

from .exceptions import GitHubAPIError


class GitHubClient:
    def __init__(self, repository: str, token: str | None = None) -> None:
        self.repository = repository
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise GitHubAPIError("Missing GITHUB_TOKEN")

    @staticmethod
    def from_repo_url(repository_url: str, token: str | None = None) -> "GitHubClient":
        repo = repository_url.removesuffix(".git").split("github.com/")[-1]
        return GitHubClient(repo, token=token)

    @staticmethod
    def build_pr_title(release: str) -> str:
        return f"chore(config): sync vendor release {release}"

    @staticmethod
    def build_pr_body(release: str, files: list[str]) -> str:
        lines = [
            f"Automated configuration sync for vendor release `{release}`.",
            "",
            "### Changed files",
        ]
        lines.extend([f"- `{item}`" for item in files])
        return "\n".join(lines)

    def create_pull_request(self, title: str, body: str, head: str, base: str) -> str:
        url = f"https://api.github.com/repos/{self.repository}/pulls"
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json"},
            json={"title": title, "body": body, "head": head, "base": base},
            timeout=30,
        )
        if response.status_code >= 300:
            raise GitHubAPIError(f"GitHub API error ({response.status_code}): {response.text}")
        return response.json()["html_url"]
