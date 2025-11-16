# Minimum Positions for Waiver Optimizer - Implementation TODO

## Objective
Add minimum position requirements for the waiver optimizer to ensure suggested trades don't make the user's team fall below minimum thresholds for each position.

## High-Level Phases

### Phase 1: Add MIN_POSITIONS Constant
- Add MIN_POSITIONS dictionary to constants file
- Use the provided default values

### Phase 2: Integrate Minimum Position Validation
- Identify where the waiver optimizer validates team composition
- Add minimum position checks to trade suggestion logic
- Ensure suggested trades don't violate minimum requirements

### Phase 3: Testing
- Add unit tests for minimum position validation
- Test edge cases (at minimum, below minimum, above minimum)
- Run full test suite to ensure no regressions

### Phase 4: Documentation
- Update README.md with minimum position information
- Update CLAUDE.md if needed
- Update code changes documentation file

### Phase 5: Pre-Commit Validation
- Run all unit tests (100% pass required)
- Manual testing of waiver optimizer
- Verify and commit changes

## Tasks

### 1. Research Codebase ✅ COMPLETED
- [x] Find constants file location: `league_helper/constants.py`
- [x] Find waiver optimizer implementation: `TradeSimulatorModeManager.start_waiver_optimizer()` (line 235)
- [x] Find where max positions are currently defined: `league_config.json` (lines 77-85), accessed via `ConfigManager.max_positions`
- [x] Find where trade suggestions are validated: `trade_analyzer.py` - `validate_roster()` and `validate_roster_lenient()` methods
- [x] Identify test files for waiver optimizer: `tests/league_helper/trade_simulator_mode/test_trade_simulator.py` (TestWaiverOptimizer class)

**Key Findings:**
- Waiver optimizer uses `TradeAnalyzer.get_trade_combinations()` to generate valid trades
- Validation happens via `validate_roster_lenient()` which checks MAX_POSITIONS using `FantasyTeam.draft_player()`
- Need to add MIN_POSITIONS check ONLY for user's team (not waiver "team")
- Validation occurs in `get_trade_combinations()` method around lines 700-730 (for waiver mode)

### 2. Add MIN_POSITIONS Constant
- [ ] Add MIN_POSITIONS dict to `league_helper/constants.py` with default values:
  ```python
  MIN_POSITIONS = {
      QB: 1,
      RB: 3,
      WR: 3,
      TE: 1,
      K: 1,
      DST: 1
  }
  # Note: No FLEX entry per user answer Q1
  ```
- [ ] Add to WAIVER OPTIMIZER CONSTANTS section (around line 38)
- [ ] Add docstring comment explaining:
  - Purpose: Minimum position requirements for trade validation
  - Scope: Applies to Waiver Optimizer and Trade Suggestor modes
  - Note: Counts total players by position (including FLEX assignments)

### 3. Implement Minimum Position Validation
- [ ] Add `count_min_position_violations()` method to `TradeAnalyzer` class
  - Method signature: `count_min_position_violations(self, roster: List[FantasyPlayer]) -> int`
  - Count positions using existing `count_positions()` method (includes FLEX assignments)
  - For each position in MIN_POSITIONS, check if count < minimum
  - Return total number of violations (0 = no violations)
  - Log violations at DEBUG level: "Min position violations: {violations} ({details})"

- [ ] Add `validate_min_positions_lenient()` method to `TradeAnalyzer` class
  - Method signature: `validate_min_positions_lenient(self, original_roster: List[FantasyPlayer], new_roster: List[FantasyPlayer]) -> bool`
  - Similar to `validate_roster_lenient()` pattern (line 173-210)
  - Count violations before and after trade
  - Return True if violations_after <= violations_before
  - Return False if trade worsens minimum violations
  - Log at DEBUG level when rejecting

- [ ] Add config validation in `TradeAnalyzer.__init__()` method
  - After existing initialization (line 54)
  - Check if MIN_POSITIONS[pos] <= config.max_positions[pos] for all positions
  - Log warning if MIN > MAX: "Configuration warning: MIN_POSITIONS[{pos}]={min_val} exceeds MAX_POSITIONS[{pos}]={max_val}"

