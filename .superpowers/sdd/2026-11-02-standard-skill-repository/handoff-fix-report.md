# Handoff evidence-link fix — RED/GREEN report

Date: 2026-11-02
Scope: final-review finding #3 only.

## Scope and boundaries

Changed only:

- `references/handoff.md`: require every matrix evidence cell to contain a Markdown link to an actual target relative to `tmp/README.md`; require replacing, not copying, template placeholders. For missing evidence, require a linked `tmp/` pending-evidence record containing the missing command, owner, and needed result; prohibit unlinked cells and invented verification.
- `templates/branch-readme.md`: place the same filling recipe beside the repository matrix.
- `tests/test_branch_handoff.py`: add two focused structural regressions covering actual relative-link replacement and the linked pending-evidence record recipe.

No subagents were dispatched. No validation ledger, GR-06, historical sample output, or other product/validation record was modified by this fix. Existing sample failures remain visible for the controller's fresh with-Skill samples.

## RED — before product/template wording changes

Command:

```bash
python3 -m unittest tests.test_branch_handoff -v
```

Observed: exit code 1; 4 tests run, 4 failures. Both new tests failed against both `references/handoff.md` and `templates/branch-readme.md`:

- `test_matrix_evidence_cells_require_actual_relative_links`: missing the per-cell actual-relative-link and placeholder-replacement recipe.
- `test_missing_evidence_requires_linked_tmp_pending_record`: missing the linked `tmp/` pending-evidence record recipe.

The two pre-existing tests passed at that point. The RED run predates concurrent finding-#2 edits in the shared worktree.

## GREEN — focused recipe regressions

Command:

```bash
python3 -m unittest tests.test_branch_handoff.BranchHandoffTests.test_matrix_evidence_cells_require_actual_relative_links tests.test_branch_handoff.BranchHandoffTests.test_missing_evidence_requires_linked_tmp_pending_record -v
```

Observed: exit code 0; 2 tests run, both passed. This is structural coverage of the required authoring recipe, not a replacement for the controller's five fresh behavior samples.

## Full structural suite and diff check

Command:

```bash
python3 -m unittest discover -s tests -v
```

Observed: exit code 1; 14 tests run, 12 passed and 2 failed. The two finding-#3 regressions passed. Failures were outside this task's scope and belonged to concurrent findings:

1. `test_all_branch_sources_and_targets_are_resolved_before_any_write` (finding #2): `references/branch-init.md` did not yet contain the required pre-write source/target resolution wording.
2. `test_metadata_targets_are_contained_and_rechecked_before_every_write` (finding #1): `references/workspace-init.md` did not yet contain the required metadata-containment wording.

Command:

```bash
git diff --check
```

Observed: exit code 0.

### Final post-commit verification

After concurrent finding-#1/#2 fixes landed in the shared worktree, the same full-suite command was rerun: exit code 0; 14 tests run, all passed. `git diff --check` again returned exit code 0. This later result does not erase the earlier failures above.

## Remaining concerns / next step

- The final full suite passed with the concurrent findings' worktree changes; their separate commits remain outside this task's scope.
- The scoped regression tests inspect the product/template recipe. They do not claim that fresh agents have already followed it.
- The controller still needs to run five fresh with-Skill samples, assess actual relative evidence links and pending-evidence records, and update GREEN evidence and ledger conclusions separately.
