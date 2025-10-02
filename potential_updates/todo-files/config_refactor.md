# Config Refactor - TODO

**Objective**: Centralize config files to `shared_files/configs/` subdirectory

**Date Created**: 2025-10-01
**Status**: In Progress
**Progress Tracking**: Update this file after completing each step

---

## Summary

Move config files from scattered locations to centralized `shared_files/configs/` directory:
- Move 5 config files to new location
- Move `DEFAULT_SCORING_CONFIG` from `enhanced_scoring.py` to `shared_config.py` and rename to `ENHANCED_SCORING_CONFIG`
- Update ~30 import statements across the codebase
- Validate with full test suite and integration tests at each phase

**Files to Move**:
1. `shared_config.py` → `shared_files/configs/shared_config.py`
2. `nfl-scores-fetcher/nfl_scores_fetcher_config.py` → `shared_files/configs/nfl_scores_fetcher_config.py`
3. `player-data-fetcher/player_data_fetcher_config.py` → `shared_files/configs/player_data_fetcher_config.py`
4. `draft_helper/draft_helper_config.py` → `shared_files/configs/draft_helper_config.py`
5. `starter_helper/starter_helper_config.py` → `shared_files/configs/starter_helper_config.py`

**Not Moving** (as per user answers):
- `draft_helper/simulation/config.py` (simulation-specific)
- Test config files
- `config_optimizer.py` (not a config file)

---

## Phase 1: Setup and Preparation

### Step 1.1: Create configs directory
- [ ] Create `shared_files/configs/` directory
- [ ] Create `shared_files/configs/__init__.py` (empty for Python package)

### Step 1.2: Move DEFAULT_SCORING_CONFIG to shared_config.py
- [ ] Read `shared_files/enhanced_scoring.py` to get full `DEFAULT_SCORING_CONFIG` dictionary
- [ ] Add `ENHANCED_SCORING_CONFIG` to `shared_config.py` (root level, will be moved in Phase 2)
- [ ] Update `enhanced_scoring.py` to import from `shared_config`:
  ```python
  from shared_config import ENHANCED_SCORING_CONFIG as DEFAULT_SCORING_CONFIG
  ```
- [ ] Run unit tests for `shared_files/tests/test_enhanced_scoring.py` to verify no breakage

### Step 1.3: Validate Phase 1
- [ ] **MANDATORY PRE-COMMIT VALIDATION PROTOCOL**
  - [ ] Copy validation checklist: `cp tests/pre_commit_validation_checklist.md tests/temp_commit_checklist.md`
  - [ ] Step 1: Analyze changes with `git status` and `git diff`
  - [ ] Step 2: Add/update unit tests if needed
  - [ ] Step 3: Run full test suite: `python -m pytest --tb=short` (100% pass required)
  - [ ] Step 4: Execute full integration testing (23 draft helper validation steps)
  - [ ] Step 5: Update documentation if needed
  - [ ] Step 6: Commit changes: "Complete Phase 1: Move DEFAULT_SCORING_CONFIG to shared_config"
  - [ ] Step 7: Cleanup: `rm tests/temp_commit_checklist.md tests/temp_integration_checklist.md`

---

## Phase 2: Move Config Files

### Step 2.1: Move shared_config.py
- [ ] Move `shared_config.py` to `shared_files/configs/shared_config.py`
- [ ] Update imports in files that use `shared_config`:
  - [ ] `draft_helper/simulation/season_simulator.py`
  - [ ] `starter_helper/starter_helper_config.py`
  - [ ] `draft_helper/draft_helper.py`
  - [ ] `draft_helper/core/scoring_engine.py`
  - [ ] `player-data-fetcher/player_data_fetcher_config.py`
  - [ ] `shared_files/data_file_manager.py`
  - [ ] `nfl-scores-fetcher/nfl_scores_fetcher_config.py`
  - [ ] `nfl-scores-fetcher/nfl_scores_exporter.py`
  - [ ] `player-data-fetcher/player_data_exporter.py`
  - [ ] `player-data-fetcher/espn_client.py`
- [ ] Update `enhanced_scoring.py` import to: `from shared_files.configs.shared_config import ENHANCED_SCORING_CONFIG`

### Step 2.2: Move draft_helper_config.py
- [ ] Move `draft_helper/draft_helper_config.py` to `shared_files/configs/draft_helper_config.py`
- [ ] Update imports in files that use `draft_helper_config`:
  - [ ] `draft_helper/tests/test_draft_helper.py`
  - [ ] `draft_helper/simulation/simulation_engine.py`
  - [ ] `draft_helper/simulation/team_strategies.py`
  - [ ] `draft_helper/simulation/config_optimizer.py`
  - [ ] `draft_helper/draft_helper_constants.py`
  - [ ] `draft_helper/core/scoring_engine.py`

### Step 2.3: Move starter_helper_config.py
- [ ] Move `starter_helper/starter_helper_config.py` to `shared_files/configs/starter_helper_config.py`
- [ ] Update imports in files that use `starter_helper_config`:
  - [ ] `starter_helper/lineup_optimizer.py`
  - [ ] `starter_helper/matchup_calculator.py`
  - [ ] `starter_helper/tests/test_lineup_optimizer.py`
  - [ ] `starter_helper/tests/test_matchup_calculator.py`
  - [ ] `draft_helper/draft_helper.py`
  - [ ] `starter_helper/starter_helper.py`
  - [ ] `starter_helper/espn_current_week_client.py`
  - [ ] `starter_helper/tests/test_starter_helper.py`

