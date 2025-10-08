# General Updates - Clarifying Questions

## Overview
Before proceeding with the 13 objectives outlined in `general_updates.txt`, I need clarification on several points to ensure proper implementation.

---

## Questions by Objective

### Objective 1: Move parameters.json to shared_files/parameters/
**Status**: Already in progress - file moved, need to update all references

**Questions**:
1. Should `shared_files/parameters/` contain ONLY the production `parameters.json`, or should simulation-related JSONs also go here?
   - Currently simulation has `draft_helper/simulation/parameters/` with subdirectories for `parameter_sets/` and `parameter_runs/`
   - Should these stay in simulation folder or consolidate into `shared_files/parameters/`?

---

### Objective 2: Move CSV files to shared_files/data/
**Questions**:
1. Should `shared_files/data/` contain:
   - Only `players.csv`, `teams.csv`, `bye_weeks.csv`? OR
   - Also include other data files currently in various module `/data/` folders?

2. What about module-specific data folders (e.g., `player-data-fetcher/data/`, `draft_helper/data/`, `starter_helper/data/`)?
   - Should these stay as module-specific output directories?
   - Or should everything consolidate into `shared_files/data/`?

---

### Objective 3: Static test CSV files
**Questions**:
1. Where should static test CSV fixtures be stored?
   - In each module's `tests/fixtures/` directory? OR
   - In a central `tests/fixtures/` at repo root?

2. Should we create "frozen" copies of current CSV files for tests?
   - E.g., `tests/fixtures/players_baseline.csv` with known data
   - This prevents tests from breaking when you update real data files

---

### Objective 4: Parameter verification in draft helper
**Questions**:
1. What level of verification is needed?
   - Manual testing through draft helper menu? OR
   - Automated integration tests that verify parameter impact? OR
   - Both?

2. Should I create new integration tests specifically for parameter validation?

---

### Objective 5: Consolidate starter_helper into draft_helper
**Questions**:
1. File structure after consolidation:
   ```
   draft_helper/
   ├── core/              # existing scoring engine, etc.
   ├── starter/           # NEW - move starter_helper code here?
   │   ├── lineup_optimizer.py
   │   ├── matchup_calculator.py
   │   └── tests/
   ├── simulation/        # existing
   └── tests/             # existing
   ```
   Is this structure acceptable?

2. Config consolidation:
   - Merge `starter_helper_config.py` into `draft_helper_config.py`? OR
   - Keep separate sections within the same file?

3. Entry points:
   - Keep `run_starter_helper.py` at root, but have it call draft_helper's starter module? OR
   - Remove `run_starter_helper.py` entirely and only access via draft helper menu?

---

### Objective 6-8: Test updates
**Questions**:
1. For unit test improvements (Objective 6):
   - What specific areas need more coverage?
   - Any known edge cases to address?

2. For integration tests (Objective 7):
   - Current automated integration test covers 23 steps - is this sufficient?
   - Should starter_helper integration tests be added?

---

### Objective 9: Improve draft helper modularity
**Questions**:
1. What specific modularity issues have you noticed?
   - Is `draft_helper.py` too large (1100+ lines)?
   - Should menu system be separated from core logic?

2. Priorities for modularity improvements?

---

### Objective 10: Consolidate config files
**Questions**:
1. How consolidated should configs be?
   - Option A: Single `config.py` with sections for each module
   - Option B: Keep `shared_config.py` + `draft_helper_config.py` (merge starter into draft)
   - Option C: Something else?

2. Should simulation config stay separate or consolidate as well?

---

### Objective 11: Improve logging
**Questions**:
1. What logging improvements are needed?
   - More detailed logging in certain areas?
   - Better log level organization?
   - Consolidated logging configuration?

2. Any specific areas where logging is insufficient?

---

### Objective 12: Improve documentation
**Questions**:
1. Which documentation needs updates?
   - CLAUDE.md (technical reference)
   - Module-level README files
   - Code comments/docstrings
   - All of the above?

2. Any specific documentation gaps you've noticed?

---

### Objective 13: Verify parameter loading
**Questions**:
1. This overlaps with Objective 4 - should they be combined?

2. Verification scope:
   - Just verify parameters load without errors? OR
   - Verify parameters actually impact scoring calculations? OR
   - Both?

---

## General Questions

1. **Order of execution**: The instructions say "in whatever order you deam best" - do you have preferences for which objectives to tackle first?

2. **Commit frequency**: Should I commit after EACH objective (13 commits) or group related objectives together?

3. **Breaking changes**: Some of these changes (like file moves) could break external scripts or workflows. Are there any external dependencies I should be aware of?

4. **Backwards compatibility**: Should old file paths continue to work (symlinks?), or is it okay to require updates everywhere?

---

## Summary
Please answer the questions above so I can create a comprehensive TODO file and proceed systematically with implementation.
