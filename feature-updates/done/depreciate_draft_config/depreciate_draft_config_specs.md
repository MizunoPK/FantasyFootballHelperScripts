# Depreciate draft_config.json Specification

## Objective

Remove `draft_config.json` from the Fantasy Football Helper system and consolidate draft-specific configuration into `league_config.json`. Research has shown that only `NORMALIZATION_MAX_SCALE` has meaningful impact on draft recommendations, making a separate draft configuration file unnecessary complexity.

---

## High-Level Requirements

### 1. Configuration Changes

**Add to league_config.json:**
- New parameter: `DRAFT_NORMALIZATION_MAX_SCALE`
- Purpose: Draft-specific normalization scaling (replaces value from draft_config.json)
- ConfigManager must be updated to read this parameter

**Remove from system:**
- `draft_config.json` file usage in all modes
- ROS configuration concept from accuracy simulation
- Multiple ConfigManager instance pattern

### 2. Scoring Logic Changes

**Update score_player() method:**
- Detect when running in "draft mode" (Add to Roster mode)
- When in draft mode: use `DRAFT_NORMALIZATION_MAX_SCALE`
- When not in draft mode: use standard `NORMALIZATION_MAX_SCALE`
- No other scoring changes needed

### 3. Add to Roster Mode Simplification

**Current behavior:**
- Uses draft_config.json for scoring

**New behavior:**
- Use `league_config.json` for base configuration
- Use weekly config file based on `CURRENT_NFL_WEEK`
- Use `DRAFT_NORMALIZATION_MAX_SCALE` parameter for draft-specific normalization
- Revert to single ConfigManager instance

### 4. Accuracy Simulation Changes

**Remove:**
- ROS (Rest of Season) accuracy assessment
- draft_config.json optimization
- ROS-related file output (draft_config.json from optimal folders)

**Keep:**
- Weekly accuracy assessment only (weeks 1-5, 6-9, 10-13, 14-17)
- 4 weekly horizon outputs in accuracy_optimal folders
- league_config.json in output folders (for base/strategy params)

### 5. Win-Rate Simulation Changes

**Remove:**
- draft_config.json creation/updating
- ROS optimization logic

**Add:**
- Test `DRAFT_NORMALIZATION_MAX_SCALE` parameter
- Update in league_config.json (not separate file)

**Keep:**
- All other simulation functionality unchanged

---

## Detailed Requirements

### Configuration File Structure

**league_config.json additions:**
```json
{
  "NORMALIZATION_SCORING": {
    "MAX_SCALE": 50.0,
    "DRAFT_MAX_SCALE": 55.0  // NEW - used during draft mode
  }
}
```

### Draft Mode Detection

**Methods to consider:**
1. Pass flag to `score_player()` method (e.g., `is_draft_mode=True`)
2. Check which mode is calling the method (context-based)
3. Add mode parameter to PlayerManager initialization

(To be resolved during planning phase)

### Files Affected (Preliminary List)

**Configuration:**
- `league_helper/util/ConfigManager.py` - Add DRAFT_NORMALIZATION_MAX_SCALE getter
- `data/league_config.json` - Add new parameter

**Scoring:**
- `league_helper/util/PlayerManager.py` - Update score_player() to use draft param

**Add to Roster Mode:**
- `league_helper/add_to_roster_mode/AddToRosterModeManager.py` - Remove draft_config usage

**Accuracy Simulation:**
- `simulation/accuracy/AccuracySimulationManager.py` - Remove ROS assessment
- `simulation/accuracy/AccuracyResultsManager.py` - Remove ROS from best_configs dict
- `simulation/accuracy/AccuracyCalculator.py` - May need updates if ROS-specific

**Win-Rate Simulation:**
- `simulation/win_rate/SimulationManager.py` - Remove draft_config, add DRAFT_NORMALIZATION_MAX_SCALE testing
- `simulation/shared/ResultsManager.py` - Remove draft_config.json from output folders
- `simulation/shared/ConfigGenerator.py` - Add DRAFT_NORMALIZATION_MAX_SCALE to parameter list

---

## Open Questions

