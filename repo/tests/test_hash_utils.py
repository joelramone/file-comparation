from pathlib import Path

from automation.python.hash_utils import sha256_bytes, sha256_file


def test_sha256_bytes_is_deterministic() -> None:
    payload = b"abc"
    assert sha256_bytes(payload) == sha256_bytes(payload)


def test_sha256_file(tmp_path: Path) -> None:
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello", encoding="utf-8")
    assert sha256_file(file_path) == sha256_bytes(b"hello")
