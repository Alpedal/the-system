# changelog-generator

Automatic conventional CHANGELOG writer.

## What it does
Reads git history (using `git log`), parses commits according to Conventional Commits format, groups them by categories (Features, Bug Fixes, Documentation, performance, etc.), and writes the result to `CHANGELOG.md`.

## Automation Level
- **100% Autonomous**: Runs fully without human intervention. Re-formats commit history automatically.

## How to invoke
```
/changelog-generator
```

Also triggers on phrases like "generate changelog", "changelog", "update changelog", or "/changelog".
