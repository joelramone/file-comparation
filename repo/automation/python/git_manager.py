from __future__ import annotations

from pathlib import Path

from git import Repo
from git.exc import GitCommandError

from .exceptions import GitError


class GitManager:
    def clone(self, repository_url: str, clone_dir: Path) -> Repo:
        try:
            if clone_dir.exists() and (clone_dir / ".git").exists():
                return Repo(clone_dir)
            return Repo.clone_from(repository_url, clone_dir)
        except GitCommandError as exc:
            raise GitError(f"Failed to clone repository {repository_url}") from exc

    def checkout(self, repo: Repo, branch: str) -> None:
        try:
            repo.git.checkout(branch)
        except GitCommandError as exc:
            raise GitError(f"Failed to checkout branch {branch}") from exc

    def create_branch(self, repo: Repo, branch: str, base_branch: str) -> None:
        try:
            repo.git.checkout(base_branch)
            repo.git.pull("origin", base_branch)
            repo.git.checkout("-B", branch)
        except GitCommandError as exc:
            raise GitError(f"Failed to create branch {branch}") from exc

    def commit_all(self, repo: Repo, message: str) -> bool:
        repo.git.add(A=True)
        if not repo.is_dirty(untracked_files=True):
            return False
        repo.index.commit(message)
        return True

    def push(self, repo: Repo, branch: str) -> None:
        try:
            repo.remote("origin").push(refspec=f"{branch}:{branch}")
        except GitCommandError as exc:
            raise GitError(f"Failed to push branch {branch}") from exc
