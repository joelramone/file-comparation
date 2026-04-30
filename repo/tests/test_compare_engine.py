from pathlib import Path

from automation.python.compare_engine import CompareEngine
from automation.python.models import MappingConfig, MappingItem, FileStatus


class FakeS3:
    def __init__(self, payload: dict[str, bytes]) -> None:
        self.payload = payload

    def download_text(self, release: str, filename: str) -> bytes:
        return self.payload[filename]


def test_compare_modified(tmp_path: Path) -> None:
    repo_file = tmp_path / "k8s/helm/values-default-qa"
    repo_file.parent.mkdir(parents=True)
    repo_file.write_text("old", encoding="utf-8")
    mapping = MappingConfig(mappings=[MappingItem(s3="values-default-qa", repo="k8s/helm/values-default-qa")])
    engine = CompareEngine(FakeS3({"values-default-qa": b"new"}), mapping)
    result = engine.compare_release("10.11.0", tmp_path)
    assert result[0].status == FileStatus.MODIFIED
