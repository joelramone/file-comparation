# Repository Strategy

## Separation of concerns

- Automation repository: orchestration logic, CI pipeline, tests, and docs.
- Application repository: runtime assets (`k8s/helm/*`) that are updated by automation.

## Operational model

The automation repository never stores application file copies permanently. It clones the target repository into a workspace (`/tmp/application-repo`), applies release deltas, and proposes updates through pull requests.

## Benefits

- Independent lifecycle for automation tooling.
- Reusable automation for multiple application repositories.
- Auditable updates through release-specific branches and PRs.
