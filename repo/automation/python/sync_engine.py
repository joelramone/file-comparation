from __future__ import annotations

import argparse
from pathlib import Path

from .compare_engine import CompareEngine
from .config_loader import load_mapping, load_settings
from .github_client import GitHubClient
from .git_manager import GitManager
from .logger import get_logger
from .manifest import build_manifest, write_manifest
from .models import FileStatus, SyncResult
from .s3_client import S3Client


def run_sync(release: str, settings_path: Path, mapping_path: Path, dry_run: bool) -> SyncResult:
    logger = get_logger("sync_engine")
    settings = load_settings(settings_path)
    mapping = load_mapping(mapping_path)

    s3 = S3Client(bucket=settings.s3.bucket, release_prefix=settings.s3.release_prefix)
    git_manager = GitManager()
    repo = git_manager.clone(str(settings.github.repository_url), Path(settings.workspace.clone_dir))

    git_manager.checkout(repo, settings.github.base_branch)
    branch = f"upgrade/{release}"
    git_manager.create_branch(repo, branch, settings.github.base_branch)

    comparer = CompareEngine(s3, mapping)
    comparisons = comparer.compare_release(release, Path(settings.workspace.clone_dir))
    changed = [c for c in comparisons if c.status in {FileStatus.ADDED, FileStatus.MODIFIED}]

    for item in changed:
        data = s3.download_text(release, item.s3_file)
        target = Path(settings.workspace.clone_dir) / item.repo_file
        logger.info("sync_change", extra={"context": {"release": release, "file": item.repo_file, "status": item.status.value}})
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

    manifest = build_manifest(release=release, dry_run=dry_run, comparisons=comparisons)
    write_manifest(Path(settings.workspace.clone_dir) / "sync-manifest.json", manifest)

    pr_url = None
    if not dry_run and changed:
        commit_message = f"chore: sync vendor config release {release}"
        committed = git_manager.commit_all(repo, commit_message)
        if committed:
            git_manager.push(repo, branch)
            gh = GitHubClient()
            pr_url = gh.create_pull_request(
                repository_url=str(settings.github.repository_url),
                title=gh.build_pr_title(release),
                body=gh.build_pr_body(release, [c.repo_file for c in changed]),
                head=branch,
                base=settings.github.base_branch,
            )

    return SyncResult(release=release, branch=branch, dry_run=dry_run, changed_files=changed, pr_url=pr_url)


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize release configuration from S3 to target repository")
    parser.add_argument("--release", required=True)
    parser.add_argument("--settings", default="automation/config/settings.yaml")
    parser.add_argument("--mapping", default="automation/config/mapping.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result = run_sync(args.release, Path(args.settings), Path(args.mapping), args.dry_run)
    print(result.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
