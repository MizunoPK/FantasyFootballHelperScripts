# TODO: Additive Matchup and Schedule Scoring Implementation

**Objective**: Convert matchup and schedule scoring from multiplicative to additive bonus system

**Status**: IMPLEMENTATION 97% COMPLETE - Phases 1-3 Done, Phase 4 Nearly Complete (97.1% tests passing)

**Workflow**: Implement Phases 1-5 → User runs simulation (Phase 6) → User decides to keep or revert

**Important**: Keep this file updated with progress as you complete each task for continuity across sessions.

**Progress Summary (2025-10-28)**:
- ✅ Phase 1: Configuration Updates COMPLETE
- ✅ Phase 2: Scoring Algorithm Changes COMPLETE
- ✅ Phase 3: Simulation System Updates COMPLETE
- ✅ Phase 4: Testing 97% COMPLETE (1886/1942 tests passing - 97.1%)
  - ✅ Created test_ConfigManager_impact_scale.py (5 validation tests)
  - ✅ Fixed all ConfigManager test fixtures (thresholds, max_positions, flex_eligible)
  - ✅ Fixed test_FantasyTeam.py, test_player_scoring.py, test_PlayerManager_scoring.py fixtures
  - ✅ Fixed test_config_generator.py (parameter count, assertions, IMPACT_SCALE)
  - ✅ Fixed AddToRosterMode test fixtures
  - ⏳ 56 tests still failing (minor fixture/assertion issues in ReserveAssessmentMode, integration tests)
- ⏸️ Phase 5: Documentation PENDING
- ⏸️ Phase 6-7: User-driven simulation and evaluation

**Test Pass Rate Progress**:
- Start of session: 82.5% (1602/1942)
- Current: 97.1% (1886/1942)
- Improvement: +284 tests fixed, +14.6% pass rate

**Iteration 1 Changes**:
- Added specific line numbers for all code modifications
- Identified exact implementation patterns (draft_order_bonus as reference)
- Confirmed ConfigManager already supports parameterized thresholds
- Identified config access pattern: `self.config.matchup_scoring.get('IMPACT_SCALE', default)`
- Added ConfigGenerator parameter definition format and ranges
- Need to research: How IMPACT_SCALE is written to generated configs (Phase 3.2)

**Iteration 2 Changes**:
- Found `create_config_dict()` method in ConfigGenerator (line 612-653)
- Identified exact location to add IMPACT_SCALE application: after line 636
- Code pattern: `params['MATCHUP_SCORING']['IMPACT_SCALE'] = combination['MATCHUP_IMPACT_SCALE']`
- No existing PlayerScoringCalculator test file - need to create new one
- Found ConfigManager test patterns in `test_ConfigManager_thresholds.py`
- Test pattern: Use fixtures, Mock objects, temp configs

**Iteration 3 Changes**:
- Found existing `test_player_scoring.py` - ADD tests to this file instead of creating new one
- PlayerScoringCalculator imported by: PlayerManager, test files only
- No IMPACT_SCALE usage in codebase yet (safe to add)
- Scoring methods only in player_scoring.py (no circular import risk)
- Simulation files use matchup_score but don't call scoring methods directly
- All requirements from original spec are covered in TODO

**Iteration 4 Changes** (Validating Question Answers):
- ✅ Q1: Values 150.0 and 80.0 correctly in Phase 1.1
- ✅ Q2: ≥70% win rate correctly in Phase 6.2
- ⚠️ Q3: Documentation timing issue - Phase 6 after Phase 5, should be before
- ✅ Q4: Update tests immediately correctly in Phase 4.2
- ✅ Q5: Full re-optimization correctly in Phase 6.1
- ✅ Q6: Error if missing correctly in Phase 1.2
- Fixed: Access pattern for REQUIRED IMPACT_SCALE (direct dict access, no .get())
- Fixed: Bonus formula simplified (multiplier already weighted by ConfigManager)
- Fixed: Added direct access pattern reference (consistency_scoring line 178)

