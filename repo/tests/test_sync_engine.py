from pathlib import Path

from automation.python.sync_engine import SyncEngine


def test_sync_engine_dry_run(monkeypatch, tmp_path: Path) -> None:
    settings = tmp_path / "settings.yaml"
    mapping = tmp_path / "mapping.yaml"

    settings.write_text(
        """
github:
  repository_url: https://github.com/company/application-repo.git
  base_branch: main
s3:
  bucket: bucket
  release_prefix: elipse-releases
workspace:
  clone_dir: /tmp/application-repo-test
""",
        encoding="utf-8",
    )
    mapping.write_text(
        """
mappings:
  - s3: values-default-qa
    repo: k8s/helm/values-default-qa
""",
        encoding="utf-8",
    )

    class DummyRepo:
        pass

    engine = SyncEngine(settings, mapping, dry_run=True)
    monkeypatch.setattr(engine.git, "clone_or_open", lambda *_: DummyRepo())
    monkeypatch.setattr(engine.git, "create_branch", lambda *_: None)
    monkeypatch.setattr(engine.s3, "get_release_files", lambda *_: {"values-default-qa": b"x"})

    result = engine.run("1.0.0")
    assert result.dry_run is True
