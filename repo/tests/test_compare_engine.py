from pathlib import Path

from automation.python.compare_engine import compare_release
from automation.python.models import FileMapping, FileStatus


def test_compare_release_detects_added(tmp_path: Path) -> None:
    mappings = [FileMapping(s3="values-default-qa", repo=Path("k8s/helm/values-default-qa"))]
    source = {"values-default-qa": b"new-data"}
    diffs = compare_release(source, mappings, tmp_path)
    assert diffs[0].status == FileStatus.ADDED