**Iteration 5 Changes** (Phase Ordering and Dependencies):
- ✅ Fixed Q3 issue: Reordered phases so Documentation (Phase 5) before Simulation (Phase 6)
- New order: Config → Code → Simulation Updates → Testing → Documentation → Simulation → Final
- Verified no circular dependencies between phases
- Added exact ValueError pattern for IMPACT_SCALE validation (lines 767-769 pattern)
- Added specific test requirements for both matchup and schedule IMPACT_SCALE validation
- Confirmed task dependencies allow sequential execution

**Iteration 6 Changes** (Final Verification):
- ✅ Verified all 7 phases have clear task groups (20 total task groups)
- ✅ Confirmed all CRITICAL/MANDATORY/BLOCKER checkpoints present
- ✅ Verified cleanup tasks present in Phase 7.3
- ✅ All question answers fully integrated and marked appropriately
- ✅ No conflicting requirements found
- ✅ Session continuity tasks present (move files, delete questions, finalize docs)
- ✅ Pre-commit validation properly placed at Phase 7.2
- ✅ Final verification protocol at Phase 7.1
- Plan is comprehensive and ready for implementation

---

## Phase 1: Configuration Updates

### 1.1 Add IMPACT_SCALE to league_config.json (REQUIRED)
- [ ] **File**: `data/league_config.json`
- [ ] **CRITICAL**: Add `IMPACT_SCALE: 150.0` to `MATCHUP_SCORING` section (REQUIRED parameter)
- [ ] **CRITICAL**: Add `IMPACT_SCALE: 80.0` to `SCHEDULE_SCORING` section (REQUIRED parameter)
- [ ] Convert MATCHUP_SCORING.THRESHOLDS to parameterized format:
  - BASE_POSITION: 0
  - DIRECTION: "BI_EXCELLENT_HI"
  - STEPS: 7.5
- [ ] Convert SCHEDULE_SCORING.THRESHOLDS to parameterized format:
  - BASE_POSITION: 0
  - DIRECTION: "INCREASING"
  - STEPS: 8
- [ ] Verify JSON syntax is valid
- [ ] **Test**: Manually load config to ensure no parsing errors

### 1.2 Update ConfigManager validation
- [ ] **File**: `league_helper/util/ConfigManager.py`
- [ ] **Location**: `_extract_parameters()` method (line 743-910)
- [ ] **Insert After**: Line 793 (after schedule_scoring assignment)
- [ ] Add IMPACT_SCALE validation for MATCHUP_SCORING:
  ```python
  # Validate IMPACT_SCALE is present (required as of additive scoring)
  if 'IMPACT_SCALE' not in self.matchup_scoring:
      raise ValueError("MATCHUP_SCORING missing required parameter: IMPACT_SCALE")
  ```
- [ ] Add IMPACT_SCALE validation for SCHEDULE_SCORING:
  ```python
  if 'IMPACT_SCALE' not in self.schedule_scoring:
      raise ValueError("SCHEDULE_SCORING missing required parameter: IMPACT_SCALE")
  ```
- [ ] **Code Pattern**: Similar to required parameter validation on lines 767-769
- [ ] **Note**: ConfigManager already has `calculate_thresholds()` method (line 582) that handles parameterized thresholds
- [ ] **Note**: Parameterized thresholds are auto-calculated in `_extract_parameters()` (lines 890-910)
- [ ] **Test**: Unit test verifying ValueError raised when IMPACT_SCALE missing from matchup_scoring
- [ ] **Test**: Unit test verifying ValueError raised when IMPACT_SCALE missing from schedule_scoring
- [ ] **Test**: Unit test verifying successful load when both IMPACT_SCALE present

---

## Phase 2: Scoring Algorithm Changes

