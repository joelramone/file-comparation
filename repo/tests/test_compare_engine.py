from pathlib import Path

from automation.python.compare_engine import CompareEngine
from automation.python.models import FileStatus, MappingEntry


class FakeS3:
    def __init__(self, content: dict[str, bytes]) -> None:
        self.content = content

    def file_exists(self, release: str, filename: str) -> bool:
        return filename in self.content

    def download_file(self, release: str, filename: str, destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(self.content[filename])
        return destination


def test_compare_detects_modified(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "k8s/helm").mkdir(parents=True)
    target = repo_root / "k8s/helm/values-default-qa"
    target.write_text("old", encoding="utf-8")

    engine = CompareEngine(FakeS3({"values-default-qa": b"new"}), tmp_path / "work")
    result = engine.compare("10.11.0", [MappingEntry(s3="values-default-qa", repo=Path("k8s/helm/values-default-qa"))], repo_root)

    assert result.records[0].status == FileStatus.MODIFIED
