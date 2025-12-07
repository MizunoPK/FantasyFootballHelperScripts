# Excel Trade Visualizer Reorganization - TODO

**Objective**: Reorganize the Excel file produced by the manual trade visualizer to make it clearer what changed between both teams' scoring before and after the trade, and why the scores changed.

**Status**: ✅ VERIFICATION COMPLETE - READY FOR IMPLEMENTATION

**Next Step**: Create code changes documentation file and begin Phase 0 (Preparation & Research)

**Source File**: `updates/excel_reorganization_ideas.txt`
**Questions File**: `updates/excel_reorganization_ideas_questions.md`

## FINAL SCOPE (User Decisions)

**Implementation Scope**: HIGH PRIORITY ONLY (Ideas 1, 2, 4)

**Ideas to Implement**:
1. **IDEA 1**: Add "Trade Impact Analysis" sheet - shows traded/received/changed players
2. **IDEA 4**: Add "Score Change Breakdown" sheet - explains why scores changed (bye/injury focus)
3. **IDEA 2**: Reorganize Detailed Calculations with side-by-side columns - easier comparison

**Design Decisions**:
- **Key Changes Detail Level**: Detailed (show component names, counts, point values)
- **Breakdown Components**: Bye & Injury Only (most relevant to trades)
- **Empty Sheet Handling**: Create sheet with informational message if no changes
- **Logging Level**: INFO (consistent with existing code)
- **Sheet Order**: New sheets will be placed after Summary, before rosters

**Out of Scope** (MEDIUM/LOWER priority - not implementing):
- IDEA 8: Visual delta indicators (▲▼=)
- IDEA 5: Full sheet reordering
- IDEA 6: Trade summary metrics
- IDEA 3: Color coding
- IDEA 7: Split Detailed Calculations into two sheets

---

## VERIFICATION SUMMARY

### Iterations Completed: 6/6 ✅ VERIFICATION COMPLETE
- ✅ First Verification Round (3/3 iterations COMPLETE)
- ✅ User Questions Answered (11/11 questions)
- ✅ TODO Updated with User Decisions
- ✅ Second Verification Round (3/3 iterations COMPLETE)

**READY FOR IMPLEMENTATION**

### Iteration 1 Findings:
**Requirements Coverage**: ✅ All 8 ideas from specification are covered in TODO phases

**Key Code Patterns Identified**:
- ScoredPlayer structure: `player` (FantasyPlayer), `score` (float), `reason` (List[str])
- TradeSnapshot structure: `my_new_team`, `their_new_team`, `my_original_players`, `my_new_players`, `their_new_players`
- TradeSimTeam structure: `scored_players` (Dict[int, ScoredPlayer]), `team_score` (float)
- Excel sheet creation pattern: Build list of dicts → pd.DataFrame → df.to_excel() → _apply_sheet_formatting()
- Score change detection: Already implemented in line 621-635 using threshold 0.01

**Existing Utilities to Reuse**:
- `_parse_scoring_reasons()` (line 702-782): Extracts component values from reason strings
- `_apply_sheet_formatting()` (line 784-820): Formats Excel sheets with bold headers, column widths
- Score change threshold: `abs(original_score - new_score) > 0.01`

**Test Patterns Identified**:
- Use pytest with Mock/MagicMock for TradeSnapshot, TradeSimTeam, ScoredPlayer
- Test file: `tests/league_helper/trade_simulator_mode/test_trade_file_writer.py`
- Pattern: Create fixtures for writer, mock_trade, call method, assert sheet exists and data correct

**Integration Points**:
- `save_manual_trade_to_excel()` (line 128-200): Main entry point, calls all sheet creation methods
- ConfigManager.get_bye_week_penalty(): Used to calculate penalty values from overlap counts

### Iteration 2 Findings:
**Error Handling Patterns Identified**:
- Wrap Excel creation in try/except with `exc_info=True` for stack traces (line 160-200)
- Log errors with `self.logger.error()` before raising
- Gracefully handle missing data (e.g., `if not reason: continue` in parsing, line 715)
- No custom exception types needed (use base Exception)

**Logging Patterns Identified**:
- Use `self.logger.info()` for progress milestones (sheet creation, file saved)
- Use `self.logger.error()` for failures with `exc_info=True`
- Log detailed counts/stats for debugging (e.g., "Created sheet with X entries")
- Pattern: f-string formatting for log messages

