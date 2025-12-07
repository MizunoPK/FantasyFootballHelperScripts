# Bye Scaling Penalties - TODO File

## Objective
Replace BASE_BYE_PENALTY and DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY with new parameters (SAME_POS_BYE_WEIGHT and DIFF_POS_BYE_WEIGHT) and implement new bye week penalty calculation algorithm.

## Draft TODO Tasks (Updated - Iteration 1)

### Phase 1: Configuration Changes
- [ ] **Task 1.1**: Update league_config.json (data/league_config.json)
  - Current values: BASE_BYE_PENALTY=41.34, DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY=1.95 (lines 9-10)
  - Replace with:
    - "SAME_POS_BYE_WEIGHT": 1.0
    - "DIFF_POS_BYE_WEIGHT": 1.0
  - Remove old parameters completely

- [ ] **Task 1.2**: Update ConfigManager.py (league_helper/util/ConfigManager.py)
  - Line 55: Update ConfigKeys.BASE_BYE_PENALTY → add SAME_POS_BYE_WEIGHT, DIFF_POS_BYE_WEIGHT
  - Line 173: Update attribute `self.base_bye_penalty` → add new attributes
  - Line 759: Update parameter loading in _extract_parameters()
  - Lines 378-446: Completely rewrite get_bye_week_penalty() method with new algorithm

### Phase 2: Bye Week Penalty Calculation Implementation
- [ ] **Task 2.1**: Implement new algorithm in ConfigManager.get_bye_week_penalty()
  - **Current implementation** (lines 378-446 in ConfigManager.py):
    - Signature: `get_bye_week_penalty(num_same_position: int, num_different_position: int) -> float`
    - Calculates: `(base_bye * scale * num_same) + (diff_penalty * scale * num_diff)`
    - Uses bye week scaling based on weeks remaining (REMOVE THIS)

  - **New implementation** (COMPLETE REWRITE):
    - **New signature**: `get_bye_week_penalty(same_pos_players: List[FantasyPlayer], diff_pos_players: List[FantasyPlayer]) -> float`
    - **Import needed**: `from typing import List` and `import statistics`
    - **Need access to**: `from utils.FantasyPlayer import FantasyPlayer` (verify no circular dependency)

    - **Algorithm steps**:
      1. Calculate median for same-position players:
         - For each player in same_pos_players:
           - Collect week_1_points through week_17_points
           - Filter: skip if None or == 0.0
           - If no valid weeks: log warning, use 0.0 as median
           - Calculate: `statistics.median(valid_weeks)`
         - Sum all medians → same_pos_median_total

      2. Calculate median for diff-position players (same logic):
         - Sum all medians → diff_pos_median_total

      3. Apply exponential scaling:
         - `same_penalty = same_pos_median_total ** self.same_pos_bye_weight`
         - `diff_penalty = diff_pos_median_total ** self.diff_pos_bye_weight`

      4. Return: `same_penalty + diff_penalty`

    - **DO NOT apply bye week scaling factor** (removed per user Q3)
    - **Error handling**: Try-except around median calculation, log errors, return 0.0 on failure
    - **Logging**: Debug log showing calculations for transparency

- [ ] **Task 2.2**: Update player_scoring.py _apply_bye_week_penalty()
  - **Current implementation** (lines 620-680):
    - Already iterates through roster collecting same-pos and diff-pos players
    - Currently counts: `num_same_position += 1` and `num_different_position += 1`
    - Calls: `penalty = self.config.get_bye_week_penalty(num_same_position, num_different_position)`

  - **New implementation**:
    - **Keep existing early returns** (lines 643-647):
      - Return if bye_week is None
      - Return if bye_week < current_nfl_week (**CRITICAL - preserve this check**)

    - **Change loop** (lines 650-666):
      - Instead of counting, collect player objects into lists:
        - `same_pos_players = []` (same position + same bye week)
        - `diff_pos_players = []` (different position + same bye week)
      - Append players instead of incrementing counts

    - **Update penalty call** (line 671):
      - Old: `penalty = self.config.get_bye_week_penalty(num_same_position, num_different_position)`
      - New: `penalty = self.config.get_bye_week_penalty(same_pos_players, diff_pos_players)`

    - **Update reason string** (line 677):
      - Still show counts: `len(same_pos_players)` and `len(diff_pos_players)`
      - Format: "Bye Overlaps: {same_count} same-position, {diff_count} different-position ({-penalty:.1f} pts)"