- [ ] Integrate minimum check into `get_trade_combinations()` method
  - Add check for both Waiver Optimizer AND Trade Suggestor modes
  - Check condition: `if is_waivers OR not ignore_max_positions:`
  - Add after existing roster validation (around line 717-720)
  - Call `validate_min_positions_lenient(my_original_full_roster, my_full_roster)`
  - Use `continue` to skip trade if validation fails
  - Only validate user's team (my_full_roster), NOT opponent/waiver team
  - Apply to all trade types (1-for-1, 2-for-2, 3-for-3, unequal trades)

### 4. Create/Update Unit Tests
- [ ] Add test class `TestMinPositionsConstant` to `tests/league_helper/test_constants.py`
  - Similar to existing `TestWaiverOptimizerConstants` class (line 63)
  - Test MIN_POSITIONS dict exists and has correct structure
  - Test each position has a positive integer minimum
  - Test all positions from Constants.ALL_POSITIONS are covered (except FLEX)
  - Test FLEX is NOT in MIN_POSITIONS

- [ ] Add test class `TestCountMinPositionViolations` to `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py`
  - Test roster that meets all minimums returns 0 violations
  - Test roster below minimum for one position returns 1 violation
  - Test roster below minimum for multiple positions returns correct count
  - Test roster at exactly minimum returns 0 violations
  - Test empty roster returns 6 violations (all positions)
  - Test FLEX-assigned players are counted toward their natural position

- [ ] Add test class `TestValidateMinPositionsLenient` to `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py`
  - Test trade that maintains minimums returns True
  - Test trade that worsens violations returns False
  - Test trade that keeps same violations returns True (lenient)
  - Test trade that improves violations returns True
  - Mock scenario: Original has 2 RBs (1 violation), new has 1 RB (2 violations) → False
  - Mock scenario: Original has 2 RBs (1 violation), new has 2 RBs (1 violation) → True
  - Mock scenario: Original has 3 RBs (0 violations), new has 2 RBs (1 violation) → False

- [ ] Add waiver optimizer integration tests to `tests/league_helper/trade_simulator_mode/test_trade_simulator.py`
  - Test waiver optimizer respects minimum positions with lenient validation
  - Test no trades suggested if all would worsen minimum violations
  - Mock scenario: User has 1 QB (at MIN), waiver trade drops QB for WR → Rejected
  - Mock scenario: User has 3 RBs (at MIN), waiver trade drops RB for WR → Rejected
  - Mock scenario: User has 4 RBs (above MIN), waiver trade drops RB for WR → Allowed

- [ ] Add trade suggestor tests (verify MIN validation applies to trade suggestor mode too)
  - Test trade suggestor also respects MIN_POSITIONS
  - Test with `is_waivers=False` and `ignore_max_positions=False`

### 5. Run Full Test Suite
- [ ] Run `python tests/run_all_tests.py`
- [ ] Fix any failing tests
- [ ] Achieve 100% pass rate

### 6. Update Documentation
- [ ] Update README.md with minimum position requirements
- [ ] Update relevant module documentation
- [ ] Create/update code changes documentation

### 7. Final Validation and Commit
- [ ] Re-run all tests
- [ ] Manual testing of waiver optimizer
- [ ] Git status and diff review
- [ ] Commit with appropriate message
- [ ] Move objective files to updates/done/

## Notes
- Keep this TODO file updated with progress for potential multi-session work
- Each phase should leave the repo in a testable, functional state
- Run pre-commit validation after each phase completion
- No shortcuts - verify all requirements are met before marking complete

## Verification Summary

### Iteration 1 (COMPLETED):
- ✅ Re-read all source documents (min_position.txt, draft TODO)
- ✅ Cross-referenced requirements - all requirements covered:
  1. Add MIN_POSITIONS dict to constants file ✓
  2. Only relevant for waiver optimizer ✓
  3. Ensure trades don't violate minimums ✓
  4. Use provided default values ✓
- ✅ Researched codebase:
  - Found constants file: `league_helper/constants.py`
  - Found waiver optimizer: `TradeSimulatorModeManager.start_waiver_optimizer()` line 235
  - Found validation logic: `trade_analyzer.py` methods
  - Found test patterns: `test_constants.py`, `test_trade_analyzer.py`, `test_trade_simulator.py`
- ✅ Identified integration points:
  - Constants access pattern: `Constants.MIN_POSITIONS`
  - Validation happens at line 717-719 in `get_trade_combinations()`
  - Only validate user's team (`my_full_roster`), not waiver team
- ✅ Updated TODO with specific file paths and line numbers

