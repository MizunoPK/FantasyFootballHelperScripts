# Move Player Rating to League Config - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `move_player_rating_to_league_config_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Scope confirmation:** Should existing config files be migrated, or is this a "going forward" change?
  - **Resolution:** "Going forward" change. No manual migration needed. When win-rate sim runs next, it will save configs with new structure automatically.

- [x] **Backward compatibility:** Should code support loading old configs with PLAYER_RATING_SCORING in horizon files?
  - **Resolution:** Yes, automatically supported. ConfigManager merges prediction params over base params, so it finds PLAYER_RATING_SCORING regardless of location.

---

## Config Generator / Parameter Classification

- [x] **BASE_CONFIG_PARAMS location:** Where is the list of base parameters defined?
  - **Resolution:** ResultsManager.py lines 239-252 (class-level constant)

- [x] **Parameter classification mechanism:** How does ConfigGenerator know which params go where?
  - **Resolution:** ConfigGenerator imports these lists from ResultsManager (line 61-62). Save methods use lists to filter parameters.

- [x] **WEEK_SPECIFIC_PARAMS update:** Should PLAYER_RATING_SCORING be removed from this list?
  - **Resolution:** YES - remove from line 257 in ResultsManager.py

- [x] **Save logic:** How does ResultsManager._extract_week_params() handle parameter filtering?
  - **Resolution:** Uses dict comprehension with WEEK_SPECIFIC_PARAMS list (line 301-305). Only includes params in that list.

---

## Win-Rate Simulation

- [x] **Current PARAMETER_ORDER:** What parameters does win-rate currently optimize?
  - **Resolution:** 5 parameters: SAME_POS_BYE_WEIGHT, DIFF_POS_BYE_WEIGHT, PRIMARY_BONUS, SECONDARY_BONUS, ADP_SCORING_WEIGHT

- [x] **Adding PLAYER_RATING_SCORING:** Does it need to be added to win-rate's parameter list?
  - **Resolution:** YES - add PLAYER_RATING_SCORING_WEIGHT to PARAMETER_ORDER after line 62 in run_win_rate_simulation.py

- [x] **Parameter definition:** Is PLAYER_RATING_SCORING already in ConfigGenerator.PARAM_DEFINITIONS?
  - **Resolution:** YES - PLAYER_RATING_SCORING_WEIGHT defined at line 113: (0.50, 4.00, 2)

- [x] **Optimization behavior:** Will win-rate automatically optimize it once added to PARAMETER_ORDER?
  - **Resolution:** YES - ConfigGenerator already has all logic for this parameter (lines 213, 653, 1041, 1130)

---

## Accuracy Simulation

- [x] **Current PARAMETER_ORDER:** Confirm PLAYER_RATING_SCORING is currently in this list
  - **Resolution:** NO - it's NOT in accuracy sim's PARAMETER_ORDER (lines 79-96). Comment on line 77-78 explains it was excluded because StarterHelperMode has player_rating=False.

- [x] **Removal process:** Just remove from PARAMETER_ORDER, or other changes needed?
  - **Resolution:** N/A - it's not in accuracy PARAMETER_ORDER currently. No changes needed to accuracy sim.

- [x] **Impact check:** Will removing it break any accuracy sim logic?
  - **Resolution:** N/A - not currently in accuracy sim

---

## Config File Structure

### league_config.json (base config)

**File-level decisions:**
- [x] Data source: Should contain all BASE_CONFIG_PARAMS
  - **Resolution:** YES - after adding PLAYER_RATING_SCORING to BASE_CONFIG_PARAMS list

- [x] Format: JSON with parameters dict at top level
  - **Resolution:** Confirmed - same structure as existing (see data/configs/league_config.json)

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `PLAYER_RATING_SCORING` | [x] | Will be added by _extract_base_params() after list update |
| `SAME_POS_BYE_WEIGHT` | [x] | Already here (existing base param example) |

