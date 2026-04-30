from automation.python.models import SyncResult


def test_sync_result_model() -> None:
    model = SyncResult(release="10.11.0", branch="upgrade/10.11.0", dry_run=True, changed_files=[])
    assert model.release == "10.11.0"