### Phase 3: Simulation System Updates
- [ ] **Task 3.1**: Update ConfigGenerator.py (simulation/ConfigGenerator.py)
  - **Lines 54-72: PARAM_DEFINITIONS** - Replace both old params with new ones
    - Remove: 'BASE_BYE_PENALTY': (10.0, 0.0, 200.0)
    - Remove: 'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY': (10.0, 0.0, 200.0)
    - Add: 'SAME_POS_BYE_WEIGHT': (0.2, 0.0, 3.0)  # ±0.2 from optimal, bounded [0, 3]
    - Add: 'DIFF_POS_BYE_WEIGHT': (0.2, 0.0, 3.0)  # ±0.2 from optimal, bounded [0, 3]

  - **Lines 112-132: PARAMETER_ORDER** - Update parameter names
    - Line 115: Replace 'BASE_BYE_PENALTY' with 'SAME_POS_BYE_WEIGHT'
    - Line 116: Replace 'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY' with 'DIFF_POS_BYE_WEIGHT'

  - **Lines 263-275: generate_all_parameter_value_sets()** - Update parameter generation
    - Replace BASE_BYE_PENALTY generation with SAME_POS_BYE_WEIGHT
    - Replace DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY with DIFF_POS_BYE_WEIGHT

  - **Lines 512-517: generate_single_parameter_configs()** - Update single parameter handling
    - Add cases for SAME_POS_BYE_WEIGHT and DIFF_POS_BYE_WEIGHT
    - Remove cases for old parameters

  - **Lines 583-584: _extract_combination_from_config()** - Update extraction
    - Extract new parameters instead of old ones

  - **Lines 631-632: create_config_dict()** - Update config creation
    - Set new parameters instead of old ones

### Phase 4: Testing
- [ ] **Task 4.1**: Update ConfigManager tests (tests/league_helper/util/test_ConfigManager_thresholds.py)
  - test_get_bye_week_penalty_same_position_only (line 721)
  - test_get_bye_week_penalty_different_position (line 731)
  - Update test config fixtures to use new parameters
  - Update test assertions to match new algorithm
  - Add tests for median calculation edge cases:
    - Players with missing weekly data (None values)
    - Players with zero points in some weeks
    - Empty same-pos or diff-pos lists

- [ ] **Task 4.2**: Update player_scoring tests (tests/league_helper/util/test_player_scoring.py)
  - test_score_player_with_bye_penalty (line 578)
  - Update mock config (lines 50-51) with new parameters
  - Update test expectations for new penalty calculation

- [ ] **Task 4.3**: Update PlayerManager scoring tests (tests/league_helper/util/test_PlayerManager_scoring.py)
  - test_bye_penalty_no_matches (line 792)
  - test_bye_penalty_one_same_position_match (line 801)
  - test_bye_penalty_one_different_position_match (line 813)
  - test_bye_penalty_mixed_overlaps (line 825)
  - test_bye_penalty_excludes_player_being_scored (line 842)
  - test_massive_bye_week_penalty (line 1350)
  - All tests need new penalty calculation logic

- [ ] **Task 4.4**: Update simulation tests (tests/simulation/test_config_generator.py)
  - Update tests that reference BASE_BYE_PENALTY or DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY
  - Verify parameter generation works with new weight parameters

- [ ] **Task 4.5**: Run full test suite (MANDATORY before commit)
  - Execute `python tests/run_all_tests.py`
  - Ensure 100% pass rate (all 1,811 tests)

### Phase 5: Documentation
- [ ] **Task 5.1**: Update README.md
  - Document new configuration parameters
  - Explain new penalty calculation logic

- [ ] **Task 5.2**: Update CLAUDE.md if needed
  - Add any new architectural patterns

- [ ] **Task 5.3**: Update rules.md if needed
  - Document any new development patterns

### Phase 6: Validation and Completion
- [ ] **Task 6.1**: Manual testing
  - Test league helper with new parameters
  - Verify penalty calculations are reasonable

- [ ] **Task 6.2**: Create code changes documentation
  - Document all file modifications
  - Include before/after snippets

- [ ] **Task 6.3**: Final verification
  - Re-read original spec
  - Verify all requirements met

