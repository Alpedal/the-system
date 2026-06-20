---
name: changelog-generator
description: >
  Reformat commit history. Reads git log, groups commits by conventional commit
  types, and writes or updates CHANGELOG.md automatically. No human input needed.
  Trigger: "generate changelog", "changelog", "update changelog", "/changelog".
automation_level: 100%
---

# Skill: Changelog Generator

Read and reformat the repository commit history to build a clean `CHANGELOG.md` file.

## Rules

**Command execution:**
- Use `git log --oneline` or `git log --pretty=format:"%h - %an, %ar : %s"` to extract the commits.
- Identify either all commits since the last release tag (using `git describe --tags --abbrev=0` to get the last tag) or since the beginning of the repository if no tag exists.

**Categorization & Grouping:**
- Scan commit subjects for conventional commit prefixes:
  - `feat`: Features
  - `fix`: Bug Fixes
  - `perf`: Performance Improvements
  - `docs`: Documentation
  - `test`: Test Changes
  - `refactor`: Refactoring Changes
  - `chore`/`build`/`ci`: Operations and Tooling Changes
- Group commits under Markdown headers corresponding to these categories.
- If a commit contains a scope, include it in bold, e.g. `* **api**: add endpoints for agents`.
- If a commit has a `BREAKING CHANGE` or `!` suffix in type, highlight it with a warning block.

**File Generation:**
- Write the output to `CHANGELOG.md` at the root of the workspace.
- Include a timestamp and release version title (e.g. `## [Unreleased] - YYYY-MM-DD`).
- Preserve any existing changelog entries below the newly added section.
- Output ONLY the finished `CHANGELOG.md` diff or code block.
