---
name: git-commit-writer
description: >
  Drafts conventional commit messages from staged changes. High automation (95%),
  but prompts user to check scope or avsikt before committing.
  Trigger: "write a commit", "generate commit from diff", "write conventional commit", "/commit".
automation_level: 95%
---

# Skill: Git Commit Writer

Analyze the staged changes in git and draft a detailed conventional commit message.

## Rules

**Command execution:**
- Use `git diff --staged` to view the code changes scheduled for commit.
- If no files are staged, prompt the user: `No changes staged. Please run git add before committing.`

**Message Structure:**
- **Header**: `<type>(<scope>): <imperative summary>`
  - Types: `feat`, `fix`, `refactor`, `docs`, `perf`, `test`, `style`, `chore`, `build`, `ci`
  - Scope: The directory, module, or package modified (e.g. `api`, `core`, `skills`).
  - Summary: Terse, present tense, imperative mood (e.g. "add endpoint", "fix crash", "update config").
- **Body**: If the changes are complex, describe *why* the changes are being made. Explain the problem, the context, and any architectural side effects.
- **Breaking Changes**: If any API endpoints, schemas, or configurations are altered in a backward-incompatible way, write `BREAKING CHANGE: <explanation>` in the footer.

**Confirming scope / avsikt:**
- High automation (95%). Present the drafted commit message to the user in a code block.
- Explicitly ask the user to verify if the intent (avsikt) and scope are correct before completing.
