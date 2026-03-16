# {{PROJECT_NAME}} — Coding Standards

> **Note to agent:** This file was scaffolded by Shamt initialization. Replace all sections with standards researched from the actual codebase. Look at existing code style, linting configs, test patterns, and any existing standards docs.

---

## Language & Version

- **Primary language:** [e.g., Python 3.11+]
- **Style guide:** [e.g., PEP 8 / Google Style / project-specific]
- **Linter/formatter:** [e.g., ruff, black, eslint]

---

## File & Module Organization

[Describe how files and modules should be organized. Include:]
- Import ordering conventions
- Where to put new modules
- File naming conventions

---

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Variables | [e.g., snake_case] | `player_score` |
| Functions | [e.g., snake_case] | `calculate_score()` |
| Classes | [e.g., PascalCase] | `PlayerStats` |
| Constants | [e.g., UPPER_SNAKE] | `MAX_PLAYERS` |
| Files | [e.g., snake_case] | `player_stats.py` |

---

## Error Handling

[Describe the project's error handling approach:]
- When to use exceptions vs. return codes
- Custom exception classes (if any)
- Logging errors

---

## Logging

- **Library:** [e.g., Python logging / winston]
- **Log levels:** [how each level is used]
- **Format:** [log message format]

---

## Testing Standards

- **Framework:** [e.g., pytest, jest]
- **Required coverage:** 100% pass rate before commits
- **Test file naming:** [e.g., `test_*.py`]
- **Test organization:** [e.g., mirrors source structure]
- **What to test:** [unit vs integration vs e2e policy]

---

## Documentation Standards

- **Docstrings:** Not added to implemented code. Use clear function and parameter naming instead. *Override this default below if this project is a library with a published API and an established docstring convention (e.g., Google-style, NumPy-style).*
- **Comments:** Not added to implemented code. Exceptions: license/copyright headers at the top of files; tool-required inline markers (e.g., `# type: ignore`, `# noqa`, `// eslint-disable-next-line`); config files where comments serve as the documentation format (e.g., `.env.example`, nginx configs). *Override below if this project requires comments in specific contexts.*
- **Type hints:** [required? partial? — fill in from codebase]

---

## Git Conventions

- **Branch format:** `{work_type}/{{EPIC_TAG}}-{N}` (epic, feat, fix)
- **Commit format:** `{commit_type}/{{EPIC_TAG}}-{N}: {message}`
- **Commit title max:** 100 characters
- **No AI attribution** in commit messages

---

## Performance & Security

[Document any project-specific performance or security rules:]
- Known bottlenecks to avoid
- Security patterns required (input validation, auth, etc.)
- Prohibited patterns

---

*Last updated by Shamt initialization agent. Agents: keep this file current as standards evolve.*
