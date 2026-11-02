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
| Create, supplement, or resume multi-repository branch worktrees | [Branch initialization](references/branch-init.md) |
| Inspect, repair, prune, or clean existing worktrees | [Maintenance](references/maintenance.md) |
| Create or update branch records, progress, evidence, or handoff | [Handoff](references/handoff.md) |
| Discover or execute repository-specific deployment | [Deployment discovery](references/deployment.md) |

## Shared Model

Discover configuration from an explicitly supplied workspace or file first; otherwise search upward for the nearest `.branch-worktree/config.yaml`. If none exists, use workspace initialization and obtain both base-directory choices before writing. Never substitute a personal or built-in path.

One development effort uses one shared branch name and one directory: `<workspace>/<worktreeDir>/<branch>/`. The `mainDir` base contains each repository's primary checkout; development occurs in isolated worktrees under `worktreeDir`. Record primary-checkout drift without switching or modifying it, and derive baselines according to branch initialization.

Do not develop from a confirmed deployment-environment branch or reverse-merge environment branches. Establish non-default baselines from project instructions or CI/CD evidence rather than branch names.

## Safety and Evidence

Before writing, validate configuration, paths, repository state, and baselines; present the proposed targets and impacts and obtain each confirmation required by the selected reference. Preserve existing history and conflicts, keep operations idempotent, and stop when evidence is missing or ambiguous.

For deployment, independently trace each target repository's CI/CD configuration, includes, scripts, and checks at the target commit. Do not assume environment refs, tag formats, or promotion order; confirm deployment write operations separately.

Report only verified results, with commit, command, path, or deployment evidence. Distinguish completed, skipped, blocked, and partial work; update handoff records as facts change.