**Questions identified for user:**
1. Should FLEX be included in MIN_POSITIONS? (not in spec, but MAX_POSITIONS has it)
2. What is the minimum for RB and WR given FLEX eligibility?
3. Should minimum check apply to trade suggestor mode too, or ONLY waiver optimizer?

- Status: Iteration 1 complete - proceeding to Iteration 2
- Iterations completed: 1 / 6 total required

### Iteration 2 (COMPLETED):
- ✅ Re-read updated TODO file
- ✅ Asked additional technical questions:
  1. Should MIN_POSITIONS be in league_config.json or constants.py?
     - Answer: Keep in constants.py per spec (less frequently changed than MAX_POSITIONS)
  2. What validation should MIN_POSITIONS have?
     - Check MIN_POSITIONS[pos] <= MAX_POSITIONS[pos] for all positions
     - Add warning if conflict detected
  3. How should validation interact with FLEX positions?
     - MIN_POSITIONS doesn't include FLEX (per spec)
     - Validation should count natural position slots only
  4. Should we track rejection statistics?
     - Yes, log summary at DEBUG level
- ✅ Researched additional code patterns:
  - Logging pattern: `self.logger.debug(f"Descriptive message: {details}")` (line 169 in trade_analyzer.py)
  - Logging pattern: `self.logger.info(f"Summary stats: count={len(items)}")` (line 430)
  - ConfigManager pattern: Access via `self.config.max_positions` (throughout codebase)
  - Constants pattern: Import and access via `Constants.MIN_WAIVER_IMPROVEMENT` (line 744)
  - Error handling: Use try/except with logger.debug for non-critical validation failures
- ✅ Updated TODO with error handling and validation details:

**Additional Implementation Details:**
- Add validation in `validate_min_positions()` to check MIN vs MAX position compatibility
- Log warning if MIN_POSITIONS[pos] > MAX_POSITIONS[pos] for any position
- Consider edge case: What if user's current roster already violates minimums before trade?
  - Answer: Still reject trades that make it worse (similar to MAX_POSITIONS lenient validation)
- Add counter for rejected trades and log summary: "Rejected {count} trades due to minimum position violations"

- Status: Iteration 2 complete - proceeding to Iteration 3
- Iterations completed: 2 / 6 total required

### Iteration 3 (COMPLETED - First Verification Round):
- ✅ Re-read all documents (min_position.txt, updated TODO)
- ✅ Asked final technical questions:
  1. Where exactly should MIN check be added in `get_trade_combinations()`?
     - After `validate_trade_roster()` check (line 717)
     - Before creating TradeSimTeam objects (line 737)
     - Only when `is_waivers=True`
  2. What happens if operations fail midway?
     - Validation failures use `continue` to skip trade (non-blocking)
     - No rollback needed (trade combinations are generated, not executed)
  3. Should MIN check use lenient validation like MAX?
     - No - MIN should be strict (always reject if below minimum)
     - MAX uses lenient to allow fixing existing violations
     - MIN is a safety threshold (user must always maintain minimums)
  4. What test mocking strategy should be used?
     - Mock FantasyTeam.draft_player() for MAX validation
     - Use real count_positions() for MIN validation (simple dict counting)
     - Mock ConfigManager.max_positions in fixtures
- ✅ Researched integration points and dependencies:
  - `is_waivers` parameter controls mode (line 623 in trade_analyzer.py)
  - Waiver mode check: `if is_waivers:` (lines 725, 743, etc.)
  - Add MIN check at same location as MAX check but only when is_waivers=True
  - No circular dependencies - MIN check is independent validation
  - Test fixtures use `mock_config.max_positions` pattern (line 33 in test_trade_analyzer.py)
- ✅ Final TODO refinements:
  - Added exact line numbers for integration
  - Specified strict vs lenient validation approach
  - Clarified test mocking strategy
  - Confirmed no backward compatibility concerns (new feature)

**Integration Points Summary:**
1. `league_helper/constants.py` line 38: Add MIN_POSITIONS constant
2. `league_helper/trade_simulator_mode/trade_analyzer.py` line 77: Add validate_min_positions() method
3. `league_helper/trade_simulator_mode/trade_analyzer.py` line 719: Integrate MIN check in get_trade_combinations()
4. `tests/league_helper/test_constants.py` line 76: Add TestMinPositionsConstant class
5. `tests/league_helper/trade_simulator_mode/test_trade_analyzer.py` line ~230: Add MIN validation tests