**Documentation Files to Update**:
- `README.md`: If Excel output format is documented
- `ARCHITECTURE.md`: If trade simulator section mentions Excel export
- `CLAUDE.md`: Unlikely to need updates (coding standards unchanged)
- Inline docstrings: Add to all new methods following Google style

**Data Validation Needs**:
- Validate `scored_players` dict is not empty before building sheets
- Check that player IDs exist in dictionaries before accessing
- Handle edge case: no players with score changes (empty Score Change Breakdown)
- Validate DataFrame not empty before writing to Excel

**Performance Considerations**:
- Current filtering already reduces Detailed Calculations size (lines 621-635)
- New sheets add minimal overhead (filtered data subsets)
- pandas DataFrame operations are efficient for this data size
- No optimization needed for typical roster sizes (10-15 players per team)

### Iteration 3 Findings:
**Integration Points Identified**:
- Main caller: `TradeSimulatorModeManager.py` line ~450 (approx, manual trade mode)
- Call pattern: `self.file_writer.save_manual_trade_to_excel(snapshot, opponent.name, original_my_score, original_their_score, self.my_team, opponent)`
- Manager wraps call in try/except, catches Exception, logs error, prints user message
- Excel creation happens AFTER txt file save, so partial failure acceptable

**Mock Objects Needed for Testing**:
- Mock TradeSnapshot with: `my_new_team`, `their_new_team`, `my_original_players`, `my_new_players`, `their_new_players`
- Mock TradeSimTeam with: `team_score` (float), `name` (str), `scored_players` (Dict[int, ScoredPlayer])
- Mock ScoredPlayer with: `player` (FantasyPlayer), `score` (float), `reason` (List[str])
- Mock FantasyPlayer with: `name`, `position`, `team`, `id`, `bye_week`
- Mock pandas ExcelWriter (already done in existing tests with `@patch`)
- Mock logger: `@patch('league_helper.trade_simulator_mode.trade_file_writer.get_logger')`

**Circular Dependency Analysis**:
- ✅ No circular dependency risk
- trade_file_writer.py only imports data structures (TradeSnapshot, TradeSimTeam, LoggingManager)
- Does NOT import TradeSimulatorModeManager or any managers
- Safe to add new methods without introducing cycles

**Rollback/Cleanup Requirements**:
- ✅ No rollback needed (Excel created after txt file, independent)
- Manager already handles exceptions gracefully
- If Excel creation fails midway, partial file may exist but will be overwritten on retry (timestamp in filename ensures uniqueness)
- No database transactions or state changes to rollback

**File Path Handling**:
- Current pattern: `"./league_helper/trade_simulator_mode/trade_outputs/..."`
- Relative paths work because scripts run from repo root
- ✅ No changes needed (consistent with existing code)

**Test Coverage Requirements**:
- Must test each new sheet creation method individually
- Must test integration (all sheets created in correct order)
- Must test error handling (empty data, missing players, etc.)
- Must test with realistic mock data (multiple score changes, various statuses)
- Must verify sheet names exact match (pandas/openpyxl is case-sensitive)

### Iteration 4 Findings (Second Verification Round):
**User Answer Integration**: ✅ All answers from questions file integrated into TODO
- Scope: HIGH PRIORITY only (Ideas 1, 2, 4) - Phases 5 & 6 marked OPTIONAL
- Detail Level: "Detailed" format integrated into Phase 1
- Components: "Bye & Injury Only" integrated into Phase 2
- Empty Handling: "Create sheet with message" noted in Phase 2

**Reason String Format Research**:
- Bye format confirmed: "Bye Overlaps: X same-position, Y different-position (Z pts)"
- Injury format confirmed: "Injury: STATUS (Z pts)"
- Existing `_parse_scoring_reasons()` regex patterns extract counts but not full strings
- "Reason for Change" column should use FULL reason strings from `ScoredPlayer.reason` list
- If multiple changes (bye + injury), concatenate with "; " separator

**Implementation Clarifications Added**:
- Phase 1: Extract full reason strings, not just parsed components
- Phase 1: Compare initial vs final reason lists to identify changes
- Phase 2: Focus only on bye & injury (other components out of scope)
- Phase 4: Minimal sheet ordering (just placing new sheets), not full IDEA 5

### Iteration 5 Findings (Second Verification Round):
**Task Dependencies Verified**: ✅ Proper sequential order confirmed
- Phase 0 (research) → Phase 1 (Trade Impact) → Phase 2 (Score Breakdown) → Phase 3 (Side-by-side) → Phase 4 (Ordering) → Phase 7 (Documentation)
- Each phase has validation checkpoint before proceeding
- Phase 3 is independent and could run parallel to Phases 1-2 if desired
- Phase 4 depends on Phases 1-2 completing (need new sheets to exist before ordering)

