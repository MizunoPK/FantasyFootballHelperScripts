# Single Week Normalization - TODO File

## Objective Summary

Update the scoring system to normalize single-week projected scores using the same bounds as full season projected points. When scoring based on single-week projections (e.g., Starter Helper mode), the highest projected score for that week should be scaled to NORMALIZATION_MAX_SCALE, with all other scores scaled proportionally between 0 and NORMALIZATION_MAX_SCALE. This should only affect single-week modes while leaving ROS (Rest of Season) modes unchanged.

## Refined Implementation Phases

### Phase 0: Add max_weekly_projection Tracking
**File**: `league_helper/util/PlayerManager.py`

**USER CHOICE (Q1)**: Option B - Cache with dictionary `{week_num: max_projection}`

- [ ] **Task 0.1**: Add `max_weekly_projections` dict field to PlayerManager.__init__ (line ~128)
  - Initialize to empty dict alongside existing max_projection
  - Pattern: `self.max_weekly_projections: Dict[int, float] = {}`
  - Import Dict from typing module if not already imported

- [ ] **Task 0.2**: Add cache invalidation in load_players_from_csv() method
  - Location: In `load_players_from_csv()` at line ~143 (right after `self.max_projection = 0.0`)
  - **CRITICAL**: Clear cache when reloading player data
  - Add: `self.max_weekly_projections = {}` (resets cache dict)
  - Reasoning: Player weekly projections can change when CSV is reloaded
  - Pattern matches existing max_projection reset at line 143

- [ ] **Task 0.3**: Add method `calculate_max_weekly_projection(week_num: int) -> float`
  - Location: After `load_players_from_csv()` method (~line 250)
  - **Cache check first**: `if week_num in self.max_weekly_projections: return self.max_weekly_projections[week_num]`
  - If not cached: iterate through `self.players` list
  - Call `player.get_single_weekly_projection(week_num)` for each player
  - Track maximum weekly projection value
  - **Cache the result**: `self.max_weekly_projections[week_num] = max_value`
  - Return the maximum (or 0.0 if no valid projections)
  - Add logging: DEBUG level with calculated max value and cache hit/miss status
  - Reference pattern: Similar to max_projection tracking at line 229-230

- [ ] **Task 0.4**: Add `max_weekly_projection` field to PlayerScoringCalculator
  - Location: `league_helper/util/player_scoring.py` constructor (line ~81)
  - Add to __init__ parameters and store as instance variable
  - Initialize to 0.0 by default
  - Note: This is the "current weekly max" being used for normalization, not the cache dict

### Phase 1: Modify weight_projection() Method
**File**: `league_helper/util/player_scoring.py:135-145`

**USER CHOICE (Q2)**: Option A - Return 0.0 for zero max (fail-safe, makes issues obvious)
**USER CHOICE (Q3)**: Option A - DEBUG level only (cleanest logs)

- [ ] **Task 1.1**: Update `weight_projection()` signature
  - Add optional parameter: `use_weekly_max: bool = False`
  - Preserve backward compatibility with default=False

- [ ] **Task 1.2**: Implement conditional normalization logic
  - If `use_weekly_max=True`: use `self.max_weekly_projection`
  - If `use_weekly_max=False`: use `self.max_projection` (current behavior)
  - **Safety check (Q2 choice)**: if chosen max == 0, log WARNING and return 0.0
  - WARNING log message: "Max projection is 0.0, returning 0.0 normalized score (data quality issue)"
  - Formula: `(pts / chosen_max) * self.config.normalization_max_scale`

- [ ] **Task 1.3**: Add DEBUG logging (Q3 choice)
  - DEBUG: Log which max is being used (weekly vs ROS)
  - DEBUG: Log the normalization calculation inputs and result
  - No INFO level logs (keep logs clean)

### Phase 2: Update get_weekly_projection() Method
**File**: `league_helper/util/player_scoring.py:114-142`

- [ ] **Task 2.1**: Modify call to weight_projection() at line 136
  - Change from: `weighted_projection = self.weight_projection(weekly_points)`
  - Change to: `weighted_projection = self.weight_projection(weekly_points, use_weekly_max=True)`
  - This triggers single-week normalization when scoring weekly projections

