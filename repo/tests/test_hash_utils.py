from pathlib import Path

from automation.python.hash_utils import sha256_bytes, sha256_file


def test_sha256_bytes_is_deterministic() -> None:
    assert sha256_bytes(b"abc") == sha256_bytes(b"abc")


def test_sha256_file(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_text("content", encoding="utf-8")
    assert sha256_file(sample)