### Remaining Questions (45 unresolved)
- See checklist items Q7.1 through Q12.5 for detailed unresolved questions
- Sections remaining:
  - Error Handling & Edge Cases (10 items)
  - Logging & Debugging (6 items)
  - Documentation & Migration (8 items)
  - Performance & Optimization (5 items)
  - Data Migration & Cleanup (8 items)
  - Relationship to Other Features (5 items)

---

## Resolved Implementation Details

**Last Updated:** 2025-12-20 (42 of 87 questions resolved)

### 1. Configuration Structure (Q1.1-Q1.9) ✓

**DRAFT_NORMALIZATION_MAX_SCALE Location:**
- **Decision:** Add to `league_config.json` in the `parameters` section
- **Value:** 163 (from current draft_config.json)
- **Validation:** Required parameter - raise `ConfigurationError` if missing
- **Property:** Add `ConfigKeys.DRAFT_NORMALIZATION_MAX_SCALE` constant
- **Loading:** ConfigManager._load_config() will load from league_config.json and expose via `draft_normalization_max_scale` property

**ConfigManager Changes:**
- **Remove:** `use_draft_config` parameter from `__init__()` entirely
- **Remove:** `_load_draft_config()` method
- **Add:** `draft_normalization_max_scale` property to access the parameter

**Existing Files:**
- **draft_config.json:** Ignore silently if found (no warning, no error)
- **Removal:** Delete `data/configs/draft_config.json` immediately (no gradual deprecation)

### 2. Draft Mode Detection (Q2.1-Q2.7) ✓

