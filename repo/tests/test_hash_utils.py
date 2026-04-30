from pathlib import Path

from automation.python.hash_utils import sha256_bytes, sha256_file


def test_sha256_bytes() -> None:
    assert sha256_bytes(b"abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_sha256_file(tmp_path: Path) -> None:
    file_path = tmp_path / "x.txt"
    file_path.write_text("content", encoding="utf-8")
    assert sha256_file(file_path) == "ed7002b439e9ac845f22357d822bac144673085f8a9d0a1b1c91e5faec63ad31"
