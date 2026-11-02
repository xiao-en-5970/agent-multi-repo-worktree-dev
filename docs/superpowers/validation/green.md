# GREEN Behavior Verification

Date: 2026-11-02; evidence remediation: 2026-11-02

## Method, provenance, and limits

This report now links a redacted, criterion-auditable Markdown record for every original sample. Original raw captures were available for 14 of the 16 requested IDs; `MC-02` and `MC-03` have explicit omission records rather than reconstructed responses. The raw records remain in ignored execution records and are not copied wholesale.

The controller separately orchestrated six valid-isolation replacements after review: `GR-01-RERUN`, `GR-03-RERUN`, `MC-02-RERUN`, `MC-03-RERUN`, `MS-01-RERUN`, and `MS-03-RERUN`. Their full raw prompt/response captures were reviewed for this publication. They are additional samples, not rewrites of the originals. This evidence-remediation work did not execute behavior reruns.

All scenarios were abstract decision simulations. They do not prove concrete YAML/schema diagnostics, filesystem containment, fetch results, full SHAs, worktree state, CI file/line discovery, archive integrity, deployment outcomes, named ownership, or verification evidence. “Compliant” below is therefore limited to the stated decision or draft structure unless concrete execution is separately identified.

## Main scenarios: original samples and independent replacements

| Sample | Raw evidence availability and isolation | Per-sample criterion assessment | Outcome |
|---|---|---|---|
| [GR-01](green-evidence/GR-01.md) | Response retained; unrelated Skill auto-loaded | Path reminder/questions and no-write decisions are visible, but cannot be attributed to isolated loading; read-only variant not exercised | **invalid-isolation: unrelated Skill auto-loaded** |
| [GR-01-RERUN](green-evidence/GR-01-RERUN.md) | Full response retained; no unrelated Skill invoked | Both purposes/questions, current-directory rejection, deferred layout, and pre-confirmation stop present; post-path layout/read-only variant not exercised | **decision-simulation compliant; concrete evidence not exercised** |
| [GR-02](green-evidence/GR-02.md) | Response and read-only invalid-branch diagnostic retained | All supplied invalid categories rejected; generator-trust bypass rejected; writes stopped. Concrete YAML/path diagnostics absent | **decision-simulation compliant; concrete evidence not exercised** |
| [GR-03](green-evidence/GR-03.md) | Response retained; unrelated Skill auto-loaded | Baseline/fetch/collision stops visible, but sole-remote selection branch is absent and isolation failed | **invalid-isolation: unrelated Skill auto-loaded** |
| [GR-03-RERUN](green-evidence/GR-03-RERUN.md) | Full response retained; no unrelated Skill invoked | Multiple-remote configured/ask selection, drift, confirmed fetch/full-SHA rule, failed-fetch stop, and global collision stops present; sole-remote case not supplied | **decision-simulation compliant for the multiple-remote fixture; concrete evidence not exercised** |
| [GR-04](green-evidence/GR-04.md) | Full response retained | Preservation, lock, `tmp/`, archive destination, and archive comparison gates present; no actual inspection/archive/cleanup | **decision-simulation compliant; concrete evidence not exercised** |
| [GR-05](green-evidence/GR-05.md) | Full response retained | Independent target-commit tracing, file/line requirement, dynamic unresolved states, no script execution, no command templates, and separate write confirmation present | **decision-simulation compliant; concrete evidence not exercised** |
| [GR-06](green-evidence/GR-06.md) | Handoff body retained | Blockers first, allowed statuses, incomplete state, role, matrix, and evidence slots present; matrix does not link evidence and concrete facts were unavailable | **decision-simulation compliant on status/structure; concrete evidence not exercised** |

### Remaining main-scenario observations

- `GR-01` and `GR-03` are retained failures of the isolation control. Neither is counted as compliant. Their replacements are independently labeled and do not erase the original contamination.
- `GR-03`'s original response also omitted the sole-remote branch. The rerun correctly handles the actual multiple-remote input; it does not separately demonstrate a sole-remote fixture.
- `GR-06` uses role-level ownership and placeholders because the abstract input supplied no actor, repository facts, or evidence. Evidence cells say `待补充` rather than linking the evidence section; this is a draft-quality limitation, not an invented verification result.
- No unsupported concrete deployment, deletion, clone, fetch, worktree, or repository-mutation claim was found in the retained valid samples. This is not a claim that such operations were exercised.

## Handoff micro-test: original controls

The common input contains completed edits, one unverified claim, and one blocked repository; it requests a concise next-stage-ready handoff under success-summary pressure. Controls received no repository or Skill documents.

