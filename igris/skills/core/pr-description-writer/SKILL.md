---
name: pr-description-writer
description: >
  Drafts PR descriptions from branch diffs. Requires human input for business
  context (85% automation).
  Trigger: "write PR description", "generate pull request", "PR description", "/pr".
automation_level: 85%
---

# Skill: PR Description Writer

Generate a comprehensive Pull Request description by comparing the active feature branch with the target branch.

## Rules

**Command execution:**
- Identify the target branch (usually `main` or `master`) and the current feature branch.
- Execute `git diff main...HEAD` to review all branch changes.

**PR Description Structure:**
- **Title**: A clean conventional title representing the PR, e.g. `feat(web): integrate websockets for real-time gpu status`.
- **Overview**: A bulleted list summarizing the key additions, bug fixes, or modifications.
- **Business Context (Crucial)**: Include a placeholder heading: `## Why are we building this? [Requires User Input]`. Prompt the user to provide the business reason (avsikt/varför) which isn't visible in the code changes.
- **Testing Checklist**:
  - `[ ]` Automated tests written & passing
  - `[ ]` Manual verification completed
- **File Changes Summary**: List key files modified and the purpose of each modification.

**Human-in-the-loop Validation:**
- Present the draft description to the user.
- Explicitly ask the user to fill out the business context placeholder before submitting the PR.