### Step 2.4: Move player_data_fetcher_config.py
- [ ] Move `player-data-fetcher/player_data_fetcher_config.py` to `shared_files/configs/player_data_fetcher_config.py`
- [ ] Update imports in files that use `player_data_fetcher_config`:
  - [ ] `player-data-fetcher/tests/test_data_fetcher_players.py`
  - [ ] `player-data-fetcher/data_fetcher-players.py`
  - [ ] `player-data-fetcher/espn_client.py`
  - [ ] `player-data-fetcher/player_data_constants.py`
  - [ ] `player-data-fetcher/tests/test_enhanced_data_collection.py`
  - [ ] `player-data-fetcher/tests/test_drafted_data_loader.py`

### Step 2.5: Move nfl_scores_fetcher_config.py
- [ ] Move `nfl-scores-fetcher/nfl_scores_fetcher_config.py` to `shared_files/configs/nfl_scores_fetcher_config.py`
- [ ] Update imports in files that use `nfl_scores_fetcher_config`:
  - [ ] `nfl-scores-fetcher/scores_constants.py`
  - [ ] `nfl-scores-fetcher/data_fetcher-scores.py`

### Step 2.6: Validate Phase 2
- [ ] **MANDATORY PRE-COMMIT VALIDATION PROTOCOL**
  - [ ] Copy validation checklist: `cp tests/pre_commit_validation_checklist.md tests/temp_commit_checklist.md`
  - [ ] Step 1: Analyze changes with `git status` and `git diff`
  - [ ] Step 2: Add/update unit tests if needed
  - [ ] Step 3: Run full test suite: `python -m pytest --tb=short` (100% pass required)
  - [ ] Step 4: Execute startup validation:
    - [ ] `timeout 10 python run_player_data_fetcher.py`
    - [ ] `timeout 10 python run_nfl_scores_fetcher.py`
  - [ ] Step 5: Execute full integration testing (23 draft helper validation steps)
  - [ ] Step 6: Update documentation if needed
  - [ ] Step 7: Commit changes: "Complete Phase 2: Move all config files to shared_files/configs"
  - [ ] Step 8: Cleanup: `rm tests/temp_commit_checklist.md tests/temp_integration_checklist.md`

---

## Phase 3: Documentation and Cleanup

### Step 3.1: Update CLAUDE.md
- [ ] Update config file locations in CLAUDE.md
- [ ] Update import examples to reflect new paths
- [ ] Update "File Structure" section to show `shared_files/configs/` directory
- [ ] Update any mentions of config file locations

### Step 3.2: Update README files
- [ ] Check if any module README files mention config locations
- [ ] Update references to new config paths

### Step 3.3: Verify no orphaned files
- [ ] Confirm old config files are deleted (not just moved, actually deleted)
- [ ] Run `find . -name "*_config.py" -type f` to verify only configs in proper locations remain
- [ ] Check for any missed import references to old paths

### Step 3.4: Final Validation
- [ ] **MANDATORY PRE-COMMIT VALIDATION PROTOCOL**
  - [ ] Copy validation checklist: `cp tests/pre_commit_validation_checklist.md tests/temp_commit_checklist.md`
  - [ ] Step 1: Analyze changes with `git status` and `git diff`
  - [ ] Step 2: Verify no new unit tests needed
  - [ ] Step 3: Run full test suite: `python -m pytest --tb=short` (100% pass required)
  - [ ] Step 4: Execute startup validation:
    - [ ] `timeout 10 python run_player_data_fetcher.py`
    - [ ] `timeout 10 python run_nfl_scores_fetcher.py`
    - [ ] `timeout 10 python run_starter_helper.py`
  - [ ] Step 5: Execute full integration testing (23 draft helper validation steps)
  - [ ] Step 6: Commit documentation updates: "Complete Phase 3: Update documentation for config refactor"
  - [ ] Step 7: Cleanup: `rm tests/temp_commit_checklist.md tests/temp_integration_checklist.md`

---

## Phase 4: Completion

### Step 4.1: Final Review
- [ ] Review all changes made
- [ ] Confirm all imports updated correctly
- [ ] Confirm all tests passing (100%)
- [ ] Confirm all scripts start without errors

### Step 4.2: Move to Done
- [ ] Move `potential_updates/config_refactor.txt` to `potential_updates/done/`
- [ ] Delete `potential_updates/config_refactor_questions.md`
- [ ] Delete this TODO file

---

## Import Pattern Reference

**Old Pattern**:
```python
from shared_config import CURRENT_NFL_WEEK
from draft_helper.draft_helper_config import MAX_POSITIONS
from starter_helper.starter_helper_config import MATCHUP_MULTIPLIERS
from player_data_fetcher_config import SKIP_DRAFTED_PLAYER_UPDATES
from nfl_scores_fetcher_config import NFL_SCORES_API_URL
```

**New Pattern**:
```python
from shared_files.configs.shared_config import CURRENT_NFL_WEEK, ENHANCED_SCORING_CONFIG
from shared_files.configs.draft_helper_config import MAX_POSITIONS
from shared_files.configs.starter_helper_config import MATCHUP_MULTIPLIERS
from shared_files.configs.player_data_fetcher_config import SKIP_DRAFTED_PLAYER_UPDATES
from shared_files.configs.nfl_scores_fetcher_config import NFL_SCORES_API_URL
```

---

## Notes

- **CRITICAL**: Execute pre-commit validation protocol at the end of EVERY phase
- **CRITICAL**: All tests must pass (100%) before proceeding to next phase
- **CRITICAL**: Update this TODO file after completing each step to track progress
- Keep repository functional after each phase completion
- Test all scripts after each phase to ensure nothing broke
- Simulation configs intentionally NOT moved per user preference
- Test configs intentionally NOT moved per user preference
- No backward compatibility needed per user preference

---

## Estimated Scope

- **Config files to move**: 5 files
- **Import statements to update**: ~30 files
- **Phases**: 4 phases, each with validation
- **Estimated time**: 2-3 hours with full testing