### 2.1 Modify matchup multiplier to additive bonus
- [ ] **File**: `league_helper/util/player_scoring.py`
- [ ] **Method**: `_apply_matchup_multiplier()` (line 557-566)
- [ ] **Current Code**: Returns `player_score * multiplier` (line 566)
- [ ] **Change to**: Return `player_score + bonus`
- [ ] Implement bonus calculation:
  - Get IMPACT_SCALE: `impact_scale = self.config.matchup_scoring['IMPACT_SCALE']` (direct access, REQUIRED)
  - Get weighted multiplier: `multiplier, rating = self.config.get_matchup_multiplier(p.matchup_score)` (already weighted)
  - **Note**: Returned multiplier already has WEIGHT applied (ConfigManager line 1001)
  - Calculate: `bonus = (impact_scale * multiplier) - impact_scale`
- [ ] Update reason string: `f"Matchup: {rating} ({bonus:+.1f} pts)"` (change from `{multiplier:.2f}x`)
- [ ] **Pattern Reference**: `_apply_draft_order_bonus()` (line 599-613) shows additive pattern
- [ ] **Pattern Reference**: Direct dict access like `self.config.consistency_scoring[self.config.keys.MIN_WEEKS]` (line 178)
- [ ] **Test**: Unit test for bonus calculation
- [ ] **Test**: Unit test verifying same bonus for different base scores

### 2.2 Modify schedule multiplier to additive bonus
- [ ] **File**: `league_helper/util/player_scoring.py`
- [ ] **Method**: `_apply_schedule_multiplier()` (line 568-597)
- [ ] **Current Code**: Returns `new_score = player_score * multiplier` (line 589)
- [ ] **Change to**: Return `player_score + bonus`
- [ ] Implement bonus calculation:
  - Get IMPACT_SCALE: `impact_scale = self.config.schedule_scoring['IMPACT_SCALE']` (direct access, REQUIRED)
  - Get weighted multiplier: `multiplier, rating = self.config.get_schedule_multiplier(schedule_value)` (already weighted)
  - **Note**: Returned multiplier already has WEIGHT applied (ConfigManager line 1001)
  - Calculate: `bonus = (impact_scale * multiplier) - impact_scale`
- [ ] Update reason string: `f"Schedule: {rating} (avg opp rank: {schedule_value:.1f}, {bonus:+.1f} pts)"` (change from `{multiplier:.2f}x`)
- [ ] Update debug log (line 592-594) to use bonus instead of multiplier
- [ ] **Pattern Reference**: `_apply_draft_order_bonus()` (line 599-613) shows additive pattern
- [ ] **Pattern Reference**: Direct dict access like `self.config.consistency_scoring[self.config.keys.MIN_WEEKS]` (line 178)
- [ ] **Test**: Unit test for bonus calculation
- [ ] **Test**: Unit test verifying same bonus for different base scores

---

## Phase 3: Simulation System Updates

### 3.1 Add IMPACT_SCALE parameters to ConfigGenerator
- [ ] **File**: `simulation/ConfigGenerator.py`
- [ ] **Location**: PARAM_DEFINITIONS dict (line 54-72)
- [ ] Add `MATCHUP_IMPACT_SCALE: (25.0, 100.0, 200.0)` to PARAM_DEFINITIONS
  - Format: (range_val, min_val, max_val)
  - Range: ±25 from optimal (baseline 150)
  - Bounds: 100-200
- [ ] Add `SCHEDULE_IMPACT_SCALE: (20.0, 40.0, 120.0)` to PARAM_DEFINITIONS
  - Range: ±20 from optimal (baseline 80)
  - Bounds: 40-120
- [ ] **Pattern Reference**: NORMALIZATION_MAX_SCALE (line 55) uses same tuple format
- [ ] **Note**: `generate_all_parameter_value_sets()` (line 236) automatically includes all PARAM_DEFINITIONS
- [ ] **Test**: Verify parameters are included in generated configs
- [ ] **Test**: Verify value ranges are correct (use logging to check)