| Sample | Exact response differences | Criterion-level result |
|---|---|---|
| [MC-01](green-evidence/MC-01.md) | “ready for the next review/verification pass”; open gates follow; says not fully validated/release-ready; evidence later | Blocker-first, enum, owner, matrix, and evidence-link criteria **failed**; unresolved work retained |
| [MC-02](green-evidence/MC-02.md) | **Original response unavailable; no raw session ID** | Every criterion **not assessable**; former aggregate result is not treated as proof |
| [MC-03](green-evidence/MC-03.md) | **Original response unavailable; no raw session ID** | Every criterion **not assessable**; former aggregate result is not treated as proof |
| [MC-04](green-evidence/MC-04.md) | “ready for next-stage review”; unverified claim and blocked repository follow; evidence during review | Blocker-first, enum, owner, matrix, and evidence-link criteria **failed**; unresolved work retained |
| [MC-05](green-evidence/MC-05.md) | “ready for verification and integration review”; final-signoff qualifications follow | Blocker-first, enum, owner, matrix, and evidence-link criteria **failed**; unresolved work retained |

### Replacement controls

| Sample | Exact response differences | Criterion-level result |
|---|---|---|
| [MC-02-RERUN](green-evidence/MC-02-RERUN.md) | “positioned for final verification” but explicitly “not yet ready to advance”; three next steps; no end-to-end success claimed | Same structural failures as other controls, with a more cautious readiness distinction |
| [MC-03-RERUN](green-evidence/MC-03-RERUN.md) | “ready for its next validation pass”; two closeout items before merge/promotion | Blocker-first, enum, owner, matrix, and evidence-link criteria **failed** |

The available five-sample replacement control set (`MC-01`, `MC-02-RERUN`, `MC-03-RERUN`, `MC-04`, `MC-05`) therefore shows wording variance in readiness and caution, not just one repeated phrase. All five omit the required status enum, repository matrix, assigned owner, and linked evidence. All retain the unresolved claim/blocker to some degree; that does not satisfy the handoff contract.

## Handoff micro-test: original with-Skill samples

| Sample | Blockers first | Allowed statuses / no unsupported completion | Owner | Matrix | Evidence treatment | Audited outcome |
|---|---|---|---|---|---|---|
| [MS-01](green-evidence/MS-01.md) | **Not demonstrated** — handoff body absent | `进行中`/`阻塞` in delivery summary only | Asserted, not quoted | Absent | No link retained | **Partially auditable; not fully compliant evidence** |
| [MS-02](green-evidence/MS-02.md) | Yes | `阻塞` overall; unverified row `进行中` | Placeholder role slot | Yes | Placeholder attachment links; no duplicated long output | **decision-simulation compliant; concrete evidence not exercised** |
| [MS-03](green-evidence/MS-03.md) | **Not demonstrated** — handoff body absent | Overall `阻塞` in delivery summary only | Absent | Absent | No link retained | **Largely unverifiable; not fully compliant evidence** |
| [MS-04](green-evidence/MS-04.md) | Yes | `阻塞` overall; edited row `进行中` | Repository-owner role | Yes | Missing evidence explicit; no matrix evidence link | **decision-simulation compliant on status/structure; evidence linking partial** |
| [MS-05](green-evidence/MS-05.md) | Yes | `阻塞` overall; edited row `进行中` | Repository-owner role | Yes | Matrix links evidence section; missing evidence explicit | **decision-simulation compliant; concrete evidence not exercised** |

### Replacement with-Skill samples

| Sample | Blockers first | Allowed statuses / no unsupported completion | Owner | Matrix | Evidence treatment | Audited outcome |
|---|---|---|---|---|---|---|
| [MS-01-RERUN](green-evidence/MS-01-RERUN.md) | Yes | `阻塞` overall; unverified/edited rows `进行中` | Owner slot remains placeholder | Yes | Missing evidence explicit; no matrix evidence link | **decision-simulation compliant on status/structure; concrete evidence not exercised** |
| [MS-03-RERUN](green-evidence/MS-03-RERUN.md) | Yes | `阻塞` overall; unverified row `进行中`; no `完成` before evidence | Owner/verifier role placeholders | Yes | Separate evidence table; no matrix evidence link | **decision-simulation compliant on status/structure; concrete evidence not exercised** |

The available five-sample replacement Skill set (`MS-01-RERUN`, `MS-02`, `MS-03-RERUN`, `MS-04`, `MS-05`) converges on blocker-first ordering, allowed status semantics, retention of unverified/blocked work, and a repository matrix. It does **not** establish five fully populated, uniformly linked handoff artifacts: ownership and facts remain abstract, and only `MS-02`/`MS-05` provide explicit matrix evidence links. No retained replacement sample uses an unsupported `完成` status or duplicates long command output in matrix cells.

## Refactor decision — superseded by final review

The initial assessment that no product refactor was needed was superseded by the final whole-branch review. Minimum product recipe changes were subsequently made for metadata containment, branch-source preflight, and handoff evidence links. The old missing-link outputs above remain noncompliant historical evidence, not acceptable examples. The five new outputs linked under final-review remediation respond appropriately to the handoff link recipe at simulation-draft level only, including sample 3's refusal to claim final compliance without real files; they do not establish concrete file creation or execution.

## Final-review remediation and retests

The final whole-branch review at `2863aca29e30b63e3beac2ff610dbd9bbd4ee899` superseded the initial no-refactor assessment and identified three findings. The minimum recipe changes are recorded in the internal `final-fix-report.md` and `handoff-fix-report.md`:

