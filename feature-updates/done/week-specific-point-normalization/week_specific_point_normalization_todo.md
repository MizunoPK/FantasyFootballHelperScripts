# Week-Specific Point Normalization - Implementation TODO

## Iteration Progress Tracker

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [ ]1 [ ]2 [ ]3 [ ]4 [ ]5 [ ]6 [ ]7 | 0/7 |
| Second (9) | [ ]8 [ ]9 [ ]10 [ ]11 [ ]12 [ ]13 [ ]14 [ ]15 [ ]16 | 0/9 |
| Third (8) | [ ]17 [ ]18 [ ]19 [ ]20 [ ]21 [ ]22 [ ]23 [ ]24 | 0/8 |

**Current Iteration:** 1

---

## Protocol Execution Tracker

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [ ]1 [ ]2 [ ]3 [ ]8 [ ]9 [ ]10 [ ]15 [ ]16 |
| Algorithm Traceability | 4, 11, 19 | [ ]4 [ ]11 [ ]19 |
| End-to-End Data Flow | 5, 12 | [ ]5 [ ]12 |
| Skeptical Re-verification | 6, 13, 22 | [ ]6 [ ]13 [ ]22 |
| Integration Gap Check | 7, 14, 23 | [ ]7 [ ]14 [ ]23 |
| Fresh Eyes Review | 17, 18 | [ ]17 [ ]18 |
| Edge Case Verification | 20 | [ ]20 |
| Test Coverage Planning | 21 | [ ]21 |
| Implementation Readiness | 24 | [ ]24 |

---

## Verification Summary

- Iterations completed: 0/24
- Requirements from spec: 6 main tasks
- Requirements in TODO: 6 main tasks
- Questions for user: 0 (all resolved in planning)
- Integration points identified: 2 (ConfigManager merge, ResultsManager classification)

---

## Phase 1: Configuration File Changes

### Task 1.1: Remove NORMALIZATION_MAX_SCALE from league_config.json
- **File:** `data/configs/league_config.json`
- **Action:** Remove line 8: `"NORMALIZATION_MAX_SCALE": 163,`
- **Tests:** Existing tests may fail until week configs updated
- **Status:** [ ] Not started

### Task 1.2: Add NORMALIZATION_MAX_SCALE to week1-5.json
- **File:** `data/configs/week1-5.json`
- **Action:** Add `"NORMALIZATION_MAX_SCALE": 163` to parameters section
- **Status:** [ ] Not started

### Task 1.3: Add NORMALIZATION_MAX_SCALE to week6-9.json
- **File:** `data/configs/week6-9.json`
- **Action:** Add `"NORMALIZATION_MAX_SCALE": 153` to parameters section
- **Status:** [ ] Not started

### Task 1.4: Add NORMALIZATION_MAX_SCALE to week10-13.json
- **File:** `data/configs/week10-13.json`
- **Action:** Add `"NORMALIZATION_MAX_SCALE": 143` to parameters section
- **Status:** [ ] Not started

### Task 1.5: Add NORMALIZATION_MAX_SCALE to week14-17.json
- **File:** `data/configs/week14-17.json`
- **Action:** Add `"NORMALIZATION_MAX_SCALE": 133` to parameters section
- **Status:** [ ] Not started

---

## Phase 2: Simulation Code Changes

### Task 2.1: Move NORMALIZATION_MAX_SCALE to WEEK_SPECIFIC_PARAMS
- **File:** `simulation/ResultsManager.py`
- **Action:**
  - Remove `'NORMALIZATION_MAX_SCALE'` from `BASE_CONFIG_PARAMS` (line 242)
  - Add `'NORMALIZATION_MAX_SCALE'` to `WEEK_SPECIFIC_PARAMS` (line 255)
- **Impact:** ConfigGenerator.is_base_param() and is_week_specific_param() will automatically update
- **Tests:** `tests/simulation/test_ResultsManager.py`, `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

---

## Phase 3: Test Fixture Updates

### Task 3.1: Identify all test files with NORMALIZATION_MAX_SCALE in mock configs
- **Count:** ~47 references across ~24 files
- **Pattern:** Most use `"NORMALIZATION_MAX_SCALE": 100.0` in mock configs
- **Status:** [ ] Not started

### Task 3.2: Update test fixtures
- **Files to update:**
  - `tests/simulation/test_simulation_manager.py`
  - `tests/simulation/test_ResultsManager.py`
  - `tests/simulation/test_config_generator.py`
  - `tests/integration/test_league_helper_integration.py`
  - `tests/integration/test_simulation_integration.py`
  - `tests/integration/test_game_conditions_integration.py`
  - `tests/league_helper/util/test_ConfigManager_*.py`
  - `tests/league_helper/util/test_PlayerManager_scoring.py`
  - `tests/league_helper/util/test_player_scoring.py`
  - `tests/league_helper/util/test_FantasyTeam.py`
  - `tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py`
  - `tests/league_helper/reserve_assessment_mode/test_ReserveAssessmentModeManager.py`
  - `tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py`
- **Status:** [ ] Not started

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| Week config NORMALIZATION_MAX_SCALE | week{N}-{M}.json | ConfigManager._load_week_config() | ConfigManager.py:261 | No change needed |
| WEEK_SPECIFIC_PARAMS update | ResultsManager.py | ConfigGenerator.is_week_specific_param() | ConfigGenerator.py:281 | Automatic (uses constant) |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Decision 1 | Remove from base config | league_config.json:8 | N/A - file edit |
| Decision 2 | Week-specific values | week{N}-{M}.json | N/A - file edit |
| Decision 3 | Move to WEEK_SPECIFIC_PARAMS | ResultsManager.py:242,255 | N/A - list membership |

---

## Data Flow Traces

### Requirement: Load NORMALIZATION_MAX_SCALE from week config
```
Entry: run_league_helper.py
  → LeagueHelperManager.__init__()
  → ConfigManager.__init__(data_folder)
  → ConfigManager._load_config()
  → ConfigManager._load_week_config(week)  # Loads week{N}-{M}.json
  → parameters.update(week_params)  # Merges NORMALIZATION_MAX_SCALE
  → ConfigManager._extract_parameters()
  → self.normalization_max_scale = self.parameters[NORMALIZATION_MAX_SCALE]
  → Output: normalization_max_scale set from week config
```

### Requirement: Simulation saves NORMALIZATION_MAX_SCALE to week configs
```
Entry: run_simulation.py
  → SimulationManager
  → ResultsManager.save_optimal_configs_folder()
  → ResultsManager._extract_week_params()  # Uses WEEK_SPECIFIC_PARAMS
  → NORMALIZATION_MAX_SCALE included in week config output
  → Output: week{N}-{M}.json files with NORMALIZATION_MAX_SCALE
```

---

## Edge Cases

1. **Legacy single-file config:** Tests that use legacy structure need NORMALIZATION_MAX_SCALE in their mock config
2. **Missing week config:** ConfigManager logs warning, validation will fail without NORMALIZATION_MAX_SCALE
3. **Simulation folder loading:** ConfigGenerator.load_baseline_from_folder() should pick up week-specific values

---

## Progress Notes

**Last Updated:** 2025-12-13
**Current Status:** TODO file created, starting verification iterations
**Next Steps:** Execute iterations 1-7
**Blockers:** None