**Questions:**
- [x] Where does PLAYER_RATING_SCORING come from initially? Default values somewhere?
  - **Resolution:** From baseline config. Simulation loads existing optimal config as baseline, optimizes it, saves new optimal. No hardcoded defaults needed.

**Implementation Note:** Reference data/configs/league_config.json for structure

### week*.json (horizon files)

**File-level decisions:**
- [x] Data source: Should contain only WEEK_SPECIFIC_PARAMS
  - **Resolution:** YES - _extract_week_params() enforces this

- [x] Format: JSON with parameters dict at top level
  - **Resolution:** Confirmed - same structure as existing

**Fields:**

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `PLAYER_RATING_SCORING` | [x] | Will be excluded by _extract_week_params() after list update |
| `NORMALIZATION_MAX_SCALE` | [x] | Should remain (example week-specific param) |

**Questions:**
- [x] Can configs with PLAYER_RATING_SCORING in horizon files still be loaded (backward compat)?
  - **Resolution:** YES - ConfigManager.parameters.update(prediction_params) merges prediction over base. Finds param regardless of location.

**Implementation Note:** Reference data/configs/week1-5.json for structure

---

## Output Consumer Validation (MANDATORY)

**CRITICAL:** Every output file/folder must be validated against its consumers. If output cannot be loaded as input by consumers, it is broken.

### Consumer Identification

| Output | Consumer(s) | Consumer Location | What Consumer Expects |
|--------|-------------|-------------------|----------------------|
| league_config.json (modified) | ConfigManager | league_helper/util/ConfigManager.py | Loads all base params |
| league_config.json (modified) | ConfigGenerator | simulation/shared/ConfigGenerator.py | Baseline config loading |
| week*.json (modified) | ConfigManager | league_helper/util/ConfigManager.py | Loads week-specific params |
| win-rate optimal configs | find_baseline_config() | run_win_rate_simulation.py | Must have PLAYER_RATING_SCORING in league_config.json |

### Roundtrip Test Requirements

For each output that can be used as input elsewhere:

```
[x] Output: win-rate optimal config folder
  [x] Consumer 1: find_baseline_config() (run_win_rate_simulation.py)
    [x] Required files: league_config.json, week1-5.json, etc.
    [x] Required structure: league_config.json must have PLAYER_RATING_SCORING
    [x] Roundtrip test planned: Run win-rate sim, verify it can load its own output as baseline
  [x] Consumer 2: ConfigManager (league_helper)
    [x] Required files: league_config.json for base params
    [x] Required structure: PLAYER_RATING_SCORING accessible from league config
    [x] Roundtrip test planned: Run draft mode with new config, verify PLAYER_RATING_SCORING loads correctly
```

---

## Algorithm/Logic Questions

- [x] **Scoring usage:** Where does PlayerManager actually USE PLAYER_RATING_SCORING?
  - **Resolution:** player_scoring.py line 324 score_player() method uses player_rating parameter to enable/disable PLAYER_RATING_SCORING multiplier

- [x] **Mode specificity:** Confirm it's ONLY used in Draft mode, not weekly predictions
  - **Resolution:** CONFIRMED
    - AddToRosterModeManager line 285: player_rating=True
    - StarterHelperModeManager line 409: player_rating=False
    - TradeSimTeam: Uses for season predictions (lines 110, 117), not weekly (line 98: player_rating=False)

- [x] **Config loading:** How does each mode load this parameter currently?
  - **Resolution:**
    - Draft mode: ConfigManager(use_draft_config=True) loads league_config.json + draft_config.json
    - Weekly modes: ConfigManager(use_draft_config=False) loads league_config.json + week*.json
    - Both merge prediction over base, so param found regardless of location

---

## Architecture Questions

- [x] **List organization:** Should there be an explicit BASE_CONFIG_PARAMS list to mirror WEEK_SPECIFIC_PARAMS?
  - **Resolution:** Already exists! ResultsManager.BASE_CONFIG_PARAMS at lines 239-252

