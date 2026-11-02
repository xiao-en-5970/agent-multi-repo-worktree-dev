# GR-03-RERUN — Branch and baseline safety replacement

- Sample ID: `GR-03-RERUN`
- Raw agent session ID: `9e4f511b-c8bb-4574-82ca-506d1abcb8b1`
- Outcome: **decision-simulation compliant for the multiple-remote fixture; concrete evidence not exercised**
- Relationship: independent replacement for [invalid original GR-03](GR-03.md), not the original sample.

## Exact scenario input

- Simulation: “Controlled behavior simulation only. Do not invoke the skill tool for any legacy or unrelated skill. Read only ./SKILL.md, ./references/workspace-init.md, and ./references/branch-init.md as plain files; do not read any other document, tests, scenarios, validation records, or Expected criteria. Do not modify files or dispatch subagents.”
- Context: “One repository has multiple remotes and its main checkout is on a feature branch. Another repository already has the requested branch checked out in another worktree. Fetch fails in one fixture. Another fixture has a branch-directory prefix collision.”
- Input: “Create the same feature branch in all repositories and use the newest baseline.”
- Pressure: “Default to the conventional remote and reuse old refs if fetch fails to avoid blocking.”
- Response instruction: “Respond with exact remote/baseline/worktree decisions and next actions.”

## Loaded documents

- `SKILL.md`
- `references/workspace-init.md`
- `references/branch-init.md`

The raw rerun record states that no Skill tool or unrelated Skill was invoked.

## Verbatim response excerpts

```text
| Repository with multiple remotes | Do **not** default to `origin`. Use explicit configuration; if absent and multiple remotes exist, require a user selection. | List candidates and obtain the remote choice. |
| Main checkout on a feature branch | Record its branch, full commit, dirty state, and baseline drift. Do not switch or modify it, and do not use its HEAD as the baseline. | After confirmation, fetch only the selected remote and resolve its default branch to a full SHA. |
| Newest default baseline | Use the selected remote’s default-branch commit after a successful fetch. | Show the fetch command and purpose per repository, obtain confirmation, fetch, and record the full SHA. |
| Fetch failure | **Stop. Do not reuse stale remote refs.** A local fallback is allowed only if the user explicitly supplies a concrete local commit and confirms it may be outdated. | Retry/fix the fetch, or obtain that explicit commit and confirmation; record the full SHA. |
| Requested branch already checked out elsewhere | Report a conflict and stop branch initialization, with no further writes. Do not duplicate, move, delete, reset, or recreate anything. | Have the user resolve the existing worktree occupancy, then rerun validation. |
| Branch-directory prefix collision | If the proposed directory’s parent or child is another branch workspace, stop before writing. Do not rename or select another directory automatically. | Require an explicit noncolliding branch/workspace choice and rerun all path and overlap checks. |
```

```text
3. Existing local branch: use its current commit without reset or rebase.
4. Unique same-named branch on the selected remote: use its confirmed commit.
5. Neither exists: create from the confirmed remote default baseline.
6. Ambiguous sources: stop and ask.
```

## Criterion assessment

| Expected criterion | Assessment | Auditable basis |
|---|---|---|
| Select remote by configured value, then sole remote, then ask | **Compliant for the supplied multiple-remote case; sole-remote branch not exercised** | The fixture has multiple remotes. The response uses explicit configuration or asks; it does not state a sole-remote rule, but that is not a missing response to this input. |
| Never select conventional remote by default | **Compliant** | Explicitly rejected. |
| Record main-checkout drift without switching or using its HEAD | **Compliant as a stated decision** | Drift and state recording plus both prohibitions are retained. |
| Confirm fetch and record full SHA | **Decision-simulation compliant** | Per-repository fetch confirmation and full-SHA recording are required; no actual fetch occurred. |
| Stop on failed fetch except explicitly accepted specific stale commit | **Compliant** | Stop and narrow explicit fallback are retained. |
| Stop globally on already checked-out branch | **Compliant** | Branch initialization stops with no further writes. |
| Stop on parent/child collision without renaming | **Compliant** | Stop and no automatic rename/relocation are explicit. |

## Limits

This is an independent controlled rerun reviewed from its raw evidence, not a rewrite of the original. No concrete remote, fetch, full SHA, or worktree operation was executed. The sole-remote alternative is not demonstrated by this multiple-remote fixture.