### 3.2 Update config application logic
- [ ] **File**: `simulation/ConfigGenerator.py`
- [ ] **Method**: `create_config_dict()` (line 612-653)
- [ ] **Insert After**: Line 636 (after DRAFT_ORDER_BONUSES updates)
- [ ] Add two lines:
  ```python
  params['MATCHUP_SCORING']['IMPACT_SCALE'] = combination['MATCHUP_IMPACT_SCALE']
  params['SCHEDULE_SCORING']['IMPACT_SCALE'] = combination['SCHEDULE_IMPACT_SCALE']
  ```
- [ ] **Pattern Reference**: NORMALIZATION_MAX_SCALE application (line 632)
- [ ] **Note**: Direct assignment to scoring section dict, NOT nested like THRESHOLDS
- [ ] **Note**: Combination dict will have these keys from generate_all_parameter_value_sets()
- [ ] **Test**: Generate test configs and verify IMPACT_SCALE present and correct
- [ ] **Test**: Verify values vary across generated configs

---

## Phase 4: Testing

### 4.1 Add unit tests for additive scoring
- [ ] **File**: `tests/league_helper/util/test_player_scoring.py` (EXISTING FILE - ADD TO IT)
- [ ] **Location**: Add new test class at end of file
- [ ] **Pattern Reference**: Existing fixtures in file (mock_data_folder, mock_config, etc.)
- [ ] Add Test Class: `TestAdditiveScoringBonuses` with these tests:
  - `test_matchup_bonus_calculation_with_excellent_rating` - EXCELLENT matchup → expected bonus
  - `test_schedule_bonus_calculation_with_good_rating` - GOOD schedule → expected bonus
  - `test_same_bonus_for_different_base_scores` - Elite (120) vs Waiver (50) get same bonus
  - `test_impact_scale_affects_bonus_magnitude` - Varying IMPACT_SCALE changes bonus
  - `test_weight_affects_bonus_magnitude` - Varying WEIGHT changes bonus
  - `test_missing_impact_scale_raises_error` - Verify ValueError when IMPACT_SCALE missing
  - `test_bonus_formula_accuracy` - Verify: `(IMPACT_SCALE * multiplier^WEIGHT) - IMPACT_SCALE`
- [ ] Mock config.matchup_scoring.get() and config.schedule_scoring.get()
- [ ] Use pytest.approx(abs=0.01) for float comparisons
- [ ] Run tests: `pytest tests/league_helper/util/test_player_scoring.py::TestAdditiveScoringBonuses -v`

### 4.2 Update existing scoring tests
- [ ] **File**: `tests/league_helper/util/test_PlayerManager_scoring.py`
- [ ] Review tests that check matchup/schedule scoring
- [ ] Update assertions to expect additive bonuses instead of multiplicative
- [ ] Search for tests checking multiplier values (e.g., `* 1.05`)
- [ ] Update to check for bonus addition (e.g., `+ 7.26`)
- [ ] Verify score calculation tests pass
- [ ] **Note**: May need to update expected score values in assertions
- [ ] Run just this test file: `pytest tests/league_helper/util/test_PlayerManager_scoring.py -v`

### 4.3 Update integration tests
- [ ] **File**: `tests/integration/test_league_helper_integration.py`
- [ ] Verify draft recommendations work with additive system
- [ ] Test that streaming candidates aren't over-valued
- [ ] **Test**: Full scoring workflow integration

### 4.4 Run complete test suite (MANDATORY)
- [ ] **Command**: `python tests/run_all_tests.py`
- [ ] **Requirement**: 100% pass rate (all 1,811 tests)
- [ ] Fix any failing tests
- [ ] Re-run until all tests pass
- [ ] **BLOCKER**: Cannot proceed without 100% pass rate

---

## Phase 5: Documentation

### 5.1 Update README.md
- [ ] **File**: `README.md`
- [ ] Update scoring algorithm description (Steps 6 and 7 are now additive)
- [ ] Add IMPACT_SCALE to configuration parameters section
- [ ] Update example calculations to show additive bonuses
- [ ] **Location**: Around line 270 (Configuration section)

