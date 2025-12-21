# Depreciate draft_config.json - Planning Checklist

## Purpose
This checklist tracks all open questions and decisions needed to complete the feature specification. Items marked `[x]` are resolved, items marked `[ ]` are pending.

**Progress: 87/87 questions resolved** ✓ COMPLETE

---

## Resolution Log

This section documents the resolution of each checklist item:

```
[2025-12-20] Sections 1-6 (Q1.1-Q6.10): 42 questions resolved in previous session
Resolution: User provided answers during systematic walkthrough
- Configuration Structure: All 9 questions resolved
- Draft Mode Detection: All 7 questions resolved
- Add to Roster Mode: All 6 questions resolved
- Accuracy Simulation ROS Removal: All 12 questions resolved
- Win-Rate Simulation Changes: All 8 questions resolved
- Testing Strategy: All 10 questions resolved
Updated: Checklist progress updated to 42/87
Note: Full details in individual question resolutions below
---
```

---

## Checklist Items

### ITERATION 1: Configuration Architecture & Basic Implementation

#### Configuration Structure (9 items)

- [x] **Q1.1**: Where should DRAFT_NORMALIZATION_MAX_SCALE live?
  - **RESOLVED**: Option A - Add to league_config.json (per original notes)
  - **Rationale**: Despite breaking the pattern (prediction params usually in weekly configs), this matches the original requirement

- [x] **Q1.2**: What should default value for DRAFT_NORMALIZATION_MAX_SCALE be?
  - **RESOLVED**: Option A - Use 163 (from current draft_config.json)

- [x] **Q1.3**: Should we validate DRAFT_NORMALIZATION_MAX_SCALE exists or provide fallback?
  - **RESOLVED**: Option A - Require it (raise error if missing)

- [x] **Q1.4**: How does ConfigManager know which NORMALIZATION param to use?
  - **RESOLVED**: Via is_draft_mode parameter passed to score_player() (see Q2.1)
  - **Implementation**: score_player passes is_draft_mode to normalize_projected_points(), which chooses the appropriate scale

- [x] **Q1.5**: Should ConfigKeys class get new constant for DRAFT_NORMALIZATION_MAX_SCALE?
  - **RESOLVED**: Option A - Yes, add constant

- [x] **Q1.6**: Does _load_config need updates to handle draft normalization param?
  - **RESOLVED**: Yes, needs to load DRAFT_NORMALIZATION_MAX_SCALE from league_config.json and expose it via property

- [x] **Q1.7**: Should we remove draft_config.json file immediately or deprecate gradually?
  - **RESOLVED**: Option A - Remove immediately

- [x] **Q1.8**: What happens to existing draft_config.json files after this change?
  - **RESOLVED**: Option A - Ignore silently

- [x] **Q1.9**: Should ConfigManager still accept use_draft_config parameter (deprecated) or remove it?
  - **RESOLVED**: Option A - Remove entirely

#### Draft Mode Detection (7 items)

- [x] **Q2.1**: How should score_player() detect it's being called for draft mode?
  - **RESOLVED**: Option A - Add `is_draft_mode` boolean parameter to score_player()

- [x] **Q2.2**: If adding parameter, should it be positional or keyword-only?
  - **RESOLVED**: Option A - Keyword-only parameter (*, is_draft_mode=False)

- [x] **Q2.3**: Should draft mode affect OTHER scoring methods besides score_player()?
  - **RESOLVED**: Investigation complete - Only score_player() needs the parameter
  - **Finding**: Other methods don't need changes, they either don't call score_player or use the same pattern

- [x] **Q2.4**: How do we pass draft mode info from AddToRosterModeManager to PlayerManager?
  - **RESOLVED**: AddToRosterModeManager calls player_manager.score_player(..., is_draft_mode=True)
  - **User confirmed**: No concerns with this approach

- [x] **Q2.5**: Should PlayerManager store draft mode state or receive it per call?
  - **RESOLVED**: Option B - Pass on every score_player call (via is_draft_mode parameter)

- [x] **Q2.6**: Where in player_scoring.py does normalization happen?
  - **RESOLVED**: In normalize_projected_points() function at L163
  - **Change**: Will check is_draft_mode and use appropriate normalization scale

- [x] **Q2.7**: Does normalize_projected_points need draft mode parameter too?
  - **RESOLVED**: Yes, needs is_draft_mode parameter passed from score_player()

#### Add to Roster Mode Changes (6 items)

- [x] **Q3.1**: Where does AddToRosterModeManager currently use draft_config?
  - **RESOLVED**: Investigation complete - AddToRosterModeManager receives config via __init__, no changes needed to class itself

