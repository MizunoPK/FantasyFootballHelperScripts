# Pre-commit Validation Protocol

**Purpose:** Ensure code quality before every commit.

**Related:** [README.md](README.md) - Protocol index

---


**Execute:** At completion of EVERY phase, step, or significant change.

**When to Execute:**
- After completing ANY phase step
- Before moving to the next phase or step
- When instructed to "validate and commit" or "commit changes"
- At any major milestone or completion point
- Before asking user for validation to proceed

**Steps:**

**1. Run Unit Tests (MANDATORY)**

```bash
python tests/run_all_tests.py
```

- 100% pass rate required
- Exit code 0 = safe to commit
- Exit code 1 = DO NOT COMMIT

**2. Analyze Changes**

```bash
git status
git diff
```

- Review ALL changed files
- Understand impact of changes

**3. Add/Update Unit Tests**

- Add tests for new functionality in `tests/` directory
- Follow test structure: `tests/module_path/test_FileName.py`
- Use proper mocking to isolate functionality
- Ensure tests follow Arrange-Act-Assert pattern

**Algorithm Behavior Tests (CRITICAL):**
- For each algorithm/calculation in the spec, write tests that verify:
  - The calculation produces expected output for known inputs
  - Conditional logic works correctly (test both branches)
  - Edge cases are handled as specified
- **Structure tests don't catch algorithm bugs** - a file can exist with wrong logic
- Write tests that would FAIL if the algorithm is implemented incorrectly

**4. Manual Testing (if applicable)**

```bash
python run_league_helper.py   # League helper mode
python run_player_fetcher.py  # Player data fetcher
python run_simulation.py      # Simulation system
```

**5. Update Documentation**
- Update README.md if functionality changed
- Update CLAUDE.md if workflow or architecture changed
- Update module-specific documentation as needed

**6. Commit Standards**
- Format: "Brief description of change"
- Keep under 50 characters when possible
- NO emojis or icons
- Do NOT include "Generated with Claude Code" footer

