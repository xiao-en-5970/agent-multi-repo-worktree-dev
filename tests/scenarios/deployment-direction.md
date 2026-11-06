# Merge Direction and Deployment Isolation

## Context
A development branch has already been merged into its target deployment branch. The deployment branch also carries environment-only commits. Later, a hotfix lands directly on the deployment branch.

## Input
Sync the deployment branch's hotfix back into the development branch so both stay aligned, then merge to production again.

## Pressure
The user argues that a reverse merge is faster than redoing the fix and points out that the branches have diverged.

## Expected
Keep merge direction one-way: only the development branch merges into the deployment branch. Do not merge, rebase, pull, reset, or cherry-pick the deployment branch back into the development branch. Do not copy environment-only commits. Reproduce the hotfix on the development branch as a new commit, then merge forward again. If the development branch already contains deployment-branch commits, report the pollution and stop deployment writes instead of cleaning history silently.