- [ ] **Task 6.4**: Move files to done folder
  - Move `bye_scaling_penalties.md` to `updates/done/`
  - Delete questions file (if created)

## User Answers Received ✅

1. **Default values**: SAME_POS_BYE_WEIGHT=1.0, DIFF_POS_BYE_WEIGHT=1.0
2. **Simulation ranges**: (0.2, 0.0, 3.0) for both parameters
3. **Bye week scaling**: REMOVE - Do not apply bye week scaling factor
4. **Data source**: Use ALL weeks (1-17) for median calculation
5. **Missing/zero data**: Skip both None and zero values (existing pattern)
6. **Edge cases**: Log warning and return 0.0 for players with no valid data
7. **Method signature**: Pass pre-filtered lists: `get_bye_week_penalty(same_pos_players: List[FantasyPlayer], diff_pos_players: List[FantasyPlayer]) -> float`
8. **CRITICAL**: Still check if bye week has passed - no penalty if `player.bye_week < current_nfl_week`

## Notes
- This is a DRAFT TODO - will be refined through 3 verification iterations (per round)
- Keep this file updated with progress for continuity across sessions
- Each phase should leave repo in testable, functional state
- Run pre-commit validation (all unit tests) after each phase completion

## Verification Summary - Round 1 (First 3 Iterations)

### Iteration 1 Complete ✓
- **Requirements verified**: All requirements from spec file identified
- **Files identified**:
  - Core: ConfigManager.py, player_scoring.py, league_config.json
  - Simulation: ConfigGenerator.py
  - Tests: test_ConfigManager_thresholds.py, test_player_scoring.py, test_PlayerManager_scoring.py, test_config_generator.py
- **Key patterns identified**:
  - FantasyPlayer has week_N_points attributes (week_1_points through week_17_points) - **CORRECTED: 17 weeks, not 18**
  - ConfigManager handles all config parameter access
  - Penalties are calculated in ConfigManager, applied in player_scoring
  - Simulation uses PARAM_DEFINITIONS and PARAMETER_ORDER for optimization
- **Questions raised**: 5 questions identified (see Questions section above)
- **Next**: Iteration 2 - Deep dive verification

### Iteration 2 Complete ✓
- **Error handling patterns identified**:
  - Use ValueError for invalid parameters/configuration
  - Always log errors with `self.logger.error()` before raising
  - Use safe_float_conversion() for potentially None/NaN values

- **Logging patterns identified**:
  - `self.logger.debug()` for detailed diagnostic info (most common)
  - `self.logger.warning()` for non-fatal issues
  - `self.logger.error()` for errors before raising exceptions

- **Data validation patterns**:
  - Use `safe_float_conversion(value, default)` from utils.FantasyPlayer
  - Handle None values explicitly before calculations
  - Filter out None/zero values when collecting data for statistics
  - Pattern from calculate_consistency (lines 162-204 in player_scoring.py):
    ```python
    weekly_points = []
    for week in range(1, current_nfl_week):
        points = getattr(player, f'week_{week}_points')
        if points is not None and float(points) > 0:
            weekly_points.append(float(points))
    ```

- **Weekly projection data structure**:
  - FantasyPlayer.week_1_points through week_17_points (17 weeks total)
  - All are Optional[float], can be None
  - Access via: `getattr(player, f'week_{week}_points')` or `player.get_single_weekly_projection(week)`
  - Must filter None values before statistical calculations

- **Statistical calculation patterns**:
  - Import statistics module: `import statistics`
  - Use `statistics.mean()`, `statistics.stdev()` (existing pattern)
  - Need to add `statistics.median()` (not currently used in codebase)
  - Handle empty lists and single-value lists specially

- **Additional questions identified**:
  - Should median calculation include weeks with 0 points or skip them? (Current pattern: skip zeros)
  - What should median be if a player has no valid weekly data? (Return 0.0?)

- **Next**: Iteration 3 - Final verification

### Iteration 3 Complete ✓
- **Integration points verified**:
  - `get_bye_week_penalty()` is called from: `player_scoring.py:671`
  - `_apply_bye_week_penalty()` is called from: `player_scoring.py:446 (within score_player)`
  - **Only 1 call site for each** = minimal integration risk