### 5.2 Update ARCHITECTURE.md
- [ ] **File**: `ARCHITECTURE.md`
- [ ] Update scoring system documentation (lines 192-210)
- [ ] Clarify multiplicative vs additive factor philosophy
- [ ] Update data flow examples with new calculation
- [ ] Add IMPACT_SCALE parameter explanation

### 5.3 Update CLAUDE.md (if needed)
- [ ] **File**: `CLAUDE.md`
- [ ] Check if workflow documentation needs updates
- [ ] Likely no changes needed (workflow unaffected)

### 5.4 Create code changes documentation
- [ ] **File**: Create `updates/additive_matchup_schedule_scoring_code_changes.md`
- [ ] Document all file modifications with line numbers
- [ ] Include before/after code snippets
- [ ] Explain rationale for each change
- [ ] Document configuration changes
- [ ] Document test modifications
- [ ] Update incrementally as work progresses

---

## Phase 6: Simulation Validation and Optimization (USER-DRIVEN)

**IMPORTANT**: Phase 6 is the USER'S responsibility. Implementation work stops after Phase 5.

### 6.1 User runs full parameter re-optimization
- [ ] **USER ACTION**: Run `python run_simulation.py iterative --sims 100 --workers 8`
- [ ] **USER ACTION**: Re-optimize ALL parameters (including new IMPACT_SCALE values)
- [ ] Target: 16+ parameters optimized with additive scoring system
- [ ] **Note**: This will take several hours (or days depending on configuration)
- [ ] **USER ACTION**: Record final optimized win rate
- [ ] **USER ACTION**: Document optimized parameter values

### 6.2 User evaluates results against acceptance criteria
- [ ] **USER ACTION**: Check if optimized win rate ≥70%
- [ ] **USER ACTION - If ≥70%**: Accept implementation, update config with optimal values, proceed to Phase 7
- [ ] **USER ACTION - If <70%**: Revert commit, keep current system, document findings
- [ ] **USER ACTION**: Review draft behavior patterns for any anomalies
- [ ] **USER ACTION**: Check for streaming behavior issues (over-valuing waiver players)

### 6.3 User updates config with optimal values (if accepted)
- [ ] **USER ACTION**: Update `data/league_config.json` with optimized IMPACT_SCALE values
- [ ] **USER ACTION**: Update all other optimized parameter values
- [ ] **USER ACTION**: Verify config is valid JSON
- [ ] **USER ACTION**: Test config loads without errors
- [ ] **USER ACTION**: Commit updated config (or request commit)

---

## Phase 7: Final Validation and Completion (ONLY IF USER ACCEPTS RESULTS)

**IMPORTANT**: Phase 7 only happens if user evaluates results in Phase 6 and decides to keep the implementation.

### 7.1 Requirement Verification Protocol (MANDATORY - if keeping changes)
- [ ] Re-read `updates/additive_matchup_schedule_scoring.txt`
- [ ] Create checklist of EVERY requirement
- [ ] Verify each requirement is implemented
- [ ] Mark requirements as ✅ DONE or ❌ MISSING
- [ ] If ANY missing: create completion TODO and implement
- [ ] Document verification in code changes file

### 7.2 Pre-Commit Validation (MANDATORY - if keeping changes)
- [ ] Run `python tests/run_all_tests.py`
- [ ] Verify 100% pass rate
- [ ] Run manual testing (if applicable)
- [ ] Review all changes with `git status` and `git diff`
- [ ] Verify documentation is complete and accurate

### 7.3 Finalize and Move Files (if keeping changes)
- [ ] Finalize code changes documentation file
- [ ] Move `additive_matchup_schedule_scoring.txt` to `updates/done/`
- [ ] Move `additive_matchup_schedule_scoring_code_changes.md` to `updates/done/`
- [ ] Move `additive_matchup_schedule_scoring_todo.md` to `updates/done/`
- [ ] Delete `additive_matchup_schedule_scoring_questions.md` (after answers integrated)
- [ ] Mark objective as COMPLETE

