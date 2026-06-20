# pr-description-writer

Pull Request description writer.

## What it does
Compares the active feature branch with the target branch (`git diff main...feature`) and drafts a descriptive Pull Request description.

## Automation Level
- **85% Autonomous**: Requires human input to fill out business context ("Why are we building this?") that cannot be deduced from code diffs alone.

## How to invoke
```
/pr-description-writer
```

Also triggers on phrases like "write PR description", "generate pull request", "PR description", or "/pr".
