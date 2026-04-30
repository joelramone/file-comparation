from pathlib import Path

from automation.python.compare_engine import CompareEngine
from automation.python.models import MappingEntry
from automation.python.sync_engine import synchronize


class FakeS3:
    def file_exists(self, release: str, filename: str) -> bool:
        return True

    def download_file(self, release: str, filename: str, destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("new-content", encoding="utf-8")
        return destination


def test_synchronize_updates_file(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    target = repo_root / "k8s/helm/values-default-qa"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("old-content", encoding="utf-8")

    mappings = [MappingEntry(s3="values-default-qa", repo=Path("k8s/helm/values-default-qa"))]
    compare = CompareEngine(FakeS3(), tmp_path / "work")

    report = synchronize(compare, mappings, "10.11.0", repo_root, dry_run=False)

    assert len(report.updated_files) == 1
    assert target.read_text(encoding="utf-8") == "new-content"
