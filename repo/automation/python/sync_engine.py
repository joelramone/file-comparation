from __future__ import annotations

from pathlib import Path

from .compare_engine import compare_release
from .config_loader import load_mappings, load_settings
from .git_manager import GitManager
from .github_client import GitHubClient
from .logger import get_logger
from .manifest import write_manifest
from .models import FileStatus, ReleaseManifest, SyncResult
from .s3_client import S3ReleaseClient


class SyncEngine:
    def __init__(self, settings_path: Path, mapping_path: Path, dry_run: bool = False) -> None:
        self.settings = load_settings(settings_path)
        self.mapping = load_mappings(mapping_path)
        self.dry_run = dry_run
        self.logger = get_logger("sync_engine")
        self.git = GitManager()
        self.s3 = S3ReleaseClient(self.settings.s3)

    def run(self, release: str) -> SyncResult:
        branch = f"upgrade/{release}"
        repo = self.git.clone_or_open(str(self.settings.github.repository_url), self.settings.workspace.clone_dir)
        self.git.create_branch(repo, branch, self.settings.github.base_branch)

        source_data = self.s3.get_release_files(release, [m.s3 for m in self.mapping.mappings])
        diffs = compare_release(source_data, self.mapping.mappings, self.settings.workspace.clone_dir)

        changed = []
        for diff in diffs:
            self.logger.info("file comparison", extra={"data": {"release": release, "file": diff.source, "status": diff.status.value}})
            if diff.status in (FileStatus.ADDED, FileStatus.MODIFIED):
                changed.append(diff.destination)
                if not self.dry_run:
                    diff.destination.parent.mkdir(parents=True, exist_ok=True)
                    diff.destination.write_bytes(source_data[diff.source])

        manifest = ReleaseManifest(release=release, changes=diffs)
        write_manifest(self.settings.workspace.clone_dir / ".sync" / f"{release}.json", manifest)

        pr_url = None
        if changed and not self.dry_run:
            committed = self.git.commit_all(repo, f"chore: sync vendor config for release {release}")
            if committed:
                self.git.push(repo, branch)
                gh = GitHubClient.from_repo_url(str(self.settings.github.repository_url))
                pr_url = gh.create_pull_request(
                    title=gh.build_pr_title(release),
                    body=gh.build_pr_body(release, [str(p) for p in changed]),
                    head=branch,
                    base=self.settings.github.base_branch,
                )

        return SyncResult(release=release, branch=branch, changed_files=changed, pr_url=pr_url, dry_run=self.dry_run)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Synchronize vendor configs from S3 to target repository")
    parser.add_argument("--release", required=True)
    parser.add_argument("--settings", default="automation/config/settings.yaml")
    parser.add_argument("--mapping", default="automation/config/mapping.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    engine = SyncEngine(Path(args.settings), Path(args.mapping), dry_run=args.dry_run)
    result = engine.run(args.release)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