- [x] **Q3.2**: Should AddToRosterMode use league_config + which weekly config?
  - **RESOLVED**: Option C - league_config + config based on CURRENT_NFL_WEEK

- [x] **Q3.3**: How many ConfigManager instances exist after this change?
  - **RESOLVED**: Only one ConfigManager instance after changes (remove self.draft_config from LeagueHelperManager)

- [x] **Q3.4**: Does AddToRosterModeManager.__init__ signature change?
  - **RESOLVED**: No signature change needed - receives regular config instead of draft_config

- [x] **Q3.5**: Are there other places that create ConfigManager with use_draft_config=True?
  - **RESOLVED**: Only LeagueHelperManager.py:L80 (already identified)

- [x] **Q3.6**: Does Add to Roster mode need special flag to enable draft normalization?
  - **RESOLVED**: Yes, via is_draft_mode=True passed to score_player() (see Q2.1)

### ITERATION 2: Simulation Changes & Testing

#### Accuracy Simulation ROS Removal (12 items)

- [x] **Q4.1**: Where is ROS mode invoked in accuracy sim?
  - **RESOLVED**: run_ros_optimization() exists but is UNUSED (CLI doesn't have --ros flag, always runs tournament mode)

- [x] **Q4.2**: How is best_configs['ros'] currently populated?
  - **RESOLVED**: Via add_result() when week_range_key='ros' (to be removed)

- [x] **Q4.3**: What files need changes to remove ROS from accuracy sim?
  - **RESOLVED**: 5 files identified:
    - AccuracyResultsManager.py: Remove 'ros' from best_configs dict and file_mapping
    - AccuracySimulationManager.py: Remove run_ros_optimization method, update run_both() to 4 horizons
    - AccuracyCalculator.py: Remove calculate_ros_mae() method
    - ParallelAccuracyRunner.py: Remove _evaluate_config_ros_worker method
    - run_accuracy_simulation.py: Update comments (4 horizons not 5)

- [x] **Q4.4**: Should accuracy_optimal folders have 4 or 5 files after ROS removal?
  - **RESOLVED**: Option A - 5 files (league_config.json + 4 weekly)
  - **Actual current structure**: 6 files (draft_config.json + league_config.json + 4 weekly)
  - **After removal**: 5 files (league_config.json already being saved, just remove draft_config.json)

- [x] **Q4.5**: Does AccuracyCalculator.calculate_ros_mae need removal?
  - **RESOLVED**: Yes, remove this method

- [x] **Q4.6**: What happens to file_mapping dict in AccuracyResultsManager?
  - **RESOLVED**: Remove 'ros' -> 'draft_config.json' entry entirely

- [x] **Q4.7**: Does WEEK_RANGES constant need updating?
  - **RESOLVED**: NO changes needed (doesn't include 'ros')

- [x] **Q4.8**: Should intermediate folders still save draft_config.json?
  - **RESOLVED**: Remove draft_config.json from intermediate folders as well

- [x] **Q4.9**: How does tournament mode handle ROS horizon?
  - **RESOLVED**: Update to test only 4 weekly horizons (remove 'ros' from horizon list)

- [x] **Q4.10**: Does AccuracySimulationManager.horizons list need updating?
  - **RESOLVED**: Yes, remove 'ros' from hardcoded horizon list at L982

- [x] **Q4.11**: What's the performance impact of removing ROS assessment?
  - **RESOLVED**: ~20% faster (4 horizons instead of 5)

- [x] **Q4.12**: Should run_accuracy_simulation.py CLI change?
  - **RESOLVED**: Update comments only (no CLI changes, already correct with 5 required files for baseline)

#### Win-Rate Simulation Changes (8 items)

- [x] **Q5.1**: Where does SimulationManager create/save draft_config.json?
  - **RESOLVED**: ResultsManager.save_optimal_configs_folder has 'ros' -> 'draft_config.json' mapping at L427, L539, L606, L626

- [x] **Q5.2**: Should win-rate simulation test DRAFT_NORMALIZATION_MAX_SCALE?
  - **RESOLVED**: Option A - Test DRAFT_NORMALIZATION_MAX_SCALE only (not NORMALIZATION_MAX_SCALE)
  - **Implementation**: Add to param_definitions, BASE_CONFIG_PARAMS, and parameter mapping

- [x] **Q5.3**: How does ConfigGenerator handle parameters?
  - **RESOLVED**: Investigation complete - Has param_definitions (L92), BASE_CONFIG_PARAMS, parameter mapping (L204), horizon_files (L335), and horizon list (L1290)
  - **Changes needed**: Add DRAFT_NORMALIZATION_MAX_SCALE; Remove 'ros' from horizons

- [x] **Q5.4**: Should DRAFT_NORMALIZATION_MAX_SCALE be tested separately or with NORMALIZATION_MAX_SCALE?
  - **RESOLVED**: Test separately (just DRAFT_NORMALIZATION_MAX_SCALE, not both)

- [x] **Q5.5**: Does win-rate sim need to output DRAFT_NORMALIZATION_MAX_SCALE in optimal configs?
  - **RESOLVED**: Yes, outputs in league_config.json (DRAFT_NORMALIZATION_MAX_SCALE is in league_config per Q1.1)

- [x] **Q5.6**: What's the structure of optimal_* folders after changes?
  - **RESOLVED**: Currently 6 files (draft_config + league_config + 4 weekly), after: 5 files (league_config + 4 weekly)

- [x] **Q5.7**: Does ResultsManager.save_optimal_config need updates?
  - **RESOLVED**: Yes, remove draft_config.json references from file mapping

- [x] **Q5.8**: How does find_baseline_config detect valid config folders?
  - **RESOLVED**: Already correct - expects 5 files (no draft_config.json) per run_accuracy_simulation.py:L237

#### Testing Strategy (10 items)

- [x] **Q6.1**: Which ConfigManager tests need updating?
  - **RESOLVED**: tests/league_helper/util/test_ConfigManager_*.py
  - **Changes**: Remove use_draft_config tests, add DRAFT_NORMALIZATION_MAX_SCALE property tests

- [x] **Q6.2**: Which LeagueHelperManager tests need updating?
  - **RESOLVED**: tests/league_helper/test_LeagueHelperManager.py
  - **Changes**: Remove self.draft_config references, verify single ConfigManager instance

- [x] **Q6.3**: Which Add to Roster mode tests need updating?
  - **RESOLVED**: tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py
  - **Changes**: Update to pass regular config (not draft_config)

- [x] **Q6.4**: Which accuracy simulation tests need updating?
  - **RESOLVED**: test_AccuracySimulationManager.py, test_AccuracyResultsManager.py, test_AccuracyCalculator.py
  - **Changes**: Remove ROS-related tests, verify 4 horizons only

- [x] **Q6.5**: Which win-rate simulation tests need updating?
  - **RESOLVED**: test_SimulationManager.py, test_ResultsManager.py, test_ConfigGenerator.py
  - **Changes**: Remove draft_config.json from file mapping tests, add DRAFT_NORMALIZATION_MAX_SCALE parameter tests

- [x] **Q6.6**: Do integration tests need updating?
  - **RESOLVED**: Yes - test_league_helper_integration.py, test_accuracy_simulation_integration.py, test_simulation_integration.py
  - **Changes**: Update to verify single ConfigManager, 4 horizons, new folder structure

- [x] **Q6.7**: How to test draft vs non-draft scoring paths?
  - **RESOLVED**: Unit test score_player(is_draft_mode=True) vs score_player(is_draft_mode=False)
  - **Verify**: Different normalization_max_scale values used (163 vs weekly value)

- [x] **Q6.8**: Should we add integration test for Add to Roster with new config?
  - **RESOLVED**: Yes, add integration test for full draft recommendation flow using DRAFT_NORMALIZATION_MAX_SCALE

- [x] **Q6.9**: How to verify ROS assessment is truly removed?
  - **RESOLVED**: Integration test: Run accuracy sim, assert exactly 5 files created (league_config + 4 weekly), no draft_config.json

- [x] **Q6.10**: Should we test backward compatibility (old draft_config.json ignored)?
  - **RESOLVED**: No - decided not to add backward compatibility test

### ITERATION 3: Cross-Cutting Concerns & Edge Cases

#### Error Handling & Edge Cases (10 items)

- [x] **Q7.1**: What if DRAFT_NORMALIZATION_MAX_SCALE is missing from config?
  - **RESOLVED**: Option A - Raise ConfigurationError in _validate_league_config() with clear message
  - **Implementation**: Include helpful message: "Missing required parameter: DRAFT_NORMALIZATION_MAX_SCALE in league_config.json. Add this parameter to the 'parameters' section with value 163 (recommended default)."
  - **Consistent with**: Q1.3 (required parameter)

- [x] **Q7.2**: What if draft_config.json still exists (backward compat)?
  - **RESOLVED**: Option A - No handling, just never load it (truly silent)
  - **Implementation**: Remove all draft_config.json loading references, file is simply ignored
  - **Rationale**: File becomes harmless cruft, consistent with Q1.8

- [x] **Q7.3**: What if weekly config is missing NORMALIZATION_MAX_SCALE?
  - **RESOLVED**: Option A - No changes, existing validation is sufficient
  - **Current behavior**: ConfigManager already validates required params (L1025)
  - **Rationale**: Not part of our refactoring, existing validation works correctly

- [x] **Q7.4**: What if score_player called with draft mode but no DRAFT_NORMALIZATION_MAX_SCALE?
  - **RESOLVED**: Option A - Trust config validation, no defensive check in scoring code
  - **Implementation**: Simple code: `scale = config.draft_normalization_max_scale if is_draft_mode else config.normalization_max_scale`
  - **Rationale**: If config loaded successfully, parameter exists (validated in Q7.1). No redundant checks in hot path.

- [x] **Q7.5**: What if CURRENT_NFL_WEEK is invalid when Add to Roster loads config?
  - **RESOLVED**: Option A - No changes, existing validation is sufficient
  - **Current behavior**: ConfigManager._get_week_config_filename validates weeks 1-17 (L259-268)
  - **Rationale**: Not part of our refactoring, existing validation works correctly

- [x] **Q7.6**: What happens during pre-season draft (week 0)?
  - **RESOLVED**: Option A - User must set CURRENT_NFL_WEEK to 1 for pre-season drafts
  - **No special handling**: Existing validation requires weeks 1-17
  - **Rationale**: Simple, no code changes. Not part of our refactoring scope - existing behavior.

- [x] **Q7.7**: Can draft mode be used with use_weekly_projection=True?
  - **RESOLVED**: Option A - No validation, allow the combination
  - **Rationale**: Parameters are orthogonal (is_draft_mode controls normalization scale, use_weekly_projection controls projection values). Trust caller's intent.
  - **Expected usage**: AddToRosterModeManager will use is_draft_mode=True, use_weekly_projection=False

- [x] **Q7.8**: What if user manually sets NORMALIZATION_MAX_SCALE in league_config?
  - **RESOLVED**: Option D - Document clearly, no code changes
  - **Behavior**: Weekly config value takes precedence (existing config merging behavior)
  - **Rationale**: Not a new risk from our refactoring. Existing config merging handles it correctly.

- [x] **Q7.9**: What if accuracy sim intermediate folder has draft_config.json?
  - **RESOLVED**: Option A - Ignore draft_config.json when loading intermediate folder
  - **Behavior**: Load only expected files (league_config + 4 weekly + metadata.json = 6 files)
  - **Rationale**: Consistent with general approach (Q7.2, Q7.4). DRAFT_NORMALIZATION_MAX_SCALE now in league_config.json.

- [x] **Q7.10**: What if optimal config folder is missing files?
  - **RESOLVED**: Option A - No changes, already validates correctly
  - **Current behavior**: Expects 5 files (league_config.json + 4 weekly configs)
  - **After changes**: Still 5 files (same structure, just no draft_config.json)
  - **Rationale**: Validation already correct. Old folders with 6 files will be skipped (don't match expected count).

#### Logging & Debugging (6 items)

- [x] **Q8.1**: Should ConfigManager log when using draft vs regular normalization?
  - **RESOLVED**: Option B - Log at DEBUG level during ConfigManager initialization
  - **Implementation**: `self.logger.debug(f"Loaded DRAFT_NORMALIZATION_MAX_SCALE: {self.draft_normalization_max_scale}")`
  - **Rationale**: Available for debugging without cluttering normal logs, consistent with other config parameters

- [x] **Q8.2**: Should score_player log when in draft mode?
  - **RESOLVED**: Option A - No logging in score_player (too frequent, would spam logs)
  - **Rationale**: score_player is called thousands of times. If draft mode confirmation needed, caller (AddToRosterModeManager) can log once.

- [x] **Q8.3**: Should we log deprecation warning if draft_config.json found?
  - **RESOLVED**: Option A - No warning, completely silent (consistent with Q7.2)
  - **Rationale**: Consistent with Q7.2 decision (no handling). File causes no harm if it exists.

- [x] **Q8.4**: What log messages change in accuracy simulation?
  - **RESOLVED**: Update log messages to reflect 4 horizons instead of 5
  - **Changes**: "Evaluating 5 horizons" → "Evaluating 4 weekly horizons"
  - **Files**: AccuracySimulationManager.py log messages

- [x] **Q8.5**: What log messages change in win-rate simulation?
  - **RESOLVED**: Update references from draft_config.json to DRAFT_NORMALIZATION_MAX_SCALE in league_config
  - **Changes**: Any logs mentioning draft_config.json creation should reference league_config parameter instead
  - **Files**: SimulationManager.py, ResultsManager.py

- [x] **Q8.6**: Should we log the DRAFT_NORMALIZATION_MAX_SCALE value at startup?
  - **RESOLVED**: Yes - already covered in Q8.1 (log at DEBUG level during ConfigManager init)
  - **Implementation**: `self.logger.debug(f"Loaded DRAFT_NORMALIZATION_MAX_SCALE: {self.draft_normalization_max_scale}")`

#### Documentation & Migration (8 items)

- [x] **Q9.1**: What README.md sections need updates?
  - **RESOLVED**: Yes - Update Configuration, Simulation, Accuracy Sim, Win-Rate Sim sections
  - **Changes**: Remove draft_config.json references, document DRAFT_NORMALIZATION_MAX_SCALE in league_config

- [x] **Q9.2**: What ARCHITECTURE.md sections need updates?
  - **RESOLVED**: Yes - Update Configuration system and Simulation overview sections
  - **Changes**: Document DRAFT_NORMALIZATION_MAX_SCALE location/usage, remove draft_config references

- [x] **Q9.3**: Do scoring docs need updates?
  - **RESOLVED**: Yes - Update docs/scoring/01_normalization.md
  - **Changes**: Add section explaining draft vs regular normalization (is_draft_mode parameter)

- [x] **Q9.4**: Should we add migration guide for users?
  - **RESOLVED**: No - Not needed (project owner is only user, can update manually)
  - **Rationale**: Low value, single-user project

- [x] **Q9.5**: Should we update CLAUDE.md workflow guides?
  - **RESOLVED**: Yes - Remove draft_config from "Current Project Structure" section
  - **Changes**: Update data files list to remove draft_config.json reference

- [x] **Q9.6**: Do commit messages need to reference this feature folder?
  - **RESOLVED**: No - Follow standard commit message format
  - **Rationale**: Standard commit practices sufficient, no special reference needed

- [x] **Q9.7**: Should simulation/README.md be updated?
  - **RESOLVED**: Yes - if simulation README exists, update it
  - **Changes**: Remove ROS mode references, update config structure (4 horizons, no draft_config)

- [x] **Q9.8**: Should we update code comments referencing draft_config?
  - **RESOLVED**: Yes - Update comments during implementation
  - **Action**: Grep for "draft_config" in comments, update to reference DRAFT_NORMALIZATION_MAX_SCALE or remove

#### Performance & Optimization (5 items)

- [x] **Q10.1**: What's the performance impact of draft mode detection?
  - **RESOLVED**: Negligible - single boolean check per score_player call
  - **Analysis**: Modern CPUs handle billions of boolean checks per second, this is unmeasurable

- [x] **Q10.2**: Should draft normalization param be cached in ConfigManager?
  - **RESOLVED**: Yes - store as instance variable (property accessor)
  - **Pattern**: Consistent with existing params cached at L1035-1044
  - **Implementation**: Load in _load_config(), expose via @property

- [x] **Q10.3**: Can we remove _load_draft_config method entirely?
  - **RESOLVED**: Yes - delete the entire _load_draft_config() method
  - **Location**: ConfigManager.py:L307-343
  - **Rationale**: No longer needed after removing draft_config.json support

- [x] **Q10.4**: Should we pre-compute both normalization scales at init?
  - **RESOLVED**: Yes - both stored as properties
  - **Implementation**: draft_normalization_max_scale from league_config, normalization_max_scale from weekly config
  - **Benefit**: Minimal conditional logic during scoring, properties already cached

- [x] **Q10.5**: What's memory impact of removing second ConfigManager?
  - **RESOLVED**: Positive but minimal - saves one ConfigManager instance
  - **Analysis**: Configs are small (~10KB), savings negligible but cleaner architecture

#### Data Migration & Cleanup (8 items)

- [x] **Q11.1**: Should we delete existing draft_config.json files?
  - **RESOLVED**: Yes - delete data/configs/draft_config.json as part of implementation
  - **Timing**: Delete in Phase 6 (Cleanup) per dependency map in specs
  - **Rationale**: File no longer needed, cleaner to remove

- [x] **Q11.2**: What about draft_config.json in simulation output folders?
  - **RESOLVED**: Leave as-is (harmless old data)
  - **Rationale**: Old simulation results, no need to clean up. New runs won't create these files.
  - **User action**: Can manually delete old folders if desired

- [x] **Q11.3**: Should find_baseline_config skip folders with draft_config?
  - **RESOLVED**: Already handled - validation expects 5 files, old folders with 6 will be skipped (Q7.10)
  - **Rationale**: File count mismatch naturally filters old folders

- [x] **Q11.4**: Should we version-bump configs to indicate breaking change?
  - **RESOLVED**: No - not needed
  - **Rationale**: Config validation will catch missing DRAFT_NORMALIZATION_MAX_SCALE. Version field adds complexity without benefit.

- [x] **Q11.5**: What about test fixtures with draft_config.json?
  - **RESOLVED**: Update test fixtures to new format (remove draft_config.json, add DRAFT_NORMALIZATION_MAX_SCALE to league_config)
  - **Action**: Update during test updates phase
  - **Files**: tests/fixtures/**/draft_config.json

- [x] **Q11.6**: Should we clean up intermediate folders with draft_config?
  - **RESOLVED**: No - leave as-is
  - **Rationale**: Old intermediate data, harmless. Q7.9 handles resume (ignores draft_config.json).

- [x] **Q11.7**: What's the transition plan for simulation runs in progress?
  - **RESOLVED**: No special transition - in-progress sims will fail if resumed
  - **Mitigation**: User can restart simulation (acceptable for refactoring)
  - **Alternative**: Complete any running simulations before updating code

- [x] **Q11.8**: Should we keep a backup of data/configs/draft_config.json?
  - **RESOLVED**: No - value (163) will be transferred to league_config.json
  - **Rationale**: Value preserved in new location, no backup needed

#### Relationship to Other Features (5 items)

- [x] **Q12.1**: Does this affect Starter Helper Mode?
  - **RESOLVED**: NO - Starter Helper Mode unaffected
  - **Verification**: Uses weekly configs only, no draft_config references
  - **No changes needed**: StarterHelperModeManager uses regular ConfigManager

- [x] **Q12.2**: Does this affect Trade Simulator Mode?
  - **RESOLVED**: NO - Trade Simulator Mode unaffected
  - **Verification**: Uses weekly configs only, no draft_config references
  - **No changes needed**: TradeSimulatorModeManager uses regular ConfigManager

- [x] **Q12.3**: Does this affect Modify Player Data Mode?
  - **RESOLVED**: NO - Modify Player Data Mode unaffected
  - **Verification**: Doesn't use ConfigManager for scoring
  - **No changes needed**: No draft_config references

- [x] **Q12.4**: Does this affect historical data compilation?
  - **RESOLVED**: NO - Historical data compilation unaffected
  - **Verification**: Separate system, no draft_config usage
  - **No changes needed**: If historical_data_compiler exists, verify no draft_config references

- [x] **Q12.5**: Does this affect player data fetcher?
  - **RESOLVED**: NO - Player data fetcher unaffected
  - **Verification**: Separate system, no draft_config references
  - **No changes needed**: player-data-fetcher/ is independent

---

## Vagueness Resolution

Items requiring clarification from specs (identified during Phase 2.8 Vagueness Audit):

- [x] **V1**: "simplify Add to Roster mode" - specify exact code changes needed
  - **RESOLVED**: Remove self.draft_config from LeagueHelperManager, pass regular config to AddToRosterModeManager, add is_draft_mode=True to score_player calls (Q3.1-Q3.6)

- [x] **V2**: "draft mode detection" - define complete mechanism (not just "somehow detect")
  - **RESOLVED**: Add is_draft_mode keyword-only parameter to score_player(), AddToRosterModeManager passes is_draft_mode=True (Q2.1-Q2.7)

- [x] **V3**: "update ConfigManager" - list specific methods that need changes
  - **RESOLVED**: Remove use_draft_config parameter from __init__, remove _load_draft_config() method, add draft_normalization_max_scale property, add validation in _validate_league_config (Q1.1-Q1.9, Q10.3)

- [x] **V4**: "remove ROS assessment" - list all code paths that invoke ROS
  - **RESOLVED**: 5 files identified - AccuracySimulationManager (remove run_ros_optimization, update run_both), AccuracyResultsManager (remove 'ros' from best_configs and file_mapping), AccuracyCalculator (remove calculate_ros_mae), ParallelAccuracyRunner (remove _evaluate_config_ros_worker), run_accuracy_simulation.py (update comments) (Q4.1-Q4.12)

- [x] **V5**: "same scoring method" - clarify if draft mode uses identical algorithm with different scale only
  - **RESOLVED**: YES - identical algorithm, only normalization scale differs. Draft mode: config.draft_normalization_max_scale (163), Regular: config.normalization_max_scale (from weekly config) (Q2.6, Q7.4)

---

## Working Reference Comparison

**Reference Feature**: None (this is a removal/refactoring, not implementing new functionality)

**Similar Patterns**:
- Weekly config loading (ConfigManager._load_week_config) - can use as pattern for DRAFT param loading
- Parameter validation (ConfigManager._load_config:L1005-1029) - pattern for validating DRAFT_NORMALIZATION_MAX_SCALE

---

## Assumptions to Verify

(Completed during Phase 2.9 Assumptions Audit)

| Assumption | Basis | Risk if Wrong | Mitigation |
|------------|-------|---------------|------------|
| **A1**: Only NORMALIZATION_MAX_SCALE needs draft-specific value | User notes state "only parameter... that has any meaningful impact" | Other params may also matter, wasted optimization potential | Verify with historical simulation data before removing ROS optimization |
| **A2**: Draft happens during season (week 1-17, not pre-season) | ConfigManager validates week 1-17 (L259) | Pre-season drafts (week 0) may fail | Add special handling for week <1, default to week1-5 config |
| **A3**: Add to Roster mode is ONLY place draft_config used | grep shows only LeagueHelperManager uses use_draft_config=True | Hidden usages break when draft_config removed | Grep for all draft_config references before removing |
| **A4**: NORMALIZATION_MAX_SCALE belongs in weekly configs, not league_config | Observed pattern: prediction params in weekly, strategy in league | Breaking architecture pattern causes confusion | Validate this is correct pattern before deciding where DRAFT param goes (Q1.1) |
| **A5**: run_ros_optimization() is unused/deprecated | No CLI flag for --ros mode | Method may be called programmatically | Grep for all callers of run_ros_optimization before removing |
| **A6**: Draft mode uses ROS projections (use_weekly_projection=False) | Draft is season-long decision | If draft uses weekly, our approach is wrong | Verify AddToRosterMode calls score_player with use_weekly_projection=False |
| **A7**: Single ConfigManager can serve all modes | Modes differ only in weekly config loaded | Some mode may need different parameters | Test each mode after consolidation |
| **A8**: Accuracy optimal folders always have 5 files currently | Git status shows many folders with draft_config.json | Inconsistent structure breaks find_baseline_config | Check actual folder contents before updating validation |
| **A9**: Win-rate sim outputs draft_config.json currently | ResultsManager has 'ros' mapping | May not actually create file | Examine actual optimal_* folders to verify |
| **A10**: draft_player_manager is separate from player_manager | LeagueHelperManager has both | May be same instance, just named differently | Check LeagueHelperManager initialization code |
| **A11**: Test suite is comprehensive enough to catch breakage | 2,200+ tests mentioned in docs | Coverage gaps may miss regressions | Review test coverage for affected modules |
| **A12**: DRAFT_NORMALIZATION_MAX_SCALE won't conflict with existing params | New parameter name | Name collision or validation conflict | Check ConfigKeys for namespace conflicts |
| **A13**: Removing second ConfigManager won't break memory references | Modes store config reference | Shared mutable config could cause bugs | Ensure modes don't modify config state |
| **A14**: ConfigGenerator horizon methods are only used for accuracy sim | Methods mention horizons | Win-rate sim might also use horizons | Check all callers of get_config_for_horizon |
| **A15**: Intermediate folders are resumable after this change | Sim uses intermediate folders to resume | Old intermediate folders become incompatible | Add version check or clear old intermediates |

---

## Testing Requirements

(Completed during Phase 2.10 Testing Requirements Analysis)

### Integration Points to Test

| Component A | Component B | Integration Mechanism | How to Verify |
|-------------|-------------|----------------------|---------------|
| ConfigManager | PlayerManager | config.draft_normalization_max_scale property | Unit test: ConfigManager loads param, PlayerManager accesses it |
| PlayerManager | AddToRosterModeManager | score_player(is_draft_mode=True) call | Unit test: Mock score_player, verify is_draft_mode=True passed |
| AddToRosterModeManager | LeagueHelperManager | Receives config instance | Integration test: Full draft recommendation flow |
| AccuracySimulationManager | ConfigGenerator | get_config_for_horizon() without 'ros' | Unit test: Verify only 4 horizons generated |
| AccuracyResultsManager | File system | save_optimal_configs creates 4 files | Integration test: Run accuracy sim, check output folder |
| ResultsManager (win-rate) | ConfigGenerator | DRAFT_NORMALIZATION_MAX_SCALE in param list | Unit test: Verify param included in generation |
| find_baseline_config | Optimal folders | Folder structure validation | Integration test: Detects folders without draft_config.json |

### Smoke Test Success Criteria

**After Configuration Changes:**
- [ ] ConfigManager loads league_config.json without errors
- [ ] DRAFT_NORMALIZATION_MAX_SCALE accessible via config.draft_normalization_max_scale
- [ ] ConfigManager no longer accepts use_draft_config parameter (or errors/warns if True)
- [ ] Single ConfigManager instance created by LeagueHelperManager

**After Scoring Changes:**
- [ ] score_player() accepts is_draft_mode parameter
- [ ] Draft mode uses draft_normalization_max_scale (value 163)
- [ ] Non-draft mode uses normalization_max_scale (value from weekly config)
- [ ] Add to Roster mode generates recommendations successfully

**After Accuracy Sim Changes:**
- [ ] Accuracy sim runs without errors
- [ ] accuracy_optimal folder contains exactly 4 weekly config files
- [ ] No draft_config.json created in accuracy_optimal folders
- [ ] No ROS-related log messages appear
- [ ] Simulation ~20% faster than before

**After Win-Rate Sim Changes:**
- [ ] Win-rate sim runs without errors
- [ ] optimal_* folders contain league_config.json + 4 weekly files (5 total)
- [ ] No draft_config.json created in optimal_* folders
- [ ] DRAFT_NORMALIZATION_MAX_SCALE tested during parameter optimization

**Integration Tests:**
- [ ] Full Add to Roster mode workflow (select mode → get recommendations → verify scoring used draft scale)
- [ ] Full accuracy simulation (run → verify 4 horizons → check output files)
- [ ] Full win-rate simulation (run → verify draft param tested → check output files)
- [ ] League Helper with all 4 modes (verify no draft_config references)

### Expected vs Actual Validation

| Metric | Expected Value/Pattern | How to Check |
|--------|------------------------|--------------|
| ConfigManager instances | 1 (not 2) | LeagueHelperManager has self.config but not self.draft_config |
| Accuracy optimal files | 4 files (week1-5.json, week6-9.json, week10-13.json, week14-17.json) | List files in accuracy_optimal folder |
| Win-rate optimal files | 5 files (league_config.json + 4 weekly) | List files in optimal_* folder |
| Draft normalization value | 163 (from old draft_config.json) | Check league_config.json DRAFT_NORMALIZATION_MAX_SCALE |
| Accuracy sim speed | ~20% faster | Time accuracy sim before/after (5 horizons vs 4 horizons) |
| score_player parameters | 14 params (was 13, +is_draft_mode) | Inspect method signature |
| ConfigManager._load_draft_config | Method doesn't exist | Grep for _load_draft_config, should find 0 results |
| best_configs dict keys | 4 keys (week_1_5, week_6_9, week_10_13, week_14_17) | Inspect AccuracyResultsManager.__init__ |
| Test pass rate | 100% (all tests pass) | Run python tests/run_all_tests.py |

---

## CODEBASE VERIFICATION STATUS

**Round 1: Initial Research - COMPLETED**
- Items researched: 87
- Items resolved from code: 15
- Items needing user decision: 45
- Items remaining unknown: 27

**Key Findings from Round 1:**
1. NORMALIZATION_MAX_SCALE is in weekly configs, NOT league_config (major architectural insight)
2. Two ConfigManager instances currently exist (LeagueHelperManager.py:L74, L80)
3. AccuracySimulationManager has run_ros_optimization method (L575) but CLI doesn't have --ros flag
4. ResultsManager maps 'ros' -> 'draft_config.json' in multiple places (L427, 539, 606, 626)
5. score_player has no draft mode parameter currently (PlayerManager.py:L565)
6. player_scoring.py uses config.normalization_max_scale directly (L163, 168, 458)
7. 15+ existing draft_config.json files in simulation output folders
8. AccuracyResultsManager has 'ros' in best_configs dict (L183)

**Round 2: Skeptical Re-verification - PENDING**
- Status: Ready to begin after initial questions reviewed
- Focus areas: Parameter architecture decision, draft mode detection approach, ROS removal completeness

---

## Notes

- **CRITICAL DECISION**: Where DRAFT_NORMALIZATION_MAX_SCALE lives affects entire implementation (Q1.1)
- **ARCHITECTURE INSIGHT**: Prediction params (NORMALIZATION_MAX_SCALE) live in weekly configs, strategy params live in league_config
- All items remain [ ] pending until user reviews and approves resolutions in Phase 4
- Questions marked with "?" need user input or investigation
- Questions with "Recommendation: ?" need codebase verification or user preference
