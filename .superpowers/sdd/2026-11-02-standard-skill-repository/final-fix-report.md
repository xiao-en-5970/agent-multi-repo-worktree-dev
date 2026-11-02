# Final-review fix wave — metadata and branch source preflight

Date: 2026-11-02
Scope: final review findings #1 and #2 only. No handoff or validation evidence was changed. No runtime fixtures or agent-behavior scenarios were executed.

## RED

Added focused structural regression coverage in `tests/test_workspace_init.py` and `tests/test_branch_handoff.py`, plus a metadata-path escape with exact stop/no-write expectations in `tests/scenarios/config-path-safety.md`.

Command run against the current documents before the production documentation changes:

```bash
python3 -m unittest -v tests.test_workspace_init.WorkspaceInitTests.test_metadata_targets_are_contained_and_rechecked_before_every_write tests.test_branch_handoff.BranchHandoffTests.test_all_branch_sources_and_targets_are_resolved_before_any_write
```

Result: 2 tests ran, both failed as expected (exit 1). The metadata document lacked the explicit containment/recheck contract; the branch document lacked the global same-name source/target preflight contract.

After the documentation changes, the metadata test also exposed a case-only typo in the new scenario assertion (`Stop` versus `stop`). Correcting that test typo and rerunning produced 2 passing tests. This did not change the scenario contract.

## Changes

1. `references/workspace-init.md`: require separate physical-path resolution and workspace containment of `.branch-worktree/` and `config.yaml` before every create/update, including nearest-existing-ancestor handling for absent targets. Reject symlink and file-type collisions, recheck on every update and immediately after writing, and preserve all first-use no-write gates.
2. `references/branch-init.md`: add a global pre-write step that resolves and classifies every repository's local and selected-remote same-name sources and existing target/occupancy. Deduplicate local/remote only at identical full SHA; divergence, multiple sources, target ambiguity, or target conflict stops the entire initialization before any `tmp/`, worktree, or branch write. Preserve local-before-selected-remote precedence for unambiguous cases and the no-reset/no-rebase rules.
3. Focused tests and the existing config/path scenario now require these contracts and the exact metadata escape stop/no-write result.

## GREEN and verification

Focused command after the changes:

```bash
python3 -m unittest -v tests.test_workspace_init.WorkspaceInitTests.test_metadata_targets_are_contained_and_rechecked_before_every_write tests.test_branch_handoff.BranchHandoffTests.test_all_branch_sources_and_targets_are_resolved_before_any_write
```

Result: 2 tests passed (exit 0).

Full suite:

```bash
python3 -m unittest discover -s tests -v
```

Result: 14 tests passed, 0 failures, 0 errors (exit 0).

Diff and public-content checks:

- `git diff --check`: passed, no whitespace errors.
- Scoped diff review: only the two requested references, focused tests, and config/path scenario were changed by this wave. A concurrently added handoff-test hunk in `tests/test_branch_handoff.py` is preserved and excluded from this wave's commit.
- Public content scan: 9 public documentation/template paths scanned; 0 findings for personal home paths, personal project markers, unfinished markers, private keys, or GitHub-token patterns. The repository public-content regression test also passed.

## Commit

Pending at report creation; the final commit SHA will be verified after committing as `fix: harden metadata and branch source preflight`.

## Concerns and limits

- These are structural Markdown contract tests, not runtime filesystem/Git fixtures. No claim is made that runtime symlink, repository, or branch fixtures were executed.
- The metadata escape scenario was added as a contract only; no behavior simulation was run in this wave.
- Finding #3 and existing handoff/validation evidence are outside this wave and were not modified.