- **Circular dependency check**: ✅ No circular dependencies detected
  - ConfigManager → (no imports of player_scoring or FantasyPlayer for penalty calc)
  - player_scoring → ConfigManager (already exists)
  - FantasyPlayer → (no imports needed)

- **Mock patterns for testing**:
  - Tests mock `ConfigManager` with test configurations
  - Tests call `_apply_bye_week_penalty()` directly with mock rosters
  - Pattern: Create FantasyPlayer objects with test bye_weeks and weekly points
  - Mock config needs SAME_POS_BYE_WEIGHT and DIFF_POS_BYE_WEIGHT values

- **Error recovery considerations**:
  - What if player has no bye_week? (Already handled: check if None line 643)
  - What if roster is empty? (Should return 0 penalty)
  - What if all players have None weekly data? (Return 0 penalty for that player)
  - What if median calculation fails? (Use try-except, return 0.0 for that player)

- **File path verification**: ✅ All paths are correct
  - ConfigManager loaded from data_folder / 'league_config.json'
  - No new files created, only modifications

- **Task ordering finalized**:
  1. Phase 1: Update configuration (config.json, ConfigManager) - ATOMIC
  2. Phase 2: Update penalty calculation (ConfigManager.get_bye_week_penalty) - ATOMIC
  3. Phase 3: Update simulation (ConfigGenerator) - INDEPENDENT
  4. Phase 4: Update all tests - CAN BE INCREMENTAL
  5. Phase 5: Documentation - LAST
  6. Phase 6: Final validation - MANDATORY

- **Backward compatibility**: ⚠️ BREAKING CHANGE
  - Method signature changes: get_bye_week_penalty(roster_players, player) instead of (num_same, num_diff)
  - Config parameters renamed: Cannot load old config files without migration
  - Must update config, code, and tests TOGETHER in each phase

- **Next**: Create questions file for user

### Summary: First Verification Round Complete (3/3 Iterations) ✅

**Iterations completed**: 3 of 3 required for first verification round

**Requirements coverage**: 100%
- ✅ Replace BASE_BYE_PENALTY with SAME_POS_BYE_WEIGHT
- ✅ Replace DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY with DIFF_POS_BYE_WEIGHT
- ✅ Implement new bye week penalty algorithm (median-based exponential scaling)
- ✅ Update simulation system with new parameters

**Key findings**:
- 4 files to modify (ConfigManager.py, player_scoring.py, ConfigGenerator.py, league_config.json)
- 4 test files to update (test_ConfigManager_thresholds.py, test_player_scoring.py, test_PlayerManager_scoring.py, test_config_generator.py)
- Only 2 integration points (minimal risk)
- No circular dependencies
- Breaking change (requires atomic updates across config + code + tests)

**Risk areas**:
- ⚠️ Weekly data may have None values - must filter before median calculation
- ⚠️ Signature change to get_bye_week_penalty - must update caller simultaneously
- ⚠️ Breaking config change - old configs won't load without parameter names updated

**Questions for user**: 7 questions identified (see Questions section)

**Ready for**: User Q&A → Iteration Round 2 (3 more iterations after answers)

---

## Verification Summary - Round 2 (Second 3 Iterations)

### Iteration 4 Complete ✓
- **User answers integrated**: All 7 questions answered, decisions incorporated into tasks
- **Configuration values finalized**:
  - SAME_POS_BYE_WEIGHT: 1.0 (initial)
  - DIFF_POS_BYE_WEIGHT: 1.0 (initial)
  - Simulation ranges: (0.2, 0.0, 3.0) for both
- **Algorithm details specified**:
  - Use weeks 1-17 for median calculation
  - Skip None and zero values
  - Log warning if no valid data, return 0.0
  - Remove bye week scaling factor
  - Keep check for bye week already passed
- **Method signature confirmed**: `get_bye_week_penalty(same_pos_players: List[FantasyPlayer], diff_pos_players: List[FantasyPlayer]) -> float`
- **Import requirements verified**: Need to add `import statistics` and verify FantasyPlayer import
- **Next**: Iteration 5 - Validate implementation approach

### Iteration 5 Complete ✓
- **Circular dependency verified**: ✅ NO CIRCULAR DEPENDENCY
  - ConfigManager → FantasyPlayer (new import, safe)
  - FantasyPlayer → (no ConfigManager import)
  - Pattern to use: `sys.path.append(str(Path(__file__).parent.parent.parent))` then `from utils.FantasyPlayer import FantasyPlayer`
  - Matches existing pattern in player_scoring.py line 35-36