**Edge Cases Identified and Added to TODO**:
- Empty score changes (no players affected by trade)
- Score delta exactly at threshold (0.01 boundary case)
- All players traded away (empty remaining roster)
- Multiple simultaneous changes (bye + injury both changing)
- Empty roster edge cases

**Test Coverage Enhancements**:
- Added edge case test requirements to Phase 1
- Ensured each edge case has explicit test
- Verified integration test requirements include sheet order verification

**Phase Validation Structure**: ✅ Each phase ends with mandatory validation
- Run all unit tests (`python tests/run_all_tests.py`)
- Manual testing where applicable
- Update code changes documentation file
- 100% test pass rate required before proceeding

### Iteration 6 Findings (Second Verification Round - FINAL):
**Comprehensive TODO Review**: ✅ All requirements accounted for
- Total tasks: 139 checkboxes across 7 phases
- All 3 HIGH PRIORITY ideas (1, 2, 4) fully planned
- Each idea broken into sub-phases with specific file references
- Line numbers provided for code to modify

**Documentation Requirements**: ✅ Complete
- Phase 7 includes README, CLAUDE.md, ARCHITECTURE.md updates
- Inline docstring requirements specified
- Code changes documentation tracked incrementally
- Final verification protocol included (Phase 7.5)

**Test Coverage**: ✅ Comprehensive
- Unit tests for each new method
- Integration tests for sheet order
- Edge case tests explicitly listed
- 100% pass rate required at each phase

**Risk Mitigation**: ✅ Identified and addressed
- 5 potential risks documented
- Mitigation strategies provided
- Performance concerns noted (user confirmed no concerns)

**Final Acceptance Criteria Met**:
- ✅ First verification round complete (3 iterations on draft TODO)
- ✅ Questions file created with thoughtful, research-backed questions
- ✅ User answers received for all 11 questions
- ✅ Second verification round complete (3 iterations with answers integrated)
- ✅ Total: 6 complete verification iterations performed
- ✅ Every requirement from original file covered in TODO (HIGH PRIORITY scope)
- ✅ Every question answer reflected in TODO tasks
- ✅ Specific file paths identified for each task
- ✅ Existing code patterns researched and documented
- ✅ Test requirements specified for each implementation
- ✅ Task dependencies and ordering verified
- ✅ Edge cases and error scenarios addressed
- ✅ Documentation update tasks included
- ✅ Pre-commit validation checkpoints added

### Questions Identified (to be formalized in questions file):
1. **Scope Decision**: Which priority level(s) to implement? (High/Medium/Low)
2. **Score Context Display**: Should "Key Changes" column show full details or abbreviated summary?
3. **Color Coding**: If implemented, use specific colors or default Excel palette?
4. **Performance**: Any concerns about Excel file size with additional sheets?
5. **Component Selection**: For Score Change Breakdown, show all components or only bye/injury?
6. **Error Handling**: Should we fail gracefully if no score changes detected (empty breakdown sheet)?
7. **Logging Level**: Should new sheets log at INFO or DEBUG level?

### Key Decisions Needed from User:
1. Which priority level to implement (High/Medium/Low)?
2. All 8 ideas or subset?
3. Timeline/scope preferences?

---

## SCOPE CLARIFICATION (User Input Required)

The specification file includes 8 different reorganization ideas at 3 priority levels:

### HIGH PRIORITY Ideas (biggest clarity improvements):
- **IDEA 1**: Add "Trade Impact Analysis" sheet
- **IDEA 4**: Add "Score Change Breakdown" sheet
- **IDEA 2**: Reorganize Detailed Calculations with side-by-side columns

### MEDIUM PRIORITY Ideas (nice visual enhancements):
- **IDEA 8**: Add visual delta indicators (▲▼=)
- **IDEA 5**: Reorganize sheet order
- **IDEA 6**: Add trade summary metrics to Summary sheet

### LOWER PRIORITY Ideas (polish):
- **IDEA 3**: Add color coding (requires openpyxl styling)
- **IDEA 7**: Split Detailed Calculations into two sheets

**QUESTION FOR USER**: Which ideas should be implemented in this update?

**DEFAULT ASSUMPTION** (if not specified): Implement HIGH PRIORITY ideas only (Ideas 1, 2, 4)

---

## PHASE 0: PREPARATION & RESEARCH