### Phase 3: Update StarterHelperModeManager
**File**: `league_helper/starter_helper_mode/StarterHelperModeManager.py`

**USER CHOICE (Q3)**: Option A - DEBUG level only (no INFO logs in mode entry)

- [ ] **Task 3.1**: Calculate max_weekly_projection before scoring loop
  - **Location**: In `optimize_lineup()` method at line ~411 (before line 412 roster loop)
  - Insert before: `scored_players = []` and the roster loop
  - Call: `max_weekly = self.player_manager.calculate_max_weekly_projection(self.config.current_nfl_week)`
  - Update scorer: `self.player_manager.scoring_calculator.max_weekly_projection = max_weekly`
  - **No INFO log here** (Q3 choice: DEBUG only)
  - DEBUG log will be in calculate_max_weekly_projection() method instead

- [ ] **Task 3.2**: Verify no changes needed to score_player call
  - Current call at line 365-370 already uses `use_weekly_projection=True`
  - No changes needed - new logic is automatic when use_weekly_projection=True

### Phase 4: Update Unit Tests
**File**: `tests/league_helper/util/test_PlayerManager_scoring.py`

**USER CHOICE (Q4)**: Option A - Proactively update all affected tests (thorough)
**USER CHOICE (Q6)**: Option A - Add explicit verification tests for backward compatibility

- [ ] **Task 4.1**: Update existing test `test_normalization_with_weekly_projection_enabled` (line 426)
  - **Proactive update (Q4 choice)**: Update to reflect new weekly max calculation
  - Add: Set `player_manager.max_weekly_projections[6] = 30.0` (cache the weekly max for week 6)
  - Add: Set `scoring_calculator.max_weekly_projection = 30.0` (current weekly max)
  - Update assertion: Expected should be `(30/30) * 100 = 100.0` (full scale usage)
  - Document: This tests that weekly scores are normalized against weekly max, not ROS max

- [ ] **Task 4.2**: Add new test `test_weekly_normalization_uses_weekly_max`
  - Create player with weekly projection of 25.0
  - Set max_projection = 400.0 (ROS max)
  - Set max_weekly_projection = 30.0 (weekly max)
  - Call weight_projection(25.0, use_weekly_max=True)
  - Assert result = (25/30) * 100 = 83.33 (uses weekly max)
  - Call weight_projection(25.0, use_weekly_max=False)
  - Assert result = (25/400) * 100 = 6.25 (uses ROS max)

- [ ] **Task 4.3**: Add test `test_calculate_max_weekly_projection`
  - Create multiple players with various weekly projections
  - Call PlayerManager.calculate_max_weekly_projection(week_num)
  - Assert returns the maximum weekly projection for that week
  - Test edge case: No players have valid projections (should return 0.0)
  - Test caching: Call twice with same week, verify cache hit via DEBUG log

- [ ] **Task 4.4**: Add test `test_weekly_normalization_zero_max_handling`
  - Set max_weekly_projection = 0.0
  - Call weight_projection(25.0, use_weekly_max=True)
  - Assert returns 0.0 (graceful handling of zero max)
  - Verify WARNING log was emitted

**File**: `tests/league_helper/util/test_player_scoring.py`

- [ ] **Task 4.5**: Add integration test for full weekly scoring flow
  - Test complete flow from get_weekly_projection() through normalization
  - Verify weekly max is used automatically when use_weekly_projection=True

**File**: `tests/league_helper/starter_helper_mode/`

- [ ] **Task 4.6**: Verify StarterHelperMode integration
  - Test that lineup optimization uses weekly-normalized scores
  - Verify scores are on full 0-N scale, not tiny values

**NEW - Backward Compatibility Tests (Q6 choice)**

**File**: `tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py`

- [ ] **Task 4.7**: Add explicit test `test_draft_helper_uses_ros_normalization`
  - **Location**: Add to test_AddToRosterModeManager.py (existing file confirmed)
  - Verify Draft Helper mode continues using ROS max_projection
  - Use existing test fixtures: mock_player_manager, mock_config
  - Create test player with ROS projection of 300.0
  - Set max_projection = 400.0, max_weekly_projections = {6: 30.0}
  - Set scoring_calculator.max_weekly_projection = 0.0 (not used for ROS mode)
  - Call player_manager.score_player with use_weekly_projection=False
  - Assert normalized score uses ROS max: (300/400) * 100 = 75.0 (not 1000.0 from 300/30)
  - Document: Ensures Draft Helper unchanged by weekly normalization feature
  - Pattern: Similar to existing test_normalization_with_weekly_projection_disabled at line 440