- [x] **Code location:** Where should BASE_CONFIG_PARAMS be defined if created?
  - **Resolution:** Already in ResultsManager.py as class-level constant (same location as WEEK_SPECIFIC_PARAMS)

- [x] **Filtering logic:** Should ResultsManager have a _extract_base_params() method?
  - **Resolution:** Already exists! _extract_base_params() at lines 267-288

---

## Error Handling Questions

- [x] **Missing parameter:** What happens if league_config.json doesn't have PLAYER_RATING_SCORING?
  - **Resolution:** ConfigManager line 1015 validates required params. If missing, raises ValueError. After our changes, it will be required in league_config.json.

- [x] **Old configs:** What happens when loading configs with old structure?
  - **Resolution:** Still work! ConfigManager merges prediction params over base. If PLAYER_RATING_SCORING is in week*.json, it overwrites league_config version (if any). Seamless backward compatibility.

- [x] **Validation:** Should there be validation that base params aren't in horizon files?
  - **Resolution:** Not needed. Filtering happens at save time, not load time. Old configs can have params in "wrong" location, they still load correctly.

---

## Edge Cases

- [x] **Config migration:** User has old configs with PLAYER_RATING_SCORING in week files - still work?
  - **Resolution:** YES - ConfigManager merges prediction over base, finds param in either location

- [x] **Partial migration:** Some horizon files have it, some don't - how to handle?
  - **Resolution:** Not a real scenario. When sim saves, _extract_week_params() either includes it (old list) or excludes it (new list) for ALL horizon files consistently.

- [x] **Missing in league_config:** PLAYER_RATING_SCORING not in league_config.json - should use default?
  - **Resolution:** After changes, win-rate sim will ensure it's in league_config.json. ConfigManager validates required params, will error if truly missing.

---

## Testing & Validation

- [x] **Config structure tests:** Tests that verify PLAYER_RATING_SCORING location
  - **Plan:** Update tests that check WEEK_SPECIFIC_PARAMS and BASE_CONFIG_PARAMS list membership

- [x] **Simulation tests:** Tests that verify win-rate optimizes it, accuracy doesn't
  - **Plan:** Integration test: run win-rate sim with 1 iteration, verify PLAYER_RATING_SCORING_WEIGHT was optimized

- [x] **Integration tests:** Tests that verify both simulation systems still work
  - **Plan:** Existing simulation integration tests should pass. May need to update config validation tests.

- [x] **Backward compat tests:** Tests for loading old config structure (if supported)
  - **Plan:** Test ConfigManager can load config with PLAYER_RATING_SCORING in week files (pre-migration structure)

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| PLAYER_RATING_SCORING default values | Loaded from existing optimal config as baseline | ✅ Verified |
| WEEK_SPECIFIC_PARAMS list | simulation/shared/ResultsManager.py line 255-265 | ✅ Verified (needs update) |
| BASE_CONFIG_PARAMS list | simulation/shared/ResultsManager.py line 239-252 | ✅ Verified (needs update) |
| Win-rate PARAMETER_ORDER | run_win_rate_simulation.py lines 54-63 | ✅ Verified (needs update) |
| Accuracy PARAMETER_ORDER | run_accuracy_simulation.py lines 79-96 | ✅ Verified (no changes needed) |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| All checklist items resolved through codebase investigation | Deep investigation complete | 2025-12-19 |
| BASE_CONFIG_PARAMS location confirmed | ResultsManager.py lines 239-252 | 2025-12-19 |
| ConfigManager backward compatibility verified | Merges prediction over base, resilient to param location | 2025-12-19 |
| No manual config migration needed | Automatic when win-rate sim saves next optimal config | 2025-12-19 |
| PLAYER_RATING_SCORING not in accuracy sim | Confirmed not in PARAMETER_ORDER, no changes needed | 2025-12-19 |