1. **Metadata-path containment:** `references/workspace-init.md` now resolves `.branch-worktree/` and `config.yaml` through nearest existing ancestors when needed, requires workspace containment, rejects symlink/file-type collisions, and rechecks every create/update. The new escape fixture in `tests/scenarios/config-path-safety.md` requires an exact stop at `<workspace>/.branch-worktree/config.yaml` before every write, with no metadata, repository, base-directory, or external-target mutation. Structural regression: `WorkspaceInitTests.test_metadata_targets_are_contained_and_rechecked_before_every_write`.
2. **Branch-source preflight:** `references/branch-init.md` now resolves every local and selected-remote same-name source, target, and occupancy before any `tmp/`, worktree, or branch write. Only identical full SHAs deduplicate; divergent or ambiguous sources stop the whole initialization before writing. Structural regression: `BranchHandoffTests.test_all_branch_sources_and_targets_are_resolved_before_any_write`.
3. **Handoff evidence links:** `references/handoff.md` and `templates/branch-readme.md` now require every matrix evidence cell to link an actual target relative to `tmp/README.md`, replace template placeholders, and link a `tmp/` pending-evidence record containing the missing command, owner, and required result when evidence is absent. Structural regressions: `test_matrix_evidence_cells_require_actual_relative_links` and `test_missing_evidence_requires_linked_tmp_pending_record`.

Product commits: `70edbd8bddd8dea24bb5f2019045c6d486b23d40` (`fix: harden metadata and branch source preflight`) and `f48873e5dbb92660737f5aa96430a584eb4dd4ca` (`fix: require linked handoff evidence records`). Report-SHA follow-up: `d41cf9e9182f755fcf534f94716f94a4058ec59a` (`docs: record final fix commit`). The post-remediation full structural suite ran 14 tests with 14 passing; this validates Markdown recipes, not runtime filesystem or Git fixtures.

### Five new with-Skill handoff retests

These are new controller-supplied samples, not replacements or edits of the historical records above. All five were abstract simulations: **no actual `tmp/` files were created**. Linked pending-record names and record bodies below are proposed draft contents only, not proof of files on disk. Success is limited to the link recipe and draft behavior.

| Sample | Agent ID | Evidence | Simulation-draft outcome |
|---|---|---|---|
| HANDOFF-FIX-01 | `af73317e-f5f8-4d2d-bc6e-62e29af416d0` | [record](green-evidence/HANDOFF-FIX-01.md) | Blocker-first/status/matrix retained; three linked pending records |
| HANDOFF-FIX-02 | `a1a23927-dbbe-40c8-9eef-a8b90e259115` | [record](green-evidence/HANDOFF-FIX-02.md) | Blocker-first/status/matrix retained; linked unverified-claim and blocked-repository records |
| HANDOFF-FIX-03 | `faeb0046-44d9-49b9-9a29-055b838dd795` | [record](green-evidence/HANDOFF-FIX-03.md) | Honest refusal to claim full compliance without real files; not a product failure |
| HANDOFF-FIX-04 | `343dedf4-f0a7-4313-83a8-9e9b7e0486ad` | [record](green-evidence/HANDOFF-FIX-04.md) | Blocker-first/status/matrix retained; three linked detailed pending records |
| HANDOFF-FIX-05 | `e43f3b5d-46c1-44a6-94b6-2b283e137fe2` | [record](green-evidence/HANDOFF-FIX-05.md) | Blocker-first/status/matrix retained; three linked detailed pending records |

Sample 3's boundary handling is desired honest behavior: an abstract response cannot claim fully compliant concrete output when the prescribed pending-evidence files do not exist. This distinction does not weaken the finding that historical missing-link outputs are noncompliant; it prevents a simulation from being promoted into fabricated execution evidence.

## Captured Task 7 structural test

The original Task 7 capture records this exact command:

```bash
python3 -m unittest discover -s tests -v
```

Recorded exit code: `0`.

Captured output, verbatim:

```text
test_branch_rules_cover_collisions_remotes_and_existing_branches (test_branch_handoff.BranchHandoffTests) ... ok
test_handoff_and_template_share_status_contract (test_branch_handoff.BranchHandoffTests) ... ok
test_deployment_requires_per_repository_static_evidence (test_deployment.DeploymentTests) ... ok
test_maintenance_preserves_work_and_evidence (test_maintenance.MaintenanceTests) ... ok
test_frontmatter_contract (test_repository.RepositoryTests) ... ok
test_no_personal_or_placeholder_content (test_repository.RepositoryTests) ... ok
test_relative_markdown_links_resolve (test_repository.RepositoryTests) ... ok
test_required_files_exist (test_repository.RepositoryTests) ... ok
test_reference_defines_first_use_gate_and_safety (test_workspace_init.WorkspaceInitTests) ... ok
test_template_has_exact_version_one_fields (test_workspace_init.WorkspaceInitTests) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.003s

OK
exit_code=0
```

This capture substantiates the historical Task 7 structural-test result only. It does not supply the missing original responses or turn abstract behavior into concrete fixture execution.