### 7.4 Alternative: If Reverting Changes
- [ ] **USER ACTION**: Run `git revert <commit_hash>` to undo implementation
- [ ] **USER ACTION**: Document why results were unacceptable (win rate, behavior issues, etc.)
- [ ] **USER ACTION**: Keep planning files in `updates/` folder for future reference
- [ ] **USER ACTION**: Update planning docs with lessons learned

---

## Verification Summary

**Status**: All Verification Complete - Plan Finalized and Ready for Implementation

**Verification Rounds Completed**: 6/6 ✅
- First Round (before questions): 3/3 iterations ✅
- Second Round (after answers): 3/3 iterations ✅

**Requirements Added After Drafting**: 0
- All requirements from original spec covered in draft
- No missing requirements discovered during 6 verification iterations
- User answers integrated without requiring new requirements

**Key Patterns Identified**:
1. Additive pattern: `player_score + bonus` with `{bonus:+.1f} pts` format (draft_order_bonus)
2. Config access: `self.config.scoring_dict.get('KEY', default)` for optional values
3. ConfigGenerator param format: `(range_val, min_val, max_val)` tuple in PARAM_DEFINITIONS
4. Config application: Direct assignment `params['SECTION']['KEY'] = combination['PARAM']`
5. Test pattern: Existing `test_player_scoring.py` has fixtures and structure to extend

**Critical Dependencies**:
- ConfigManager.calculate_thresholds() already supports parameterized thresholds ✅
- ConfigManager._extract_parameters() auto-calculates thresholds on load ✅
- ConfigGenerator.generate_all_parameter_value_sets() auto-includes PARAM_DEFINITIONS ✅
- No circular imports: PlayerScoringCalculator only imported by PlayerManager and tests ✅

**Risk Areas**:
1. **Existing Tests**: test_PlayerManager_scoring.py will need updates for additive expectations
2. **Streaming Behavior**: Additive bonuses may over-value waiver players with good matchups
3. **Simulation Win Rate**: Changes could affect optimal strategy (need to validate ≥70%)
4. **Breaking Change**: IMPACT_SCALE is REQUIRED in config - existing configs will fail to load

**User Answers Summary**:
- Q1: Use spec values (MATCHUP=150.0, SCHEDULE=80.0) as starting point ✅
- Q2: Minimum acceptable win rate ≥70% ✅
- Q3: Update documentation after implementation, before simulation ✅
- Q4: Update all existing tests immediately for clean suite ✅
- Q5: Run full re-optimization of all parameters (comprehensive approach) ✅
- Q6: Require explicit IMPACT_SCALE in config (error if missing, breaking change) ✅

**Implementation Strategy**:
- Direct implementation of additive scoring (no A/B testing or feature flags)
- Implementation work stops after Phase 5 (Documentation)
- User runs simulation and evaluates results in Phase 6
- User decides to keep (≥70% win rate) or revert (<70% win rate)
- Breaking change: IMPACT_SCALE is REQUIRED (existing configs will fail)

**Next Step**: Begin implementation following Phase 1 → Phase 7 sequence

---

## Notes

- **Implementation Approach**: Direct implementation, no feature flags or A/B testing
- **Workflow Responsibility**:
  - Agent: Implements Phases 1-5 (Config, Code, Tests, Documentation)
  - User: Runs simulation and evaluates results (Phase 6)
  - User: Decides to keep (Phase 7) or revert changes based on performance
- **Rollback Plan**: If simulation win rate <70%, user reverts commit and keeps current system
- **Breaking Change**: IMPACT_SCALE is REQUIRED - configs without it will fail to load (ValueError)
- **Philosophy Change**: Matchup/schedule are ENVIRONMENTAL (additive) not ABILITY (multiplicative)
- **Watch For**: Streaming behavior becoming too dominant with additive bonuses
- **Testing**: Every phase must pass 100% unit tests before proceeding
- **Session Continuity**: Update this file with progress for multi-session work
- **Optimization**: Full re-optimization of ALL parameters run by user after implementation (comprehensive approach)