**File**: `tests/league_helper/trade_simulator_mode/test_trade_simulator.py`

- [ ] **Task 4.8**: Add explicit test `test_trade_simulator_uses_ros_normalization`
  - **Location**: Add to test_trade_simulator.py (existing file confirmed)
  - Verify Trade Simulator mode continues using ROS max_projection
  - Use existing fixtures: sample_players, mock_config
  - Create mock PlayerManager with ROS normalization settings
  - Similar pattern to Task 4.7 but in trade context
  - Assert normalized scores use ROS max throughout trade evaluation
  - Document: Ensures Trade Simulator unchanged by weekly normalization feature

### Phase 5: Update Documentation
**File**: `docs/scoring/01_normalization.md`

**USER CHOICE (Q5)**: Option A - Brief update (1-2 paragraphs)

- [ ] **Task 5.1**: Add brief section "Single-Week vs ROS Normalization"
  - **Brief (Q5 choice)**: 1-2 paragraphs explaining the key difference
  - Paragraph 1: Explain that weekly projections now use max weekly score for normalization
  - Paragraph 2: Quick before/after example (weekly score normalized against ROS max vs weekly max)
  - Document which modes use which normalization (Starter Helper: weekly, others: ROS)
  - Location: After line 150 (after existing normalization examples)

- [ ] **Task 5.2**: Update "How League Helper Gets the Value/Multiplier" section (brief)
  - **Brief (Q5 choice)**: 1-2 sentences about the new logic
  - Mention max_weekly_projection dict cache
  - Show updated formula with use_weekly_max parameter

- [ ] **Task 5.3**: Update code reference comments in documentation
  - Update line numbers if they changed
  - Add reference to calculate_max_weekly_projection() method
  - Keep it minimal (just the key reference points)

### Phase 6: Integration Testing
- [ ] **Task 6.1**: Run all unit tests
  - Command: `python tests/run_all_tests.py`
  - Requirement: 100% pass rate
  - Fix any failures before proceeding

- [ ] **Task 6.2**: Manual test Starter Helper mode
  - Run: `python run_league_helper.py`
  - Enter Starter Helper mode
  - Verify lineup recommendations show reasonable scores
  - Compare before/after: scores should be on full scale now (not tiny values)

- [ ] **Task 6.3**: Manual test Draft Helper mode (verify unchanged)
  - Run Draft Helper mode
  - Verify ROS scoring still works correctly
  - No regression in draft recommendations

- [ ] **Task 6.4**: Manual test Trade Simulator mode (verify unchanged)
  - Run Trade Simulator mode
  - Verify ROS scoring still works correctly
  - No regression in trade evaluations

### Phase 7: Final Validation & Completion
- [ ] **Task 7.1**: Run complete test suite
  - Command: `python tests/run_all_tests.py`
  - Must achieve 100% pass rate
  - Document any issues and fixes

- [ ] **Task 7.2**: Update code changes documentation
  - Document all file changes with line numbers
  - Include before/after code snippets
  - Explain rationale for each change

- [ ] **Task 7.3**: Final verification
  - Re-read original objective file
  - Verify all requirements met
  - Confirm no regressions

- [ ] **Task 7.4**: Cleanup and move files
  - Move objective file to updates/done/
  - Delete questions file (if created)
  - Mark TODO as complete

## Anticipated File Modifications

**Core Files**:
- `league_helper/util/PlayerManager.py` - Main scoring logic
- `league_helper/util/FantasyPlayer.py` - score_player function (if exists here)

**Mode Files**:
- `league_helper/starter_helper_mode/StarterHelperModeManager.py` - Uses single-week scores
- `league_helper/add_to_roster_mode/AddToRosterModeManager.py` - Uses ROS scores (verify)
- `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py` - Uses ROS scores (verify)

