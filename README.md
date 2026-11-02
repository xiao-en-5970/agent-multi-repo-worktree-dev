# Agent Multi-Repository Worktree Development

A reusable agent Skill for initializing a multi-repository workspace, isolating branch work in worktrees, maintaining and handing off that work, and discovering deployment rules from repository evidence.

## Installation

Clone or copy this repository into a skills directory supported by your agent, keeping `SKILL.md` at the root of the installed `agent-multi-repo-worktree-dev` directory. Enable or reload skills according to the agent's documentation. The Skill uses Git and the agent's filesystem tools; no additional package is required.

## First Use

Ask your agent:

> Use agent-multi-repo-worktree-dev to initialize my multi-repository workspace. Ask me to choose and confirm the primary-checkout base directory and worktree base directory before creating anything.

The agent will request any missing workspace and repository information and show proposed changes for confirmation.

## Directory Model

```text
<workspace>/
├── .branch-worktree/
│   └── config.yaml
├── <mainDir>/
│   ├── project-a/
│   └── project-b/
└── <worktreeDir>/
    └── <branch-name>/
        ├── project-a/
        └── tmp/
```

Each development effort uses one shared branch name and one branch directory. Primary checkouts remain under `<mainDir>`; development worktrees and handoff records remain under `<worktreeDir>`.

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