### 0.1: Create Code Changes Documentation File
- [ ] Create `updates/excel_reorganization_ideas_code_changes.md`
- [ ] Initialize with header and sections for tracking changes
- [ ] Update incrementally throughout implementation

### 0.2: Research Existing Code Patterns
- [ ] Study existing sheet creation methods in `trade_file_writer.py`
  - [ ] `_create_summary_sheet()` (lines 354-408)
  - [ ] `_create_initial_rosters_sheet()` (lines 410-475)
  - [ ] `_create_final_rosters_sheet()` (lines 477-588)
  - [ ] `_create_detailed_calculations_sheet()` (lines 590-700)
- [ ] Study `_parse_scoring_reasons()` method (lines 702-782)
- [ ] Study `_apply_sheet_formatting()` method (lines 784-820)
- [ ] Examine `TradeSnapshot` data structure
- [ ] Examine `TradeSimTeam.scored_players` dictionary structure
- [ ] Examine `ScoredPlayer.reason` list structure

### 0.3: Research Test Patterns
- [ ] Study `tests/league_helper/trade_simulator_mode/test_trade_file_writer.py`
- [ ] Identify test patterns for Excel sheet creation
- [ ] Identify mock data patterns for TradeSnapshot/TradeSimTeam
- [ ] Understand how to test Excel output (sheet names, data presence, etc.)

---

## PHASE 1: IMPLEMENT IDEA 1 - TRADE IMPACT ANALYSIS SHEET

**Goal**: Add new sheet showing only what changed (traded players + score-changed players)

### 1.1: Create Helper Method to Calculate Score Changes
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Add method `_calculate_score_changes()` to identify players with changed scores
  - Input: my_original_team, their_original_team, trade
  - Output: Dict mapping player_id to (initial_score, final_score, delta, reason_summary)
- [ ] Reuse existing score change detection logic from `_create_detailed_calculations_sheet` (lines 621-635)
- [ ] Extract "Key Changes" reason from score delta and `ScoredPlayer.reason` list
  - Focus on bye week penalty changes
    - Format: "Bye Overlaps: 2 same-position, 0 different-position (-10.5 pts)"
    - Extract from reason string using existing regex in `_parse_scoring_reasons()`
  - Focus on injury status changes
    - Format: "Injury: QUESTIONABLE (-10.0 pts)"
    - Extract from reason string using existing regex
  - Note roster context differences (if player scores differently on different rosters)

**Implementation Details**:
- Threshold: abs(score_delta) > 0.01
- Compare my_original_team.scored_players vs trade.my_new_team.scored_players
- Compare their_original_team.scored_players vs trade.their_new_team.scored_players