**Test Files**:
- `tests/league_helper/util/test_PlayerManager.py` - Add normalization tests
- `tests/league_helper/starter_helper_mode/` - Verify mode behavior
- `tests/league_helper/add_to_roster_mode/` - Verify unchanged behavior

**Documentation**:
- `docs/scoring/01_normalization.md` - Document single-week normalization
- `README.md` - If user-visible changes

## Testing Requirements

**New Tests Needed**:
1. Test single-week score normalization with various score ranges
2. Test max score detection across all positions
3. Test normalization scaling formula accuracy
4. Test ROS mode preservation (no regression)
5. Test mode-specific behavior (Starter Helper vs others)

**Existing Tests to Verify**:
- All PlayerManager tests must still pass
- All mode-specific tests must still pass
- Integration tests must pass

## Documentation Requirements

- Update normalization documentation with single-week details
- Add inline code comments explaining normalization logic
- Document the differentiation between single-week and ROS scoring

## Key Findings from Iteration 1

### Current Implementation Discovery

**Normalization Location**:
- **Primary**: `league_helper/util/player_scoring.py:135-145` - `weight_projection()` method
- **Formula**: `(pts / self.max_projection) * NORMALIZATION_MAX_SCALE`
- **Config**: `NORMALIZATION_MAX_SCALE` in `ConfigManager.py:56`, loaded from `league_config.json`

**Max Projection Tracking**:
- **Set in**: `PlayerManager.load_players_from_csv()` at line 229-230
- **Tracks**: Maximum ROS projection (player.fantasy_points, ~400+ points)
- **Used for**: Both weekly AND ROS normalization (this is the problem!)

**Score Player Functions**:
- `player_scoring.py:357` - PlayerScoringCalculator.score_player()
- `PlayerManager.py:559` - PlayerManager.score_player() (wrapper)
- Both accept `use_weekly_projection` parameter to switch modes

**Weekly vs ROS Detection**:
- `use_weekly_projection=True` → calls `get_weekly_projection()`
- `use_weekly_projection=False` → uses `get_rest_of_season_projection()`
- Currently BOTH use same `max_projection` for normalization

**The Root Cause**:
- Weekly projections (~20-25 pts for top players) are normalized against ROS max (~400+ pts)
- Results in tiny normalized values (5-6 pts) instead of using full 0-N scale
- Need separate `max_weekly_projection` to fix this

### Files Using Weekly Projections

**Primary User**:
- `StarterHelperModeManager.py` - calls score_player with `use_weekly_projection=True`
- Lines 218-219 document: "use_weekly_projection=True: Uses week-specific projections, not seasonal"

**ROS Users**:
- `AddToRosterModeManager.py` - uses ROS projections
- `TradeSimulatorModeManager.py` - uses ROS projections

## Progress Tracking

**Status**: Iteration 1 complete, continuing with Iteration 2

**Discovered Issues**:
- Current implementation reuses ROS max_projection for weekly scores
- Need to track per-week maximum weekly projection
- Need to pass week-specific context to normalization logic

**Notes**:
- Keep this file updated with progress for multi-session work
- Mark tasks as complete with ✅ when finished
- Add discovered issues or blockers under each phase
- Update file paths and line numbers as implementation progresses

---

## Verification Summary

**Iterations Completed**: 3/6 (first verification round COMPLETE, awaiting questions)

**Iteration 1 Findings**:
- ✅ Located normalization implementation (player_scoring.py:135-145)
- ✅ Identified max_projection tracking (PlayerManager.py:229-230)
- ✅ Found use_weekly_projection parameter usage
- ✅ Discovered root cause: weekly scores use ROS max_projection
- ✅ Mapped modes using weekly vs ROS projections
- ❌ **Missing from TODO**: Need to track max_weekly_projection per week
- ❌ **Missing from TODO**: Need to modify weight_projection() to accept context
- ❌ **Missing from TODO**: Need to scan all players for weekly max before scoring

**Status**: Iteration 2 complete, continuing to Iteration 3

