---
name: agent-multi-repo-worktree-dev
description: Use when setting up a multi-repository workspace for the first time, creating or resuming branch-based worktrees across repositories, maintaining or handing off branch work, or discovering repository-specific CI/CD deployment rules.
---

# Agent Multi-Repository Worktree Development

## Route the Request

Load the reference matching the request; keep its complete procedure in that file.

| Request | Reference |
|---|---|
| First-use setup, workspace adoption, missing or invalid configuration | [Workspace initialization](references/workspace-init.md) |
| Create, supplement, or resume multi-repository branch worktrees from a requirement source, shared branch name, and optional repository list | [Branch initialization](references/branch-init.md) |
| Inspect, repair, prune, or clean existing worktrees | [Maintenance](references/maintenance.md) |
| Create or update branch records, progress, evidence, or handoff | [Handoff](references/handoff.md) |
| Discover or execute repository-specific deployment | [Deployment discovery](references/deployment.md) |

## Shared Model

Discover configuration from an explicitly supplied workspace or file first; otherwise search upward for the nearest `.branch-worktree/config.yaml`. If none exists, use workspace initialization and obtain both base-directory choices before writing. Never substitute a personal or built-in path.

One development effort uses one shared branch name and one directory: `<workspace>/<worktreeDir>/<branch path>/`, where every `/` in the branch name becomes a nested directory level. `worktreeDir` may be `.` when the user explicitly chooses a root-level layout; branch directories then sit directly beside `mainDir` under the workspace root, and branch paths must avoid `mainDir` and every registered repository. The `mainDir` base contains each repository's primary checkout; development occurs in isolated worktrees under the worktree root. Record primary-checkout drift without switching or modifying it, and derive baselines according to branch initialization.

Preserve user-supplied branch names verbatim after Git reference and path-safety checks. If the user does not name the branch, propose the default `feature/<slug>-YYYYMMDD`, `fix/<slug>-YYYYMMDD`, or `hotfix/<slug>-YYYYMMDD` form with the current date and confirm it. Never append a date, replace a prefix, or rewrite an existing branch without explicit user direction.

First-use setup requires only the two base directories as initial input; repository registration is derived from the confirmed main base and configuration, with ambiguity resolved by asking. Branch initialization accepts a requirement source and shared branch name; repositories may be named explicitly or derived from the requirement, with the candidate set confirmed before writes. A requested frontend/backend integration creates all confirmed repositories' worktrees under the same branch directory in one initialization pass. Dependency installation, service startup, and deployment remain separate confirmed actions.

Do not develop from a confirmed deployment-environment branch or reverse-merge environment branches. Establish non-default baselines from project instructions or CI/CD evidence rather than branch names.

## Safety and Evidence

Before writing, validate configuration, paths, repository state, and baselines; present the proposed targets and impacts and obtain each confirmation required by the selected reference. Preserve existing history and conflicts, keep operations idempotent, and stop when evidence is missing or ambiguous.

For deployment, independently trace each target repository's CI/CD configuration, includes, scripts, and checks at the target commit. Do not assume environment refs, tag formats, or promotion order; confirm deployment write operations separately.

Report only verified results, with commit, command, path, or deployment evidence. Distinguish completed, skipped, blocked, and partial work; update handoff records as facts change.
