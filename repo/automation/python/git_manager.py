from __future__ import annotations

from pathlib import Path

from git import Repo
from git.exc import GitCommandError

from .exceptions import GitOperationError


class GitManager:
    def clone_or_open(self, repository_url: str, clone_dir: Path) -> Repo:
        try:
            if clone_dir.exists() and (clone_dir / ".git").exists():
                return Repo(clone_dir)
            clone_dir.parent.mkdir(parents=True, exist_ok=True)
            return Repo.clone_from(repository_url, clone_dir)
        except GitCommandError as exc:
            raise GitOperationError(f"Failed cloning repository: {repository_url}") from exc

    def checkout(self, repo: Repo, branch: str) -> None:
        try:
            repo.git.checkout(branch)
        except GitCommandError as exc:
            raise GitOperationError(f"Failed checkout: {branch}") from exc

    def create_branch(self, repo: Repo, branch: str, base_branch: str) -> None:
        try:
            repo.git.checkout(base_branch)
            repo.remotes.origin.pull(base_branch)
            repo.git.checkout("-B", branch)
        except GitCommandError as exc:
            raise GitOperationError(f"Failed creating branch {branch}") from exc

    def commit_all(self, repo: Repo, message: str) -> bool:
        repo.git.add(A=True)
        if not repo.is_dirty(untracked_files=True):
            return False
        repo.index.commit(message)
        return True

    def push(self, repo: Repo, branch: str) -> None:
        try:
            repo.remotes.origin.push(refspec=f"{branch}:{branch}", set_upstream=True)
        except GitCommandError as exc:
            raise GitOperationError(f"Failed pushing branch {branch}") from exc