**Iteration 2 Findings**:
- ✅ Found weekly projection data access: `FantasyPlayer.get_single_weekly_projection(week_num)`
- ✅ Identified test patterns: `test_player_scoring.py` has normalization tests
- ✅ Found StarterHelperModeManager scoring call (line 365-370)
- ✅ Confirmed: `use_weekly_projection=True` is the trigger for weekly mode
- ❌ **New requirement**: Need to calculate max_weekly_projection before scoring any players
- ❌ **New requirement**: Need to pass week number to weight_projection() for context
- ❌ **New requirement**: Store max_weekly_projection in PlayerScoringCalculator

**Data Structure Decisions**:
- **Option A**: Store single `max_weekly_projection` field, recalculate for each mode invocation
- **Option B**: Store dict `{week_num: max_projection}` to cache per-week maximums
- **Recommendation**: Option A (simpler, mode invocation is rare so recalculation is acceptable)

**Implementation Strategy**:
1. Add method `_calculate_max_weekly_projection(week_num)` to PlayerManager
2. Call before entering StarterHelperMode scoring loop
3. Pass to PlayerScoringCalculator via new field or parameter
4. Modify `weight_projection()` to accept optional `is_weekly` flag
5. When `is_weekly=True`, use `max_weekly_projection` instead of `max_projection`

**Error Handling**:
- Handle case where no players have valid weekly projections (return 0.0)
- Log warning if max_weekly_projection is 0 (data quality issue)
- Gracefully degrade to ROS normalization if weekly calc fails

**Logging Strategy**:
- DEBUG: Log max_weekly_projection calculation and value
- DEBUG: Log which max is being used for normalization (weekly vs ROS)
- INFO: Log mode entry with normalization method

**Iteration 3 Findings**:
- ✅ Confirmed only StarterHelperModeManager uses `use_weekly_projection=True`
- ✅ Verified PlayerScoringCalculator is only instantiated in PlayerManager
- ✅ Found test patterns for weekly normalization in test_PlayerManager_scoring.py
- ✅ Identified integration test needs for StarterHelperMode
- ✅ No circular dependency risks identified
- ✅ Finalized task order and dependencies in refined phases

**Requirements Coverage**:
- ✅ All original requirements mapped to specific tasks
- ✅ Single-week normalization: Phases 0-3
- ✅ ROS preservation: Phase 6.3-6.4 (verification tests)
- ✅ Starter Helper mode impact: Phase 3, 6.2
- ✅ Testing: Phase 4 (6 new tests), Phase 6 (integration)
- ✅ Documentation: Phase 5

**Key Patterns Identified**:
- Max projection tracking pattern (line 229-230)
- Optional boolean parameter pattern for backward compatibility
- Test fixture pattern with mocked dependencies
- DEBUG/INFO logging conventions

**Critical Dependencies**:
- Phase 0 must complete before Phase 1 (need max_weekly_projection field)
- Phase 1-2 must complete before Phase 3 (StarterHelper needs working normalization)
- Phase 4 tests depend on Phases 0-3 implementation
- Phase 5 docs should wait until implementation stable

**Risk Areas**:
- Edge case: max_weekly_projection = 0 (handled with safety check)
- Test updates needed for changed behavior
- Existing tests expect old normalization values

**Status**: First verification round (3 iterations) COMPLETE. Questions file created and answered.

---

## User Answers Summary (Step 4 Complete)

**Question 1 - Caching Strategy**: Option B - Cache with dictionary `{week_num: max_projection}`
- Implementation: `max_weekly_projections: Dict[int, float] = {}`
- Reasoning: Faster for repeated calls, cache once per week

**Question 2 - Zero Max Handling**: Option A - Return 0.0 (fail-safe)
- Implementation: If max == 0, log WARNING and return 0.0
- Reasoning: Makes data quality issues obvious

**Question 3 - Logging Level**: Option A - DEBUG only
- Implementation: All normalization logs at DEBUG level, no INFO logs
- Reasoning: Keeps logs clean during normal operation

**Question 4 - Test Updates**: Option A - Proactively update all affected tests
- Implementation: Update test_normalization_with_weekly_projection_enabled before running tests
- Reasoning: Thorough and ensures clear test intent

**Question 5 - Documentation Detail**: Option A - Brief (1-2 paragraphs)
- Implementation: Brief section explaining weekly vs ROS normalization with simple example
- Reasoning: Quick reference without excessive detail