**Error Handling & Validation**:
- [ ] Validate `scored_players` dictionaries are not empty
- [ ] Check player_id exists in dict before accessing
- [ ] Handle case where no score changes detected (return empty dict)
- [ ] Handle edge case: score delta exactly 0.01 (boundary - should be included)
- [ ] Handle edge case: player both traded AND has score change on remaining roster (shouldn't happen logically)
- [ ] Handle edge case: empty roster (all players traded away)
- [ ] Add docstring with error scenarios documented

**Logging**:
- [ ] Log number of score changes found (e.g., "Found 3 players with score changes")

### 1.2: Create Trade Impact Analysis Sheet Method
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Add method `_create_trade_impact_analysis_sheet()`
  - Signature: `(writer, trade, my_original_team, their_original_team, opponent_name, original_my_score, original_their_score)`
  - Build data structure with sections for MY TEAM and THEIR TEAM
- [ ] For MY TEAM section:
  - [ ] List players I traded away (from `trade.my_original_players`)
  - [ ] List players I received (from `trade.my_new_players`)
  - [ ] List players kept but score changed (from score change detection)
  - [ ] Calculate team score changes (original → final, delta)
- [ ] For THEIR TEAM section:
  - [ ] List players they traded away (inferred from `trade.my_new_players`)
  - [ ] List players they received (from `trade.their_new_players`)
  - [ ] List players kept but score changed (from score change detection)
  - [ ] Calculate team score changes (original → final, delta)
- [ ] Build pandas DataFrame with columns:
  - Status (TRADED AWAY / RECEIVED / KEPT (CHANGED) / KEPT (UNCHANGED))
  - Player Name
  - Position
  - Initial Score (or "-" if received)
  - Final Score (or "-" if traded away)
  - Δ Score
  - Reason for Change (DETAILED format: e.g., "Bye penalty: +2 same-pos overlaps (-10.5 pts)")
    - **Implementation Note**: Extract FULL reason string from `ScoredPlayer.reason` list
    - Don't use just counts from `_parse_scoring_reasons()`, use the actual reason string
    - Compare initial vs final reason lists to find which one(s) changed
    - If multiple changes, concatenate with "; " separator
- [ ] Write to "Trade Impact Analysis" sheet
- [ ] Apply formatting with `_apply_sheet_formatting()`

**Error Handling & Validation**:
- [ ] Validate DataFrame not empty before writing to Excel
- [ ] Handle case where no changed players (write informational row)
- [ ] Wrap sheet creation in try/except with informative error message
- [ ] Add Google-style docstring with Args, Returns, Raises sections

**Logging**:
- [ ] Log start: `self.logger.info(f"Creating Trade Impact Analysis sheet")`
- [ ] Log completion: `self.logger.info(f"Created Trade Impact Analysis sheet with X rows")`
- [ ] Log breakdown: "MY TEAM: X traded, Y received, Z changed | THEIR TEAM: A traded, B received, C changed"

### 1.3: Integrate Trade Impact Analysis into Excel Export
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Update `save_manual_trade_to_excel()` method (lines 128-200)
- [ ] Add call to `_create_trade_impact_analysis_sheet()` after Summary sheet
- [ ] Pass all required parameters (trade, original teams, scores, opponent name)

### 1.4: Add Tests for Trade Impact Analysis
**File**: `tests/league_helper/trade_simulator_mode/test_trade_file_writer.py`

- [ ] Add test method `test_create_trade_impact_analysis_sheet()`
  - Create mock TradeSnapshot with traded players
  - Create mock original teams with score changes
  - Call method and verify sheet exists
  - Verify data structure (columns, rows)
  - Verify score deltas calculated correctly
- [ ] Add test for score change detection helper
- [ ] Add test for "Key Changes" reason extraction
- [ ] Add edge case tests:
  - Empty score changes dict (no changes)
  - Score delta exactly at threshold (0.01)
  - All players traded (empty remaining roster)
  - Multiple simultaneous changes (bye + injury)
- [ ] Update integration test to verify new sheet exists in Excel output

### 1.5: Validate Phase 1
- [ ] Run all unit tests: `python tests/run_all_tests.py`
- [ ] Manually test Excel output with sample trade
- [ ] Verify new sheet appears and contains expected data
- [ ] Update code changes documentation file

---

## PHASE 2: IMPLEMENT IDEA 4 - SCORE CHANGE BREAKDOWN SHEET

**Goal**: Add sheet explaining WHY each player's score changed (focus on bye/injury penalties)

### 2.1: Create Score Component Change Analyzer
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Add method `_analyze_score_component_changes()`
  - Input: initial_scored_player, final_scored_player
  - Output: Dict with before/after/delta for each component
- [ ] Parse initial and final `ScoredPlayer.reason` lists
- [ ] Extract component values using `_parse_scoring_reasons()` (lines 702-782)
- [ ] Calculate deltas for BYE & INJURY ONLY (per user decision Q3):
  - Bye week overlaps (same-position and different-position counts)
  - Bye week penalty points
  - Injury status
  - Injury penalty points
  - NOTE: Other components (ADP, matchup, performance, etc.) are OUT OF SCOPE

**Implementation Details**:
- Reuse existing regex patterns from `_parse_scoring_reasons()`
- Calculate point values from penalty counts (use ConfigManager formulas)
- Handle cases where component is present in one state but not the other

### 2.2: Create Score Change Breakdown Sheet Method
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Add method `_create_score_change_breakdown_sheet()`
  - Signature: `(writer, trade, my_original_team, their_original_team, opponent_name)`
  - Only include players whose scores changed (reuse detection logic)
- [ ] Build DataFrame with columns (BYE & INJURY ONLY per user decision Q3):
  - Player Name
  - Position
  - Team (NFL team)
  - Owner (My Team / Opponent Name)
  - Initial Bye Overlaps (e.g., "2 same-pos, 0 diff-pos")
  - Final Bye Overlaps
  - Bye Δ (points)
  - Initial Injury Status
  - Final Injury Status
  - Injury Δ (points)
  - Total Δ Score
- [ ] If no players with bye/injury changes, create sheet with message "No bye week or injury changes detected" (per user decision Q4)
- [ ] Write to "Score Change Breakdown" sheet
- [ ] Apply formatting

### 2.3: Integrate Score Change Breakdown into Excel Export
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Update `save_manual_trade_to_excel()` method
- [ ] Add call to `_create_score_change_breakdown_sheet()` after Trade Impact Analysis
- [ ] Pass required parameters

### 2.4: Add Tests for Score Change Breakdown
**File**: `tests/league_helper/trade_simulator_mode/test_trade_file_writer.py`

- [ ] Add test method `test_create_score_change_breakdown_sheet()`
  - Mock players with bye week penalty changes
  - Mock players with injury status changes
  - Verify sheet exists and data is correct
- [ ] Add test for component change analyzer
- [ ] Verify delta calculations for bye penalties
- [ ] Verify delta calculations for injury penalties
- [ ] Update integration test

### 2.5: Validate Phase 2
- [ ] Run all unit tests: `python tests/run_all_tests.py`
- [ ] Manually test Excel output with sample trade
- [ ] Verify Score Change Breakdown sheet appears with correct data
- [ ] Update code changes documentation file

---

## PHASE 3: IMPLEMENT IDEA 2 - SIDE-BY-SIDE DETAILED CALCULATIONS

**Goal**: Reorganize Detailed Calculations to show Initial/Final in same row (not separate rows)

### 3.1: Refactor Detailed Calculations Sheet Structure
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Modify `_create_detailed_calculations_sheet()` method (lines 590-700)
- [ ] Change from "two rows per player" to "one row per player"
- [ ] New column structure:
  - Player Name
  - Position
  - Team (NFL team)
  - Owner
  - Status (Traded / Received / Kept-Changed / Kept-Unchanged)
  - Initial Score
  - Final Score
  - Δ Score
  - Initial [Component] (for each scoring component)
  - Final [Component]
  - Δ [Component]

**Scoring Components to Include**:
- Base Projected Points
- Weighted Projected Points
- ADP Rating
- Player Rating
- Team Quality
- Performance (rating + percentage)
- Matchup Rating
- Schedule (rating + avg opp rank)
- Draft Bonus
- Bye Overlaps (same-pos + diff-pos counts)
- Injury Status

### 3.2: Create Component Delta Columns
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] For each scoring component, create Initial/Final/Δ columns
- [ ] Calculate deltas (handle cases where component doesn't apply)
- [ ] Format delta columns with appropriate precision
  - Scores: 2 decimal places
  - Ratings: text (EXCELLENT, GOOD, etc.)
  - Counts: integers (bye overlaps)
  - Percentages: 1 decimal place

### 3.3: Update Parsing Logic for Side-by-Side Format
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Ensure `_parse_scoring_reasons()` extracts all needed components
- [ ] Add logic to match initial and final players by player_id
- [ ] Build single row combining both initial and final data
- [ ] Handle edge cases:
  - Player traded away (no final data)
  - Player received (no initial data)
  - Player kept unchanged (initial == final)

### 3.4: Update Tests for Side-by-Side Format
**File**: `tests/league_helper/trade_simulator_mode/test_trade_file_writer.py`

- [ ] Update existing Detailed Calculations tests
  - `test_create_detailed_calculations_sheet()` (verify new structure)
  - `test_parse_scoring_reasons()` (ensure all components extracted)
- [ ] Add test for delta column calculations
- [ ] Add test for edge cases (traded/received/kept players)
- [ ] Verify column count increased (more columns due to Initial/Final/Δ triplets)

### 3.5: Validate Phase 3
- [ ] Run all unit tests: `python tests/run_all_tests.py`
- [ ] Manually test Excel output with sample trade
- [ ] Verify Detailed Calculations sheet uses new side-by-side format
- [ ] Verify easier to spot changes compared to old format
- [ ] Update code changes documentation file

---

## PHASE 4: SHEET ORDERING (Minimal - for new sheets)

**Goal**: Place new sheets in logical order (Summary → Impact → Breakdown → Final → Initial → Detailed)

**Note**: This is NOT full IDEA 5 implementation (MEDIUM priority), just deciding where to place the two new sheets created in Phases 1 & 2. Keeping it simple per user decision (HIGH PRIORITY only).

### 4.1: Update Sheet Creation Order
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Modify `save_manual_trade_to_excel()` method (lines 173-193)
- [ ] Change sheet creation order:
  1. Summary (existing)
  2. Trade Impact Analysis (new - IDEA 1)
  3. Score Change Breakdown (new - IDEA 4)
  4. Final Rosters (existing - move earlier)
  5. Initial Rosters (existing - move to end)
  6. Detailed Calculations (existing - move to end)

**Current Order** (lines 175-193):
```python
# Sheet 1: Summary
self._create_summary_sheet(...)

# Sheet 2: Initial Rosters
self._create_initial_rosters_sheet(...)

# Sheet 3: Final Rosters
self._create_final_rosters_sheet(...)

# Sheet 4: Detailed Calculations
self._create_detailed_calculations_sheet(...)
```

**New Order**:
```python
# Sheet 1: Summary
self._create_summary_sheet(...)

# Sheet 2: Trade Impact Analysis (NEW)
self._create_trade_impact_analysis_sheet(...)

# Sheet 3: Score Change Breakdown (NEW)
self._create_score_change_breakdown_sheet(...)

# Sheet 4: Final Rosters
self._create_final_rosters_sheet(...)

# Sheet 5: Initial Rosters
self._create_initial_rosters_sheet(...)

# Sheet 6: Detailed Calculations
self._create_detailed_calculations_sheet(...)
```

### 4.2: Update Tests for New Sheet Order
**File**: `tests/league_helper/trade_simulator_mode/test_trade_file_writer.py`

- [ ] Update integration test that checks sheet names/order
- [ ] Verify sheets appear in expected order when opening Excel file

### 4.3: Validate Phase 4
- [ ] Run all unit tests: `python tests/run_all_tests.py`
- [ ] Manually verify sheet order in Excel output
- [ ] Update code changes documentation file

---

## PHASE 5: MEDIUM PRIORITY ENHANCEMENTS (OPTIONAL)

**Note**: Only implement if user requests these enhancements

### 5.1: IDEA 8 - Visual Delta Indicators (▲▼=)
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Add helper method `_format_delta_with_indicator(delta_value)`
  - Returns: "▲ +X.XX" for positive, "▼ -X.XX" for negative, "= 0.00" for zero
- [ ] Apply to all Δ Score columns across sheets:
  - Trade Impact Analysis sheet
  - Score Change Breakdown sheet
  - Detailed Calculations sheet (delta columns)
- [ ] Update tests for new format
- [ ] Validate Phase 5.1

### 5.2: IDEA 6 - Trade Summary Metrics
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Modify `_create_summary_sheet()` method (lines 354-408)
- [ ] Add "TRADE METRICS" section after current content:
  - Total value traded (sum of traded player scores)
  - Net advantage calculation
  - Count of players with score changes
  - Bye week penalty changes (count of overlaps added/removed)
- [ ] Update Summary sheet tests
- [ ] Validate Phase 5.2

---

## PHASE 6: LOWER PRIORITY POLISH (OPTIONAL)

**Note**: Only implement if user explicitly requests these features

### 6.1: IDEA 3 - Color Coding
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Import openpyxl.styles (PatternFill, Font)
- [ ] Modify `_apply_sheet_formatting()` to accept optional color_map parameter
- [ ] In Final Rosters sheet, apply background colors:
  - Green fill for "Received" status
  - Red fill for "Traded Away" status (if shown in separate section)
  - Yellow fill for "Kept (Score Changed)" status
  - White fill for "Kept (Unchanged)" status
- [ ] Update tests for color coding
- [ ] Validate Phase 6.1

### 6.2: IDEA 7 - Split Detailed Calculations into Two Sheets
**File**: `league_helper/trade_simulator_mode/trade_file_writer.py`

- [ ] Create new method `_create_scoring_changes_sheet()`
  - Only include components that have Δ ≠ 0
  - Filter out unchanged components for cleaner view
- [ ] Rename existing `_create_detailed_calculations_sheet()` to `_create_complete_scoring_sheet()`
  - Keep full component listing (current behavior)
- [ ] Update `save_manual_trade_to_excel()` to create both sheets:
  - "Scoring Changes" (new filtered sheet)
  - "Complete Scoring" (existing full sheet)
- [ ] Update tests
- [ ] Validate Phase 6.2

---

## PHASE 7: DOCUMENTATION & FINAL VALIDATION

### 7.1: Update Documentation Files
- [ ] Update `README.md` if Excel output format mentioned
- [ ] Update `CLAUDE.md` if workflow descriptions need updates
- [ ] Update `ARCHITECTURE.md` if trade simulator architecture section needs updates
- [ ] Add inline documentation comments to new methods

### 7.2: Final Code Changes Documentation
- [ ] Review and finalize `updates/excel_reorganization_ideas_code_changes.md`
- [ ] Ensure all changes documented with:
  - File paths and line numbers
  - Before/after code snippets
  - Rationale for each change
  - Impact analysis
  - Test modifications

### 7.3: Final Test Suite Run
- [ ] Run complete test suite: `python tests/run_all_tests.py`
- [ ] Verify 100% test pass rate
- [ ] Fix any failing tests
- [ ] Re-run until all tests pass

### 7.4: Manual Integration Testing
- [ ] Run league helper: `python run_league_helper.py`
- [ ] Navigate to Trade Simulator mode
- [ ] Execute manual trade with real data
- [ ] Verify Excel export creates file successfully
- [ ] Open Excel file and verify:
  - All new sheets present
  - Sheets in correct order
  - Data accurate and properly formatted
  - Score deltas calculated correctly
  - Reason explanations clear and helpful

### 7.5: Requirement Verification Protocol
- [ ] Re-read original `updates/excel_reorganization_ideas.txt` file
- [ ] Create checklist of EVERY requirement (based on implemented scope)
- [ ] Verify each requirement implemented (✅ DONE or ❌ MISSING)
- [ ] Search codebase for evidence of each requirement
- [ ] Document verification in code changes file
- [ ] Ensure 100% requirement coverage

### 7.6: Move Files to Done Folder
- [ ] Move `updates/excel_reorganization_ideas.txt` to `updates/done/`
- [ ] Move `updates/excel_reorganization_ideas_code_changes.md` to `updates/done/`
- [ ] Delete `updates/excel_reorganization_ideas_questions.md` (after user answers integrated)
- [ ] Delete `updates/todo-files/excel_reorganization_ideas_todo.md` (this file)

---

## RISK ASSESSMENT

### Potential Risks:
1. **Large Excel files**: More sheets = larger file size, potential performance impact
2. **Column width issues**: Side-by-side format has many columns, may need wider display
3. **Score change detection false positives**: Threshold of 0.01 may catch floating-point rounding errors
4. **Bye week penalty calculation complexity**: Extracting deltas from reason strings may be fragile
5. **Test data complexity**: Mocking TradeSnapshots with realistic score changes is non-trivial

### Mitigation Strategies:
1. Monitor Excel file sizes during testing, optimize if needed
2. Adjust column width formatting to handle wider sheets
3. Consider slightly higher threshold (e.g., 0.05) if too many false positives
4. Add robust error handling for reason string parsing
5. Create comprehensive test fixtures with realistic trade scenarios

---

## DEPENDENCIES & PREREQUISITES

### Code Dependencies:
- `pandas` library (already installed)
- `openpyxl` library (already installed)
- Existing `TradeSnapshot` class structure
- Existing `TradeSimTeam` class structure
- Existing `ScoredPlayer` class structure
- Existing `_parse_scoring_reasons()` method

### External Dependencies:
- None (all changes internal to trade_file_writer.py and tests)

### Task Dependencies:
- Phase 1 must complete before Phase 4 (sheet order depends on new sheets existing)
- Phase 2 must complete before Phase 4 (sheet order depends on new sheets existing)
- Phase 3 is independent (can be done in parallel with Phases 1-2)
- Phase 5-6 optional enhancements depend on Phases 1-4 completing

---

## PROGRESS TRACKING INSTRUCTIONS

**IMPORTANT**: Keep this TODO file updated as work progresses. If a new Claude agent needs to continue this work in a future session, they should:

1. Re-read this TODO file to understand what's been completed
2. Check the code changes documentation file for implementation details
3. Review any open questions or blockers documented below
4. Continue from the next pending task

**Current Status**: Draft TODO created, awaiting first verification round

**Last Updated**: 2025-10-23

---

## VERIFICATION ITERATIONS LOG

### First Verification Round (STEP 2):
- **Iteration 1**: Not started
- **Iteration 2**: Not started
- **Iteration 3**: Not started

### Second Verification Round (STEP 5):
- **Iteration 4**: Not started
- **Iteration 5**: Not started
- **Iteration 6**: Not started

---

## NOTES & QUESTIONS

### Questions for User (to be formalized in questions file):
1. Which priority level of ideas to implement?
2. Any additional requirements beyond the 8 ideas listed?
3. Should color coding use specific color schemes or default Excel colors?
4. Any performance constraints on Excel file size?

### Implementation Notes:
- Current Detailed Calculations sheet uses "Timing" column (Initial/Final) - will be removed in new side-by-side format
- Score change detection already exists but needs to be extracted into reusable helper
- Reason parsing regex patterns already exist and can be reused

### Blockers:
- None identified yet (awaiting verification round and user input on scope)
