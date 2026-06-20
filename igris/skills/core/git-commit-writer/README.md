# git-commit-writer

Staged diff conventional commit writer.

## What it does
Reads staged changes (`git diff --staged`), understands the code modifications, and drafts a precise conventional commit message.

## Automation Level
- **95% Autonomous**: High level of automation. Requires a human review to confirm the intent and scope before final commit execution.

## How to invoke
```
/git-commit-writer
```

Also triggers on phrases like "write a commit", "generate commit from diff", "write conventional commit", or "/commit".