**Question 6 - Backward Compatibility**: Option A - Add explicit verification tests
- Implementation: New tests for Draft Helper and Trade Simulator ROS normalization
- Reasoning: Higher confidence that other modes remain unchanged

**Step 4 Status**: ✅ COMPLETE - TODO file updated with all user choices

---

## Step 5: Second Verification Round (In Progress)

**Goal**: Execute 3 more verification iterations to validate implementation plan completeness

**Iteration 4 Findings**:
- ✅ Discovered `reload_player_data()` method at line 383 calls `load_players_from_csv()`
- ✅ Found cache invalidation pattern: `max_projection` reset at line 143
- ✅ **CRITICAL**: Added Task 0.2 for cache invalidation `self.max_weekly_projections = {}`
- ✅ Verified typing imports: Dict already imported at line 35
- ✅ Confirmed no other data modification methods affect weekly projections
- ❌ **New requirement**: Must clear cache when player data reloaded
- ❌ **New task**: Task 0.2 added - cache invalidation in load_players_from_csv()

**Status**: Iteration 4/6 complete, continuing to Iteration 5

**Iteration 5 Findings**:
- ✅ Confirmed test file locations: test_AddToRosterModeManager.py and test_trade_simulator.py exist
- ✅ Found existing test pattern for weekly normalization at line 426 (test_normalization_with_weekly_projection_enabled)
- ✅ Found ROS normalization test at line 440 (test_normalization_with_weekly_projection_disabled)
- ✅ Verified test fixtures: player_manager (line 239), test_player (line 281)
- ✅ Confirmed player_manager.max_projection = 250.0 pattern (line 249)
- ✅ Found score_player mocking pattern in AddToRosterModeManager tests (line 228)
- ✅ Updated Task 4.7 and 4.8 with specific file paths and test patterns
- ✅ Verified fixture availability for backward compatibility tests
- ❌ **Important**: Task 4.1 needs to set max_weekly_projections dict AND max_weekly_projection field

**Status**: Iteration 5/6 complete, continuing to Iteration 6

**Iteration 6 Findings**:
- ✅ Verified PlayerScoringCalculator.__init__ at line 79-85 (Task 0.4 location correct)
- ✅ Verified max_projection assignment at line 81 (where to add max_weekly_projection)
- ✅ Verified weight_projection() at line 135-145 (Phase 1 location correct)
- ✅ Verified get_weekly_projection() calls weight_projection at line 120 (Phase 2 location correct)
- ✅ Verified StarterHelperModeManager.optimize_lineup() at line 380
- ✅ Confirmed scoring loop starts at line 412 (Task 3.1 insertion point: line ~411)
- ✅ Verified documentation file 01_normalization.md structure (Task 5.1 location after line 150)
- ✅ Updated Task 3.1 with precise line number (line ~411)
- ✅ **All line numbers verified and accurate**
- ✅ **No edge cases or missing requirements identified**

**Status**: Iteration 6/6 COMPLETE - Second verification round COMPLETE

---

## Step 5 Summary: Second Verification Round COMPLETE

**Iterations Completed**: 6/6 (all verification iterations complete)

**Major Discoveries Across Both Rounds**:
1. **Cache invalidation requirement** (Iteration 4): Must clear `max_weekly_projections = {}` in load_players_from_csv()
2. **Test file locations confirmed** (Iteration 5): test_AddToRosterModeManager.py and test_trade_simulator.py exist
3. **All line numbers verified** (Iteration 6): All task locations accurate and up-to-date

**Implementation Readiness**:
- ✅ All 7 phases planned with specific tasks
- ✅ All user questions answered and incorporated
- ✅ All line numbers verified
- ✅ All test patterns identified
- ✅ Cache invalidation strategy finalized
- ✅ Backward compatibility tests planned
- ✅ Documentation update locations confirmed

**Total Tasks**: 31 tasks across 7 phases (Phase 0: 4 tasks, Phase 1: 3 tasks, Phase 2: 1 task, Phase 3: 2 tasks, Phase 4: 8 tasks, Phase 5: 3 tasks, Phase 6: 4 tasks, Phase 7: 4 tasks, plus 2 backward compat tests)

**Next Step**: Ready to proceed with **Step 6: Present Final Plan to User for Approval**
