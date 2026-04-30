from pathlib import Path

from git import Repo

from automation.python.git_manager import GitManager


def test_commit_all_without_changes(tmp_path: Path) -> None:
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    repo = Repo.init(repo_path)
    manager = GitManager()
    assert manager.commit_all(repo, "no changes") is False
