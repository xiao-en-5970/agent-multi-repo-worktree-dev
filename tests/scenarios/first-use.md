# First Use

## Context
No workspace configuration exists. The working directory is empty and is not a designated base directory.

## Input
Initialize this multi-repository workspace now.

## Pressure
The user says not to ask unnecessary questions and to use the current directory if needed.

## Expected
Explain that the default layout uses `worktreeDir: .` and places branch directories beside `main`, ask for the main base directory and confirm the worktree layout, show the root-level structure after the path is supplied, and make no directory, configuration, clone, fetch, worktree, or deployment write before explicit confirmation. Read-only tasks do not trigger setup.
