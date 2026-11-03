# Agent Multi-Repository Worktree Development

A reusable agent Skill for initializing a multi-repository workspace, isolating branch work in worktrees, maintaining and handing off that work, and discovering deployment rules from repository evidence.

## Installation

Clone or copy this repository into a skills directory supported by your agent, keeping `SKILL.md` at the root of the installed `agent-multi-repo-worktree-dev` directory. Enable or reload skills according to the agent's documentation. The Skill uses Git and the agent's filesystem tools; no additional package is required.

## First Use

Ask your agent:

> Use agent-multi-repo-worktree-dev to initialize my multi-repository workspace. Ask me for and confirm the main base directory and worktree layout before creating anything. Use the default `worktreeDir: .` so branch directories sit beside `mainDir`; do not create branch worktrees in this step.

This step only establishes the workspace configuration. The default layout places branch directories directly under the workspace root, beside `mainDir`. The agent will request the main path, show the proposed structure, and wait for confirmation.

## Ongoing Use

For each new requirement, provide the requirement source, a shared branch name, and optionally the repositories:

> Requirement: <document link or pasted brief>
> Branch: fix/upload-retry-20261102
> Repositories: repo-a, repo-b (optional; infer them from the requirement if omitted)
> Do a read-only preflight, list the paths you will create or reuse, then create all frontend/backend worktrees needed for joint debugging in one pass.

When the repository list is omitted, the agent derives candidate repositories from the requirement, shows the candidates and rationale, and waits for confirmation before writing. It does not clone or register unlisted repositories by itself. Creating the worktrees prepares the joint-debugging workspace; dependency installation, service startup, and deployment remain separately confirmed actions.

## Branch Naming and Directories

User-supplied branch names are preserved verbatim after Git reference and path-safety checks. When the user does not choose a name, the default proposal is `feature/<slug>-YYYYMMDD`, `fix/<slug>-YYYYMMDD`, or `hotfix/<slug>-YYYYMMDD` using the current date; the proposal is confirmed before use.

Every `/` in a branch name becomes a nested directory level. With the default root layout, `fix/upload-retry-20261102` maps to `<workspace>/fix/upload-retry-20261102/`; `<workspace>/feature/` and `<workspace>/fix/` are grouping directories that may contain multiple branch directories.

## Directory Model

```text
<workspace>/
├── .branch-worktree/
│   └── config.yaml
├── <mainDir>/
│   ├── project-a/
│   └── project-b/
├── fix/
│   └── upload-retry-20261102/
│       ├── project-a/
│       ├── project-b/
│       └── tmp/
└── feature/
    └── order-export-20261102/
        ├── project-a/
        └── tmp/
```

Each development effort uses one shared branch name and one branch directory directly under the workspace root. Primary checkouts remain under `<mainDir>`; development worktrees and handoff records remain in the branch directory beside it.

A separate worktree base is optional: set `worktreeDir` to a sibling directory only when the user explicitly prefers one. The separate base and `<mainDir>` must not nest, and branch paths must still avoid `mainDir` and every registered repository in the default layout.

## Documentation

| Document | Purpose |
|---|---|
| [Skill entry](SKILL.md) | Request routing and shared safety rules |
| [Workspace initialization](references/workspace-init.md) | Configuration discovery, first-use setup, adoption, and validation |
| [Branch initialization](references/branch-init.md) | Shared branch, baseline, and worktree creation |
| [Maintenance](references/maintenance.md) | Inspection, repair, pruning, and guarded cleanup |
| [Handoff](references/handoff.md) | Branch records, status, evidence, and handoff |
| [Deployment discovery](references/deployment.md) | Repository-specific CI/CD tracing and deployment confirmation |
| [Workspace configuration template](templates/workspace-config.yaml) | Version 1 configuration fields |
| [Branch record template](templates/branch-readme.md) | Handoff record structure |

## Validation

Run the standard-library test suite from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT; see [LICENSE](LICENSE).
