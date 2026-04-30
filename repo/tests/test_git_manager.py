from pathlib import Path

from git import Repo

from automation.python.git_manager import GitManager


def test_commit_all(tmp_path: Path) -> None:
    repo = Repo.init(tmp_path)
    file_path = tmp_path / "file.txt"
    file_path.write_text("value", encoding="utf-8")
    manager = GitManager()
    assert manager.commit_all(repo, "initial") is True