**Risk Areas:**
- FLEX position interaction (MIN doesn't include FLEX, but RB/WR are FLEX-eligible)
- Need to clarify if MIN counts natural position only or includes FLEX assignments
- Edge case: User starts with 2 QB but MIN is 1, drops 1 QB for WR - should work
- Edge case: User has 1 QB (at MIN), tries to drop for non-QB - should reject

- Status: First verification round complete (3 iterations)
- Iterations completed: 3 / 6 total required
- Next step: Create questions file for user clarification

---

## USER ANSWERS RECEIVED - Updating Implementation Plan

**Q1: FLEX Position Handling** → Answer: **A** - No FLEX in MIN_POSITIONS
**Q2: Position Counting Strategy** → Answer: **B** - Total position count (natural + FLEX)
**Q3: Scope of Minimum Validation** → Answer: **B** - Waiver Optimizer + Trade Suggestor
**Q4: Validation Strictness** → Answer: **B** - Lenient validation
**Q5: Error Messaging** → Answer: **A** - Silent filtering (DEBUG logging only)
**Q6: Configuration Validation** → Answer: **B** - Validation with warning

### Implementation Adjustments Based on Answers:

1. **MIN_POSITIONS constant**: No FLEX entry (keep as specified)
2. **Position counting**: Use `count_positions()` method (counts by player.position, includes FLEX assignments)
3. **Validation scope**: Apply MIN check when `is_waivers=True OR (not ignore_max_positions AND not is_waivers)`
   - This covers Waiver Optimizer and Trade Suggestor modes
4. **Validation approach**: Implement lenient validation similar to `validate_roster_lenient()`
   - Create `validate_min_positions_lenient()` method
   - Allow trades that don't worsen minimum violations
   - Count violations before and after trade
5. **User feedback**: Silent filtering with DEBUG logging only
   - No user-facing messages about MIN rejections
   - Log at DEBUG level for debugging
6. **Config validation**: Add warning check at TradeAnalyzer initialization
   - Compare MIN_POSITIONS vs config.max_positions
   - Log warning if MIN > MAX for any position

- Status: Answers integrated - proceeding to second verification round
- Iterations completed: 3 / 6 total required

### Iteration 4 (COMPLETED - Second Verification Round):
- ✅ Re-read all source documents with user answers
- ✅ Cross-referenced all requirements against updated TODO:
  1. ✅ Add MIN_POSITIONS constant (no FLEX) - Task 2
  2. ✅ Apply to waiver optimizer AND trade suggestor - Task 3
  3. ✅ Lenient validation (don't worsen violations) - Task 3
  4. ✅ Count total positions (including FLEX) - Task 3
  5. ✅ Silent filtering (DEBUG logging only) - Task 3
  6. ✅ Config validation (MIN <= MAX check) - Task 3
  7. ✅ Put in constants file - Task 2
  8. ✅ Use provided default values - Task 2
- ✅ Validated implementation pattern against existing `validate_roster_lenient()`:
  - Line 173-210 in trade_analyzer.py shows exact pattern to follow
  - Count violations before and after trade
  - Return `violations_after <= violations_before`
  - Log at DEBUG level (line 204, 209)
- ✅ All user answers successfully integrated into plan
- ✅ No conflicts or missing requirements identified

**Pattern to follow for `validate_min_positions_lenient()`:**
```python
def validate_min_positions_lenient(self, original_roster, new_roster) -> bool:
    violations_before = self.count_min_position_violations(original_roster)
    violations_after = self.count_min_position_violations(new_roster)
    self.logger.debug(f"Min violations before: {violations_before}, after: {violations_after}")
    result = violations_after <= violations_before
    self.logger.debug(f"Min validation result: {result}")
    return result
```

- Status: Iteration 4 complete - proceeding to Iteration 5
- Iterations completed: 4 / 6 total required

### Iteration 5 (COMPLETED - Second Verification Round):
- ✅ Deep dive into integration points
- ✅ Researched exact location for MIN validation in `get_trade_combinations()`:
  - Line 693-700: `validate_trade_roster()` helper function defined
  - Line 717: MAX validation happens here with `validate_trade_roster()`
  - **INTEGRATION POINT**: Add MIN validation immediately after line 719
  - Applies when `not ignore_max_positions` (covers both waiver + trade suggestor per Q3-B)
- ✅ Researched all call sites of `validate_trade_roster()`:
  - 1-for-1 trades: Line 717 (my team), Line 726 (their team)
  - 2-for-2 trades: Line 788 (my team), Line 794 (their team)
  - 3-for-3 trades: Line 844 (my team), plus others
  - Unequal trades: Multiple locations throughout method
  - **Need to add MIN check at ALL these locations** (only for my_team, not their_team)
- ✅ Identified all trade type blocks that need MIN validation:
  1. 1-for-1 trades (line 704-755)
  2. 2-for-2 trades (line 757-818)
  3. 3-for-3 trades (line 820-871)
  4. 2-for-1 trades (unequal)
  5. 1-for-2 trades (unequal)
  6. 3-for-1 trades (unequal)
  7. 1-for-3 trades (unequal)
  8. 3-for-2 trades (unequal)
  9. 2-for-3 trades (unequal)
- ✅ Integration strategy clarified:
  - Add MIN check right after MAX check (line 719)
  - Use same pattern: `if not ignore_max_positions:` to control when it applies
  - Only validate my_team (not their_team or waiver team)
  - Use `continue` to skip trade if MIN validation fails
  - Replicate this pattern in ALL trade type blocks

**Exact integration code pattern:**
```python
# Line 717-719 (existing MAX validation)
if not validate_trade_roster(my_original_full_roster, my_full_roster):
    continue

# ADD HERE (new MIN validation) - Line 720
if not ignore_max_positions:
    if not self.validate_min_positions_lenient(my_original_full_roster, my_full_roster):
        self.logger.debug("Trade rejected: would worsen minimum position violations")
        continue
```

- Status: Iteration 5 complete - proceeding to Iteration 6
- Iterations completed: 5 / 6 total required

### Iteration 6 (COMPLETED - Second Verification Round COMPLETE):
- ✅ Re-read all final TODO tasks
- ✅ Final technical validation questions:
  1. Where to add config validation in __init__? → After line 54 (after logger initialization)
  2. How to model count_min_position_violations? → Similar to count_position_violations (line 117)
  3. Are there any circular imports to worry about? → No, Constants already imported at line 17
  4. What if MIN_POSITIONS dict is modified incorrectly? → Config validation will warn
  5. Performance impact of additional validation? → Minimal (simple dict counting, same as MAX)
- ✅ Final integration checklist:
  - ✅ Task 2: Add MIN_POSITIONS to constants.py (3 subtasks)
  - ✅ Task 3: Implement 3 methods + config validation + integration (5 major subtasks)
  - ✅ Task 4: Add 4 test classes (12+ test cases total)
  - ✅ Task 5: Run full test suite
  - ✅ Task 6: Update documentation
  - ✅ Task 7: Final validation and commit
- ✅ Verified no missing edge cases:
  - Empty roster: Will show 6 violations (all positions below minimum) ✓
  - FLEX assignments: Counted via count_positions() which uses player.position ✓
  - Locked/IR players: Included in validation rosters (my_full_roster) ✓
  - Multiple violation positions: count_min_position_violations() sums all ✓
- ✅ Confirmed all dependencies in place:
  - Constants module: Already imported in trade_analyzer.py ✓
  - count_positions() method: Already exists (line 56) ✓
  - validate_roster_lenient() pattern: Well-established (line 173) ✓
  - Logger: Already available (self.logger) ✓
  - ConfigManager: Already available (self.config) ✓

**Final Implementation Checklist:**
- [ ] 1 constant added (MIN_POSITIONS)
- [ ] 2 new methods added (count_min_position_violations, validate_min_positions_lenient)
- [ ] 1 __init__ modification (config validation)
- [ ] 9 integration points (one per trade type in get_trade_combinations)
- [ ] 4 test classes added (~15-20 individual tests)
- [ ] 2 documentation files updated (README.md, code changes doc)

**Risk Mitigation:**
- Config validation prevents nonsensical MIN > MAX
- Lenient validation prevents breaking existing workflows
- DEBUG-only logging prevents user confusion
- Comprehensive tests ensure correctness
- Follows established patterns (low implementation risk)

**Ready for Implementation:** ✅ ALL 6 VERIFICATION ITERATIONS COMPLETE
- Status: Second verification round complete (6 iterations total)
- Iterations completed: 6 / 6 total required
- Next step: Begin implementation