**score_player() Changes:**
- **Method:** Add keyword-only parameter: `*, is_draft_mode=False`
- **Location:** PlayerManager.py:L565
- **Signature:** `def score_player(self, ..., *, is_draft_mode=False)`
- **Propagation:** Only `score_player()` needs the parameter (investigated - other methods don't need changes)

**normalize_projected_points() Changes:**
- **Parameter:** Add `is_draft_mode` parameter (passed from score_player)
- **Logic:**
  ```python
  scale = config.draft_normalization_max_scale if is_draft_mode else config.normalization_max_scale
  ```
- **Locations:** player_scoring.py:L163, L168, L458

**AddToRosterModeManager Integration:**
- **Call pattern:** `player_manager.score_player(..., is_draft_mode=True)`
- **No concerns:** User confirmed this approach

### 3. Add to Roster Mode Changes (Q3.1-Q3.6) ✓

**ConfigManager Instances:**
- **Before:** Two instances (LeagueHelperManager.py:L74 regular + L80 draft)
- **After:** Single instance (remove `self.draft_config`)
- **AddToRosterModeManager:** Receives regular `config` instead of `draft_config`
- **No signature change:** AddToRosterModeManager.__init__() keeps same signature, just receives different config object

**Weekly Config Selection:**
- **Decision:** Use `league_config.json` + weekly config based on `CURRENT_NFL_WEEK`
- **Pattern:** Same as other modes

**Other Modes:**
- **Verified:** Only LeagueHelperManager.py:L80 creates ConfigManager with `use_draft_config=True`

### 4. Accuracy Simulation ROS Removal (Q4.1-Q4.12) ✓

**ROS Method Removal:**
- **AccuracySimulationManager.py:L575:** Remove `run_ros_optimization()` (unused - CLI has no --ros flag)
- **AccuracyCalculator.py:L126:** Remove `calculate_ros_mae()` method
- **ParallelAccuracyRunner.py:** Remove `_evaluate_config_ros_worker()` method

**Horizon Updates:**
- **AccuracySimulationManager.py:L982:** Remove 'ros' from hardcoded horizon list
- **AccuracySimulationManager.run_both():** Update to test 4 horizons (not 5)
- **Tournament mode:** Tests each param across 4 weekly horizons only

**File Structure Changes:**
- **AccuracyResultsManager.py:L183:** Remove 'ros' from `best_configs` dict
- **AccuracyResultsManager.py:L326-332:** Remove 'ros' -> 'draft_config.json' from `file_mapping`
- **save_intermediate_results:** Remove draft_config.json from intermediate folders

**Output Folders:**
- **Current structure:** 6 files (draft_config.json + league_config.json + 4 weekly)
- **After removal:** 5 files (league_config.json + 4 weekly)
- **Note:** league_config.json already being saved, just remove draft_config.json

**No Changes Needed:**
- **WEEK_RANGES constant:** Doesn't include 'ros', no changes needed
- **run_accuracy_simulation.py CLI:** Update comments only (already expects 5 files for baseline)

**Performance Impact:**
- **Estimate:** ~20% faster (4 horizons instead of 5)

### 5. Win-Rate Simulation Changes (Q5.1-Q5.8) ✓

**draft_config.json References:**
- **ResultsManager.py:L427, L539, L606, L626:** Remove 'ros' -> 'draft_config.json' mappings
- **save_optimal_configs_folder:** Remove draft_config.json from file_mapping
- **save_optimal_config:** Remove draft_config.json references

**Parameter Testing:**
- **Add:** DRAFT_NORMALIZATION_MAX_SCALE to ConfigGenerator
- **Locations:** param_definitions (L92), BASE_CONFIG_PARAMS, parameter mapping (L204)
- **Test:** DRAFT_NORMALIZATION_MAX_SCALE only (not NORMALIZATION_MAX_SCALE)
- **Output:** In league_config.json

**Horizon Updates:**
- **ConfigGenerator.py:L335:** Remove 'ros' from `horizon_files` dict
- **ConfigGenerator.py:L1290:** Remove 'ros' from hardcoded horizon list
- **Methods:** Update get_config_for_horizon(), update_baseline_for_horizon() to remove 'ros' handling

**Output Folders:**
- **Current structure:** 6 files (draft_config + league_config + 4 weekly)
- **After removal:** 5 files (league_config + 4 weekly)

**Baseline Detection:**
- **find_baseline_config:** Already correct - expects 5 files (no draft_config.json)

### 6. Testing Strategy (Q6.1-Q6.10) ✓

**Unit Tests to Update:**
- **ConfigManager tests:** Remove `use_draft_config` tests, add `draft_normalization_max_scale` property tests
- **LeagueHelperManager tests:** Remove `self.draft_config` references, verify single ConfigManager instance
- **AddToRosterModeManager tests:** Update to pass regular config (not draft_config)
- **AccuracySimulationManager tests:** Remove ROS-related tests, verify 4 horizons only
- **AccuracyResultsManager tests:** Verify best_configs has 4 keys (not 5)
- **AccuracyCalculator tests:** Remove calculate_ros_mae tests
- **SimulationManager tests:** Remove draft_config.json file mapping tests
- **ResultsManager tests:** Update folder structure assertions (5 files not 6)
- **ConfigGenerator tests:** Add DRAFT_NORMALIZATION_MAX_SCALE parameter tests

**Integration Tests:**
- **test_league_helper_integration.py:** Verify single ConfigManager, draft mode flow
- **test_accuracy_simulation_integration.py:** Verify 4 horizons, 5-file output structure
- **test_simulation_integration.py:** Verify new folder structure

**New Tests to Add:**
- **Draft vs non-draft scoring:** Unit test `score_player(is_draft_mode=True)` vs `score_player(is_draft_mode=False)` - verify different normalization scales (163 vs weekly value)
- **Add to Roster integration:** Full draft recommendation flow using DRAFT_NORMALIZATION_MAX_SCALE
- **ROS removal verification:** Integration test - run accuracy sim, assert exactly 5 files created (league_config + 4 weekly), no draft_config.json

**Backward Compatibility:**
- **Decision:** Do NOT test backward compatibility (old draft_config.json ignored)

### 7. Error Handling & Edge Cases (Q7.1+) ✓ In Progress

**Missing DRAFT_NORMALIZATION_MAX_SCALE (Q7.1):**
- **Decision:** Raise ConfigurationError in _validate_league_config() with clear message
- **Error message:** "Missing required parameter: DRAFT_NORMALIZATION_MAX_SCALE in league_config.json. Add this parameter to the 'parameters' section with value 163 (recommended default)."
- **Location:** ConfigManager._validate_league_config()
- **Rationale:** Fail fast at config load time, consistent with Q1.3 (required parameter)

**Existing draft_config.json Files (Q7.2):**
- **Decision:** No handling - never load it, truly silent
- **Implementation:** Remove all draft_config.json loading references, don't check for existence
- **Result:** File becomes harmless cruft if it exists
- **Rationale:** Consistent with Q1.8 (ignore silently), no need for warnings or checks

**Weekly Config NORMALIZATION_MAX_SCALE Validation (Q7.3):**
- **Decision:** No changes - existing validation is sufficient
- **Current behavior:** ConfigManager already validates required params (L1025)
- **Rationale:** Not part of our refactoring, existing validation works correctly

**Draft Mode Scoring Without DRAFT_NORMALIZATION_MAX_SCALE (Q7.4):**
- **Decision:** Trust config validation - no defensive check in scoring code
- **Implementation:** `scale = config.draft_normalization_max_scale if is_draft_mode else config.normalization_max_scale`
- **Rationale:** Config validation (Q7.1) guarantees parameter exists. No redundant checks in hot path (score_player is called frequently)

**Invalid CURRENT_NFL_WEEK (Q7.5):**
- **Decision:** No changes - existing validation is sufficient
- **Current behavior:** ConfigManager._get_week_config_filename validates weeks 1-17 (L259-268)
- **Rationale:** Not part of our refactoring, existing validation works correctly

**Pre-Season Draft (Week 0) (Q7.6):**
- **Decision:** User must set CURRENT_NFL_WEEK to 1 for pre-season drafts
- **No special handling:** Existing validation requires weeks 1-17, no changes
- **Rationale:** Simple approach, not part of our refactoring scope

**Draft Mode with Weekly Projections (Q7.7):**
- **Decision:** No validation - allow is_draft_mode=True with use_weekly_projection=True
- **Rationale:** Parameters are orthogonal (is_draft_mode controls normalization scale, use_weekly_projection controls projection values). Trust caller's intent.
- **Expected usage:** AddToRosterModeManager calls with is_draft_mode=True, use_weekly_projection=False

**NORMALIZATION_MAX_SCALE in league_config (Q7.8):**
- **Decision:** Document clearly, no code changes
- **Behavior:** If user mistakenly adds NORMALIZATION_MAX_SCALE to league_config.json, weekly config value takes precedence (existing merging behavior)
- **Rationale:** Not a new risk from our refactoring. Config merging already handles this correctly.
- **Documentation note:** Clarify that NORMALIZATION_MAX_SCALE belongs in weekly configs, DRAFT_NORMALIZATION_MAX_SCALE in league_config

**Old Intermediate Folders with draft_config.json (Q7.9):**
- **Decision:** Ignore draft_config.json when loading intermediate folders
- **Behavior:** Load only expected files (league_config + 4 weekly + metadata.json = 6 files)
- **Result:** Old draft_config.json in intermediate folders is silently ignored
- **Rationale:** Consistent with general approach (Q7.2, Q7.4). DRAFT_NORMALIZATION_MAX_SCALE now loaded from league_config.json

**Optimal Folder Validation (Q7.10):**
- **Decision:** No changes - find_baseline_config already validates correctly
- **Current validation:** Expects 5 files (league_config.json + 4 weekly configs)
- **After changes:** Still expects 5 files (same structure, no draft_config.json)
- **Result:** Old optimal folders with 6 files (including draft_config.json) will be skipped (don't match expected file count)
- **Rationale:** Existing validation is correct for new structure

### 8. Logging & Debugging (Q8.1-Q8.6) ✓

**ConfigManager Logging (Q8.1, Q8.6):**
- **Decision:** Log DRAFT_NORMALIZATION_MAX_SCALE at DEBUG level during initialization
- **Implementation:** `self.logger.debug(f"Loaded DRAFT_NORMALIZATION_MAX_SCALE: {self.draft_normalization_max_scale}")`
- **Location:** ConfigManager.__init__ or _load_config()
- **Rationale:** Available for debugging without cluttering normal logs, consistent with other config parameters

**score_player Draft Mode Logging (Q8.2):**
- **Decision:** No logging in score_player (too frequent, would spam logs)
- **Rationale:** score_player is called thousands of times. Logging on every call would create massive log spam.
- **Alternative:** If draft mode confirmation needed, caller (AddToRosterModeManager) can log once at start

**draft_config.json Deprecation Warning (Q8.3):**
- **Decision:** No warning - completely silent (consistent with Q7.2)
- **Rationale:** Consistent with overall approach. File causes no harm if it exists.

**Accuracy Simulation Log Messages (Q8.4):**
- **Changes needed:** Update from "Evaluating 5 horizons" to "Evaluating 4 weekly horizons"
- **Files:** AccuracySimulationManager.py

**Win-Rate Simulation Log Messages (Q8.5):**
- **Changes needed:** Update references from draft_config.json to DRAFT_NORMALIZATION_MAX_SCALE in league_config
- **Files:** SimulationManager.py, ResultsManager.py

### 9. Documentation & Migration (Q9.1-Q9.8) ✓

**Documentation Updates:**
- **README.md (Q9.1):** Update Configuration, Simulation, Accuracy Sim, Win-Rate Sim sections - remove draft_config.json references, document DRAFT_NORMALIZATION_MAX_SCALE in league_config
- **ARCHITECTURE.md (Q9.2):** Update Configuration system and Simulation overview sections - document DRAFT_NORMALIZATION_MAX_SCALE location/usage
- **docs/scoring/01_normalization.md (Q9.3):** Add section explaining draft vs regular normalization (is_draft_mode parameter)
- **CLAUDE.md (Q9.5):** Remove draft_config from "Current Project Structure" section
- **simulation/README.md (Q9.7):** Remove ROS mode references, update config structure (4 horizons, no draft_config) if file exists

**Code Comments (Q9.8):**
- **Action:** Grep for "draft_config" in comments during implementation, update to reference DRAFT_NORMALIZATION_MAX_SCALE or remove

**Migration Guide (Q9.4):**
- **Decision:** Not needed (project owner is only user, can update manually)

**Commit Messages (Q9.6):**
- **Decision:** Follow standard format, no special reference needed

### 10. Performance & Optimization (Q10.1-Q10.5) ✓

**Draft Mode Detection Performance (Q10.1):**
- **Impact:** Negligible - single boolean check per score_player call
- **Analysis:** Modern CPUs handle billions of boolean checks per second, unmeasurable

**Parameter Caching (Q10.2, Q10.4):**
- **Decision:** Yes - store draft_normalization_max_scale as instance variable (property accessor)
- **Pattern:** Consistent with existing params cached at ConfigManager.py:L1035-1044
- **Implementation:** Load in _load_config(), expose via @property
- **Both scales cached:** draft_normalization_max_scale (league_config) and normalization_max_scale (weekly config)

**Method Removal (Q10.3):**
- **Decision:** Yes - delete entire _load_draft_config() method
- **Location:** ConfigManager.py:L307-343
- **Rationale:** No longer needed after removing draft_config.json support

**Memory Impact (Q10.5):**
- **Result:** Positive but minimal - saves one ConfigManager instance
- **Analysis:** Configs are small (~10KB), savings negligible but cleaner architecture

### 11. Data Migration & Cleanup (Q11.1-Q11.8) ✓

**File Deletion (Q11.1):**
- **Decision:** Yes - delete data/configs/draft_config.json as part of implementation
- **Timing:** Delete in Phase 6 (Cleanup) per dependency map

**Simulation Output Folders (Q11.2, Q11.6):**
- **Decision:** Leave as-is (harmless old data)
- **Rationale:** Old simulation results, no need to clean up. New runs won't create these files.

**Baseline Config Validation (Q11.3):**
- **Decision:** Already handled - validation expects 5 files, old folders with 6 will be skipped (Q7.10)

**Config Versioning (Q11.4):**
- **Decision:** No - not needed
- **Rationale:** Validation will catch missing parameter. Version field adds complexity without benefit.

**Test Fixtures (Q11.5):**
- **Decision:** Update test fixtures to new format
- **Action:** Remove draft_config.json, add DRAFT_NORMALIZATION_MAX_SCALE to league_config fixtures

**In-Progress Simulations (Q11.7):**
- **Decision:** No special transition - in-progress sims will fail if resumed
- **Mitigation:** User can restart simulation (acceptable for refactoring)

**Backup (Q11.8):**
- **Decision:** No - value (163) will be transferred to league_config.json
- **Rationale:** Value preserved in new location

### 12. Relationship to Other Features (Q12.1-Q12.5) ✓

**Unaffected Modes:**
- **Starter Helper Mode (Q12.1):** NO impact - uses weekly configs only, no draft_config references
- **Trade Simulator Mode (Q12.2):** NO impact - uses weekly configs only
- **Modify Player Data Mode (Q12.3):** NO impact - doesn't use ConfigManager for scoring
- **Historical Data Compilation (Q12.4):** NO impact - separate system (verify no draft_config references if exists)
- **Player Data Fetcher (Q12.5):** NO impact - independent system

---

## Dependencies

### External Dependencies
None - this is internal refactoring

### Internal Dependencies
- ConfigManager must support DRAFT_NORMALIZATION_MAX_SCALE before scoring changes
- Accuracy sim changes must complete before removing draft_config.json
- Win-rate sim changes must complete before removing draft_config.json

---

## Migration/Backward Compatibility

**Existing draft_config.json files:**
- Will be ignored (not loaded)
- No migration tool needed
- Users can manually delete old files if desired

**Existing optimal/accuracy_optimal folders:**
- May contain draft_config.json files
- These become "dead" files (harmless but unused)
- No cleanup required (won't break anything)

---

## Testing Strategy

(To be defined during planning)

### Unit Tests
- ConfigManager reading DRAFT_NORMALIZATION_MAX_SCALE
- score_player() using correct scale in draft vs non-draft mode
- Accuracy sim no longer includes ROS assessment
- Win-rate sim tests DRAFT_NORMALIZATION_MAX_SCALE

### Integration Tests
- Add to Roster mode end-to-end with new config
- Accuracy simulation runs with 4 horizons (not 5)
- Win-rate simulation outputs league_config.json only (no draft_config)

### Manual Testing
- Run Add to Roster mode and verify recommendations
- Run accuracy sim and verify 4-file output
- Run win-rate sim and verify no draft_config.json created

---

## Performance Implications

**Expected improvements:**
- Accuracy simulation: ~20% faster (no ROS assessment)
- Simpler config loading: marginal improvement
- Fewer files to manage: developer productivity improvement

**No negative performance impacts expected**

---

## Notes

### Why Only NORMALIZATION_MAX_SCALE Matters
Research showed that of all parameters in draft_config.json, only NORMALIZATION_MAX_SCALE had measurable impact on draft recommendation quality. Other parameters (ADP weights, team quality, etc.) worked fine with league_config.json values.

### Simplification Benefits
1. **Fewer moving parts** - One config file vs two
2. **Less confusion** - No "use this file only here" special cases
3. **Easier simulation** - No need to optimize ROS parameters
4. **Clearer code** - Single ConfigManager pattern restored

---

## Dependency Map

### Component Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONFIGURATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  league_config.json              weekly configs                 │
│  ├─ Strategy params              ├─ week1-5.json                │
│  │  ├─ BYE_WEIGHTS              │  ├─ NORMALIZATION_MAX_SCALE  │
│  │  ├─ DRAFT_ORDER              │  ├─ TEAM_QUALITY_WEIGHT      │
│  │  └─ MAX_POSITIONS            │  ├─ PERFORMANCE_WEIGHT       │
│  │                               │  └─ MATCHUP_WEIGHT           │
│  └─ **NEW**: DRAFT_              ├─ week6-9.json               │
│     NORMALIZATION_MAX_SCALE      ├─ week10-13.json             │
│                                   └─ week14-17.json             │
│                                                                  │
│  ~~draft_config.json~~ ← TO BE REMOVED                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CONFIGURATION MANAGER                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ConfigManager (league_helper/util/ConfigManager.py)            │
│  ├─ __init__(data_folder, ~~use_draft_config~~)                │
│  │  └─ REMOVE use_draft_config parameter                        │
│  ├─ _load_config()                                              │
│  │  ├─ Loads league_config.json                                 │
│  │  ├─ **UPDATE**: Load DRAFT_NORMALIZATION_MAX_SCALE           │
│  │  └─ Merges weekly config based on CURRENT_NFL_WEEK           │
│  ├─ ~~_load_draft_config()~~ ← REMOVE METHOD                    │
│  ├─ normalization_max_scale (property)                          │
│  └─ **NEW**: draft_normalization_max_scale (property)           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LEAGUE HELPER LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LeagueHelperManager                                            │
│  ├─ self.config = ConfigManager(data_folder)                    │
│  ├─ ~~self.draft_config = ConfigManager(..., True)~~ ← REMOVE   │
│  ├─ self.player_manager = PlayerManager(config, ...)            │
│  ├─ ~~self.draft_player_manager = ...~~ ← REMOVE?               │
│  ├─ AddToRosterModeManager(~~draft_config~~)                    │
│  │  └─ **UPDATE**: Pass regular config OR flag for draft mode   │
│  ├─ StarterHelperModeManager(config, ...)                       │
│  └─ TradeSimulatorModeManager(config, ...)                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    PLAYER SCORING LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PlayerManager (league_helper/util/PlayerManager.py)            │
│  ├─ score_player(..., **NEW**: is_draft_mode=False)            │
│  │  └─ Calls normalize_projected_points()                       │
│  │                                                              │
│  player_scoring.py                                              │
│  ├─ normalize_projected_points(player, config, ...)            │
│  │  └─ Uses config.normalization_max_scale                      │
│  │     **UPDATE**: Check is_draft_mode flag                     │
│  │     ├─ If True: use config.draft_normalization_max_scale    │
│  │     └─ If False: use config.normalization_max_scale          │
│  └─ (Lines 163, 168, 458 reference normalization_max_scale)    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ADD TO ROSTER MODE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  AddToRosterModeManager                                         │
│  ├─ **UPDATE**: __init__(config) [was draft_config]            │
│  ├─ Calls player_manager.score_player()                         │
│  │  └─ **UPDATE**: Pass is_draft_mode=True                      │
│  └─ Returns draft recommendations                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    ACCURACY SIMULATION                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  AccuracySimulationManager                                      │
│  ├─ run() - tournament mode (all horizons)                      │
│  │  ├─ **BEFORE**: 5 horizons ['ros', 'week_1_5', ...]         │
│  │  └─ **AFTER**: 4 horizons ['week_1_5', 'week_6_9', ...]     │
│  ├─ ~~run_ros_optimization()~~ ← REMOVE METHOD                  │
│  └─ Calls ConfigGenerator.get_config_for_horizon()             │
│                                                                  │
│  AccuracyResultsManager                                         │
│  ├─ best_configs = {                                            │
│  │    ~~'ros': None,~~  ← REMOVE                                │
│  │    'week_1_5': None,                                         │
│  │    'week_6_9': None,                                         │
│  │    'week_10_13': None,                                       │
│  │    'week_14_17': None                                        │
│  │  }                                                           │
│  ├─ save_optimal_configs()                                      │
│  │  ├─ file_mapping = {                                         │
│  │  │    ~~'ros': 'draft_config.json',~~  ← REMOVE              │
│  │  │    'week_1_5': 'week1-5.json',                            │
│  │  │    ...                                                    │
│  │  │  }                                                        │
│  │  └─ **AFTER**: Creates 4 weekly files only                   │
│  └─ save_intermediate_results()                                 │
│     └─ **UPDATE**: Remove draft_config.json from output         │
│                                                                  │
│  AccuracyCalculator                                             │
│  ├─ ~~calculate_ros_mae()~~ ← REMOVE METHOD                     │
│  └─ calculate_weekly_mae() - keep for 4 horizons                │
│                                                                  │
│  ParallelAccuracyRunner                                         │
│  └─ ~~_evaluate_config_ros_worker()~~ ← REMOVE                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    WIN-RATE SIMULATION                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SimulationManager (win_rate/)                                  │
│  └─ Calls ResultsManager.save_optimal_configs_folder()          │
│                                                                  │
│  ResultsManager (shared/)                                       │
│  ├─ save_optimal_configs_folder()                               │
│  │  ├─ file_mapping = {                                         │
│  │  │    ~~'ros': 'draft_config.json',~~  ← REMOVE              │
│  │  │    'week_1_5': 'week1-5.json',                            │
│  │  │    ...                                                    │
│  │  │  }                                                        │
│  │  └─ **AFTER**: Output league_config.json + 4 weekly files    │
│  ├─ save_optimal_config() - single file                         │
│  │  └─ **UPDATE**: Remove draft_config references               │
│  └─ validate_optimal_folder()                                   │
│     ├─ **BEFORE**: Required files include draft_config.json     │
│     └─ **AFTER**: Update validation logic                       │
│                                                                  │
│  ConfigGenerator (shared/)                                      │
│  ├─ Parameter definitions                                       │
│  │  └─ **ADD**: DRAFT_NORMALIZATION_MAX_SCALE                   │
│  ├─ generate_horizon_test_values(param)                         │
│  │  └─ **UPDATE**: Remove 'ros' horizon handling                │
│  ├─ get_config_for_horizon(horizon, ...)                        │
│  │  └─ **UPDATE**: Remove 'ros' horizon handling                │
│  └─ update_baseline_for_horizon(horizon, ...)                   │
│     └─ **UPDATE**: Remove 'ros' horizon handling                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Critical Dependencies

**Configuration Loading Chain:**
1. league_config.json → ConfigManager → PlayerManager → score_player()
2. weekly configs → ConfigManager → PlayerManager → score_player()
3. **NEW**: DRAFT_NORMALIZATION_MAX_SCALE in league_config → ConfigManager.draft_normalization_max_scale → score_player(is_draft_mode=True)

**Draft Mode Signal Flow:**
1. User selects "Add to Roster" mode
2. LeagueHelperManager creates AddToRosterModeManager
3. AddToRosterModeManager calls player_manager.score_player(**is_draft_mode=True**)
4. score_player passes is_draft_mode to normalize_projected_points()
5. normalize_projected_points chooses draft vs regular normalization scale

**ROS Removal Chain:**
1. AccuracySimulationManager.run() - Remove 'ros' from horizons list
2. AccuracyResultsManager.best_configs - Remove 'ros' key
3. AccuracyResultsManager.save_optimal_configs - Remove 'ros' from file_mapping
4. AccuracyCalculator - Remove calculate_ros_mae() method
5. ParallelAccuracyRunner - Remove _evaluate_config_ros_worker()
6. ConfigGenerator - Remove 'ros' horizon handling from all methods

### Files That Must Change (in Order)

**Phase 1: Configuration**
1. `data/configs/league_config.json` - Add DRAFT_NORMALIZATION_MAX_SCALE
2. `league_helper/util/ConfigManager.py` - Load and expose draft parameter
3. `league_helper/util/player_scoring.py` - Use draft scale when in draft mode

**Phase 2: Scoring**
4. `league_helper/util/PlayerManager.py` - Add is_draft_mode parameter
5. `league_helper/add_to_roster_mode/AddToRosterModeManager.py` - Pass is_draft_mode=True

**Phase 3: League Helper**
6. `league_helper/LeagueHelperManager.py` - Remove second ConfigManager instance

**Phase 4: Accuracy Simulation**
7. `simulation/accuracy/AccuracyResultsManager.py` - Remove 'ros' from best_configs and file_mapping
8. `simulation/accuracy/AccuracySimulationManager.py` - Remove run_ros_optimization()
9. `simulation/accuracy/AccuracyCalculator.py` - Remove calculate_ros_mae()
10. `simulation/accuracy/ParallelAccuracyRunner.py` - Remove _evaluate_config_ros_worker()
11. `run_accuracy_simulation.py` - Update comments

**Phase 5: Win-Rate Simulation**
12. `simulation/shared/ResultsManager.py` - Remove draft_config from file_mapping
13. `simulation/shared/ConfigGenerator.py` - Add DRAFT_NORMALIZATION_MAX_SCALE, remove 'ros' horizon
14. `simulation/win_rate/SimulationManager.py` - Update config output

**Phase 6: Cleanup**
15. `data/configs/draft_config.json` - Delete file

### Breaking Changes

**API Changes:**
- `ConfigManager.__init__(use_draft_config)` - Remove parameter (BREAKING)
- `PlayerManager.score_player()` - Add is_draft_mode parameter (BACKWARD COMPATIBLE if keyword-only with default=False)
- `AddToRosterModeManager.__init__()` - Change from draft_config to regular config (BREAKING but internal API)

**File Structure Changes:**
- `data/configs/draft_config.json` - No longer created/used
- `simulation_configs/accuracy_optimal_*/` - 4 files instead of 5 (draft_config.json removed)
- `simulation_configs/optimal_*/` - 5 files instead of 6 (draft_config.json removed)

**Behavioral Changes:**
- Accuracy simulation runs 4 horizons instead of 5 (~20% faster)
- Add to Roster mode uses league_config + weekly config instead of draft_config
- Single ConfigManager instance instead of two

---

## Assumptions

(To be documented during Phase 2.9 Assumptions Audit)