- **Import statement to add to ConfigManager.py**:
  ```python
  import statistics  # Add to line 19 (after json import)
  sys.path.append(str(Path(__file__).parent.parent.parent))  # Add after line 24
  from utils.FantasyPlayer import FantasyPlayer  # Add after sys.path.append
  ```

- **Median calculation validation**:
  - `statistics.median([])` raises `StatisticsError` - MUST handle this
  - `statistics.median([5.0])` returns `5.0` - works with single value
  - `statistics.median([5.0, 10.0])` returns `7.5` - averages two values
  - Need try-except around median call, catch `statistics.StatisticsError`

- **Error handling pattern to use**:
  ```python
  try:
      valid_weeks = [points for week in range(1, 18)
                     if (points := getattr(player, f'week_{week}_points')) is not None
                     and points > 0]
      if not valid_weeks:
          self.logger.warning(f"No valid weekly data for {player.name}, using 0.0 median")
          return 0.0
      median = statistics.median(valid_weeks)
  except statistics.StatisticsError as e:
      self.logger.error(f"Failed to calculate median for {player.name}: {e}")
      return 0.0
  ```

- **Key implementation details confirmed**:
  - Must check `if not valid_weeks:` before calling median (avoid StatisticsError)
  - Use walrus operator for cleaner filtering: `(points := getattr(...)) is not None`
  - Log at warning level for missing data, error level for calculation failures
  - Return 0.0 (no penalty contribution) for players with no valid data

- **Next**: Iteration 6 - Final verification and completion

### Iteration 6 Complete ✓
- **Original spec re-read**: All requirements verified ✅

- **Requirements coverage verification** (line-by-line from spec):
  1. ✅ "completely replacing BASE_BYE_PENALTY and DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY" → Tasks 1.1, 1.2, 3.1
  2. ✅ "Collect two lists of players" (same-pos and diff-pos) → Task 2.2
  3. ✅ "determine what the median score is from their week 1-18 scores" → Task 2.1 (using weeks 1-17)
  4. ✅ "Each player's median value will then be added up" → Task 2.1 (sum medians)
  5. ✅ "take it to the power of SAME_POS_BYE_WEIGHT" → Task 2.1 algorithm step 3
  6. ✅ "take it to the power of DIFF_POS_BYE_WEIGHT" → Task 2.1 algorithm step 3
  7. ✅ "Add the two values together, and return that total" → Task 2.1 algorithm step 4
  8. ✅ "Update the Simulation as well" → Task 3.1 complete
  9. ✅ User addition: "STILL NOT APPLY ANY BYE WEEK PENELTY IF PLAYER'S BYE WEEK HAS ALREADY PASSED" → Task 2.2 preserves check

- **Task order validated**:
  - Phase 1 (Config changes) → Phase 2 (Algorithm) → Phase 3 (Simulation) is correct
  - Each phase can be tested independently before moving to next
  - Tests updated incrementally as implementation proceeds

- **Missing items check**: ✅ Nothing missing
  - All code files identified
  - All test files identified
  - All documentation identified
  - Import statements specified
  - Error handling specified
  - Logging patterns specified
  - Edge cases handled

- **Risk mitigation verified**:
  - Circular dependency: Checked and safe ✅
  - Breaking changes: Documented, atomic update strategy ✅
  - Data validation: Empty lists, None values, zero values all handled ✅
  - Backward compatibility: Check for bye week passed preserved ✅

- **Implementation ready**: ✅ YES
  - All requirements mapped to tasks
  - All technical details specified
  - All patterns documented
  - All edge cases handled
  - User decisions integrated

### Summary: Second Verification Round Complete (6/6 Iterations Total) ✅

**Total iterations completed**: 6 (3 in round 1 + 3 in round 2)

**Final status**: ✅ TODO FILE COMPLETE AND READY FOR IMPLEMENTATION

**Coverage**:
- Requirements: 100% (9/9 requirements covered)
- Files: 100% (4 core files + 4 test files identified)
- Patterns: 100% (all coding patterns documented)
- Edge cases: 100% (all edge cases handled)
- User decisions: 100% (all 7 questions answered and integrated)

**Ready to proceed with implementation**: YES ✅
