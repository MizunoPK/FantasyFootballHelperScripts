# Save Aggregate Scoring Results - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `save_aggregate_scoring_results_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## Progress Summary

**Total Items:** (To be counted after Phase 2 investigation)
**Resolved:** 0
**Pending:** (All items - to be populated in Phase 2)

---

## General Decisions

- [x] **Architecture Approach:** Full mode manager with standard structure (Option A)
  - **Decision:** Use full mode manager pattern for consistency
  - **Rationale:** Consistent with other modes, easier for future developers, allows for future enhancements
  - **Date:** 2025-12-22
- [x] **ConfigManager Error Handling:** Trust ConfigManager initialization (Option A)
  - **Decision:** No defensive checks for None values
  - **Rationale:** Matches existing code patterns, ConfigManager is well-tested, if config is broken the whole app fails anyway
  - **Date:** 2025-12-22
- [ ] **Menu Integration Pattern:** What's the exact pattern for adding top-level menu items?
- [ ] **Error Handling Strategy:** Fail fast vs. graceful degradation for missing files/folders?

---

## Menu System Integration

- [ ] **Menu Definition Location:** Where are top-level menu options defined in LeagueHelperManager?
- [ ] **Mode Dispatch Mechanism:** How does LeagueHelperManager route to mode managers?
- [ ] **Menu Option Label:** Confirm exact text "Save Calculated Projected Points" or adjust?
- [ ] **Return Behavior:** How do modes return control to main menu?
- [ ] **Menu Order:** Where should new option appear in the menu list?

---

## Scoring Logic

- [ ] **StarterHelper Scoring Method:** What exact method/class does StarterHelper use?
- [ ] **Scoring Parameters:** What parameters does StarterHelper pass to the scoring method?
- [x] **Weekly vs Season-Long:** Use `use_weekly_projection` flag (Option A)
  - **Decision:** `use_weekly_projection=(week > 0)` - False for week 0, True for weeks 1-17
  - **Rationale:** Simplest implementation, uses existing parameter, week 0 → season-long projections from `fantasy_points`
  - **Date:** 2025-12-22
- [ ] **Scoring Initialization:** What setup is required before calling scoring (e.g., max_weekly_projection)?
- [ ] **Player Loading:** How to get all available players for scoring?
- [x] **Player Filtering:** Score all available players (Option A)
  - **Decision:** Score all players in `self.player_manager.players` (~1500 players)
  - **Rationale:** Comprehensive historical record, enables future analysis, negligible time difference vs filtering
  - **Date:** 2025-12-22
- [x] **JSON Score Precision:** Round to 2 decimal places (Option B)
  - **Decision:** `round(score, 2)` for all score values in JSON
  - **Rationale:** Standard for scoring values, good balance between precision and readability
  - **Date:** 2025-12-22

---

## Data Files & Historical Data

### Files to Copy

- [ ] **File List:** What files does player-data-fetcher currently copy to historical_data?
  - [ ] players.csv?
  - [ ] teams_week_N.csv?
  - [ ] league_config.json?
  - [ ] Other files?
- [ ] **Copy Method:** Use shutil.copy, or custom logic?
- [ ] **Overwrite Behavior:** What if files already exist in historical_data destination?

### Folder Structure

- [ ] **Season Determination:** How to get current SEASON value?
- [ ] **Week Determination:** How to get current WEEK value?
- [ ] **Folder Creation:** Should we create historical_data/{SEASON}/{WEEK} if it doesn't exist?
- [ ] **Week 0 Handling:** Confirm path for season-long is data/historical_data/{SEASON}/calculated_season_long_projected_points.json

### JSON Output

- [ ] **Player ID Format:** What format are player IDs (string, int)?
- [ ] **Score Precision:** How many decimal places for calculated scores?
- [ ] **JSON Structure:** Confirm simple flat dict {player_id: score} is sufficient
- [ ] **Empty Results:** What if no players are available to score?

---

## Error Handling & Edge Cases

- [ ] **Missing historical_data Folder:** Create automatically or error?
- [ ] **Missing Source Files:** Skip file copying or abort entirely?
- [ ] **Week > 17:** How to handle playoff weeks or off-season?
- [ ] **Empty players.csv:** Error and abort, or save empty JSON?
- [ ] **Malformed Data:** Validation strategy for input data?
- [ ] **File Write Failures:** How to handle permission errors or disk full?

---

## Architecture & Code Organization

- [ ] **New Mode Location:** Where should the new mode manager class be created?
  - Option A: `league_helper/save_scoring_mode/SaveScoringModeManager.py`
  - Option B: `league_helper/SaveScoringManager.py` (top level)
  - Option C: Add as method to LeagueHelperManager (no separate class)
- [ ] **Class Name:** SaveScoringModeManager? SaveCalculatedPointsManager? Other?
- [ ] **Inheritance:** Should it inherit from a base mode class?

---

## Testing & Validation

- [ ] **Unit Tests:** What aspects need unit test coverage?
- [ ] **Integration Tests:** How to test end-to-end (menu selection → file creation)?
- [ ] **Test Data:** Need fixture data for testing?
- [ ] **Verification:** How to verify JSON output is correct?

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Player data | players.csv via PlayerManager | Pending verification |
| Scoring method | StarterHelper scoring logic | Pending identification |
| Current week | ConfigManager | Pending verification |
| Current season | ConfigManager or elsewhere? | Pending |
| Files to copy | player-data-fetcher reference | Pending research |

---

## Resolution Log

### Codebase Verification - Round 1 Findings

**Player ID Format (RESOLVED from codebase):**
- `FantasyPlayer.id` is typed as `int` (utils/FantasyPlayer.py:88)
- JSON keys should be strings (JSON spec converts int keys to strings anyway)
- **Recommendation:** Use `str(player.id)` as JSON key for explicitness

**Season/Week Values (RESOLVED from codebase):**
- `ConfigManager.nfl_season` is typed as `int` (league_helper/util/ConfigManager.py:196)
- `ConfigManager.current_nfl_week` is typed as `int` (league_helper/util/ConfigManager.py:195)
- Values loaded from `league_config.json` which has `NFL_SEASON: 2025` (int)
- **Recommendation:** Direct use of config values is safe

**Week Number Format (RESOLVED from codebase):**
- player-data-fetcher uses zero-padded: `f"{CURRENT_NFL_WEEK:02d}"` (player_data_fetcher_main.py:393)
- Creates folders like `historical_data/2025/01/`, `historical_data/2025/15/`
- **Recommendation:** Use `f"{week:02d}"` to match existing pattern

**Files to Copy (RESOLVED from codebase):**
- player-data-fetcher copies: `["players.csv", "players_projected.csv", "game_data.csv"]` (lines 410)
- Also copies `team_data/` folder using `shutil.copytree()` (lines 424-427)
- **Recommendation:** Match this list exactly for consistency

**File Overwrite Behavior (RESOLVED from codebase):**
- player-data-fetcher skips if folder exists (idempotent) - lines 400-402
- Logs: "Historical data already saved for Week X (folder exists)"
- **Recommendation:** Match pattern - skip if folder exists, log info message

**Missing Files Handling (RESOLVED from codebase):**
- player-data-fetcher checks `source.exists()` before copying (line 417)
- If missing: `logger.warning(f"Source file not found: {source}")` and continues
- Does NOT abort - gracefully skips missing optional files
- **Recommendation:** Match pattern - warning for missing files, continue operation

**Logging Pattern (RESOLVED from codebase):**
- player-data-fetcher uses:
  - `logger.info()` for start/completion/skip messages
  - `logger.debug()` for per-file copy operations
  - `logger.warning()` for missing files (non-fatal)
- StarterHelperModeManager uses:
  - `logger.info()` for mode entry/exit with summary
  - `logger.debug()` for detailed operation logs
- **Recommendation:** info for mode start/completion, debug for per-player scoring, warning for missing files

**Mode Entry Point Pattern (RESOLVED from codebase):**
- Different modes use different entry point names:
  - AddToRosterModeManager: `start_interactive_mode(player_manager, team_data_manager)`
  - StarterHelperModeManager: `show_recommended_starters(player_manager, team_data_manager)`
  - TradeSimulatorModeManager: `run_interactive_mode()`
  - ModifyPlayerDataModeManager: `start_interactive_mode(player_manager)`
- **Recommendation:** Since this mode is non-interactive (just execute and return), use simple `execute()` method

**Exception Handling (RESOLVED from codebase):**
- Existing code does NOT wrap `score_player()` calls in try-except
- Assumption: score_player() does not raise exceptions under normal conditions
- **Recommendation:** Skip individual player on exception, log warning, continue

**Test Fixtures (RESOLVED from codebase):**
- Test fixtures exist at `tests/fixtures/accuracy_test_data/`
- Includes: `players_projected.csv`, `players_actual.csv`
- **Recommendation:** Use existing test fixture pattern for unit tests

**ConfigManager Error Handling (NEEDS USER DECISION):**
- ConfigManager loads config in `__init__`, may raise exceptions if file missing
- No evidence of ConfigManager returning None for season/week under normal conditions
- **Question:** Should we add defensive checks or trust ConfigManager initialization?

**Config Files Copy (RESOLVED):**
- **Decision:** Copy entire `data/configs/` folder to `historical_data/{SEASON}/{WEEK}/configs/`
- **Rationale:** Full reproducibility - preserves all configuration state at time of scoring
- **Implementation:** Use `shutil.copytree()` to copy configs folder
- **Date:** 2025-12-22

**drafted_data.csv Copy (RESOLVED):**
- **Decision:** Copy drafted_data.csv to historical_data
- **Rationale:** Captures roster state at time of scoring, enables historical analysis
- **Date:** 2025-12-22

**Progress Display (RESOLVED):**
- **Decision:** Summary message only (Option C)
- **Implementation:**
  - Entry: `logger.info(f"Entering Save Calculated Points mode (Week {week})")`
  - Completion: `print(f"Saved {count} player scores to {path}")`
- **Rationale:** 1-4 seconds is fast enough, summary provides confirmation, matches StarterHelper pattern
- **Date:** 2025-12-22

**JSON Metadata (RESOLVED):**
- **Decision:** Simple format without metadata wrapper (Option A)
- **Format:** `{player_id: score}` (flat dictionary)
- **Rationale:** Week/season in folder path, config in copied configs/, simpler to parse, YAGNI principle
- **Date:** 2025-12-22

**Parallelization (RESOLVED):**
- **Decision:** Sequential loop (Option A)
- **Implementation:** Simple `for player in self.player_manager.players:` loop
- **Rationale:** 1-4 seconds is acceptable, simplicity preferred, matches existing patterns, easier to maintain
- **Date:** 2025-12-22

---

### Items Categorized

**RESOLVED from codebase (11 items):**
1. Player ID format - int type
2. Season/week values - int type from ConfigManager
3. Week number format - zero-padded (02d)
4. Files to copy - match player-data-fetcher list
5. File overwrite behavior - skip if exists
6. Missing files handling - warning + continue
7. Logging pattern - info/debug/warning
8. Mode entry point - use execute() method
9. Exception handling - continue on error
10. Test fixtures - exist and available
11. Mode manager pattern - varies by mode

**NEEDS USER DECISION (10 items):**
1. Architecture: Mode manager vs simple utility class
2. Error handling: ConfigManager defensive checks?
3. league_config.json: Add to files_to_copy?
4. drafted_data.csv: Add to files_to_copy?
5. Progress display: Silent vs progress bar?
6. JSON metadata: Add timestamp/config info?
7. Parallelization: Sequential vs parallel?
8. Player filtering: All players vs subset?
9. Season-long scoring: How to handle week 0?
10. JSON precision: Full float vs rounded?

**UNKNOWN (requires further investigation - 0 items)**

---

| Item | Resolution | Date |
|------|------------|------|
| Player ID format | int → str for JSON keys | 2025-12-22 |
| Week number format | Zero-padded f"{week:02d}" | 2025-12-22 |
| Files to copy | Match player-data-fetcher list | 2025-12-22 |
| Q1: Mode manager structure | Full mode manager (Option A) | 2025-12-22 |
| Q2: ConfigManager error handling | Trust initialization (Option A) | 2025-12-22 |
| Q3: Config files to copy | Copy entire data/configs/ folder | 2025-12-22 |
| Q4: drafted_data.csv copy | Yes - copy for roster state (Option A) | 2025-12-22 |
| Q5: Progress display | Summary message only (Option C) | 2025-12-22 |
| Q6: JSON metadata | Simple format, no wrapper (Option A) | 2025-12-22 |
| Q7: Parallelization | Sequential loop (Option A) | 2025-12-22 |
| Q8: Player filtering | All available players (Option A) | 2025-12-22 |
| Q9: Season-long scoring (week 0) | use_weekly_projection=False (Option A) | 2025-12-22 |
| Q10: JSON score precision | Round to 2 decimals (Option B) | 2025-12-22 |

---

---

## ITERATION 1: Edge Cases, Error Conditions, Configuration

### Data Validation Edge Cases

- [ ] **Empty players.csv:** What if players.csv exists but has no player rows (only headers)?
  - Options: A) Error and abort, B) Save empty JSON {}, C) Warning and skip
- [ ] **Malformed player data:** What if a player has None/null for projected_points?
  - Options: A) Skip that player, B) Use 0.0 as default, C) Error and abort
- [ ] **Player scoring exception:** What if score_player() raises an exception for a specific player?
  - Options: A) Skip player and continue, B) Abort entire operation, C) Use 0.0 and log warning

### File System Edge Cases

- [ ] **Missing team_data folder:** What if data/team_data/ doesn't exist?
  - Context: Needed for matchup scoring
  - Options: A) Skip copying it, B) Create empty folder, C) Error and abort
- [ ] **Missing game_data.csv:** Already identified - decide on approach
- [ ] **Insufficient disk space:** What if historical_data creation fails due to disk full?
  - Options: A) Catch exception and display error, B) Pre-check disk space, C) Let OS error bubble up
- [ ] **Write permissions:** What if historical_data folder is read-only?
  - Options: A) Check permissions first, B) Catch exception and report, C) Assume permissions OK

### Configuration Edge Cases

- [ ] **Invalid week value:** Already identified - decide on validation approach
- [ ] **ConfigManager returns None:** What if current_nfl_week or nfl_season is None?
  - Context: Could happen if config is malformed
  - Options: A) Use fallback values, B) Error and abort, C) Validate config on mode start
- [ ] **Missing configs folder:** What if data/configs/ doesn't exist?
  - Context: ConfigManager loads league_config.json from there
  - Options: A) Handled by ConfigManager already, B) Need explicit check

### Week Number Format

- [ ] **Week number format:** Should we use zero-padded (01, 02) or regular (1, 2)?
  - Context: player-data-fetcher uses zero-padded: `f"{CURRENT_NFL_WEEK:02d}"`
  - Recommendation: Match player-data-fetcher pattern for consistency

---

## ITERATION 2: Logging, Performance, Testing, Integration

### Logging Strategy

- [ ] **Logging level:** What log level should mode operations use?
  - Context: StarterHelper uses debug/info, no error/warning
  - Options: A) info for start/completion, debug for player scoring, B) All debug, C) All info
- [ ] **Player scoring logs:** Should we log each player scored (1500+ log lines)?
  - Options: A) No individual logs (too verbose), B) Every 100 players, C) Summary only
- [ ] **File copy logs:** Should we log each file copied?
  - Context: player-data-fetcher logs each file copy with debug level
  - Recommendation: Match pattern - debug log per file
- [ ] **Error logging:** What to log when operations fail?
  - Options: A) error for critical failures (can't write JSON), B) warning for skippable (missing optional file), C) Both

### Performance Considerations

- [ ] **Scoring performance:** Is scoring 1500+ players fast enough for interactive menu?
  - Context: StarterHelper scores only roster (10-15 players), this scores ALL
  - Need: Rough estimate of time per player (10ms? 100ms?)
- [ ] **Parallelization:** Should we parallelize player scoring?
  - Options: A) No - simple loop is fine, B) Yes - use multiprocessing, C) Only if >1000 players
- [ ] **File copy performance:** Is copying team_data/ folder fast enough?
  - Context: team_data/ has ~32 team CSV files
  - Expectation: Should be sub-second operation

### Testing Requirements

- [ ] **Unit tests needed:** What aspects need unit test coverage?
  - A) SaveCalculatedPointsManager.execute() method
  - B) JSON format validation
  - C) File copying logic
  - D) Error handling for missing files
- [ ] **Integration tests:** How to test end-to-end without polluting historical_data?
  - Options: A) Use temp folder for tests, B) Clean up after test, C) Mock file operations
- [ ] **Test data:** Need fixture data for testing?
  - Context: Need sample players.csv, team_data/, etc.
  - Recommendation: Use existing test fixtures if available

### Integration with Existing Systems

- [ ] **State modification:** Does this mode modify any system state?
  - Context: Other modes modify player_manager.team.roster
  - Answer: No - read-only operation (scores players, writes files)
- [ ] **Callable from other modes:** Should this be callable programmatically or menu-only?
  - Options: A) Menu-only, B) Also expose as public method
  - Recommendation: Menu-only for now (simplest)
- [ ] **Player data reload:** Does this mode need to call reload_player_data()?
  - Context: LeagueHelperManager reloads before showing menu
  - Answer: No - menu handler already reloaded data

---

## ITERATION 3: Relationships, Cross-Cutting Concerns

### Relationship to Similar Features

- [ ] **ModifyPlayerDataMode comparison:** How does this relate to ModifyPlayerDataMode?
  - Similarity: Both deal with player data
  - Difference: Modify changes data in-place, this saves read-only snapshot
- [ ] **StarterHelper dependency:** Should scoring logic be extracted to shared utility?
  - Context: Both StarterHelper and this mode use same scoring call
  - Options: A) Duplicate initialization code, B) Extract to helper method, C) Keep separate
- [ ] **player-data-fetcher overlap:** After implementation, how to coordinate both?
  - Current: player-data-fetcher copies files (to be removed)
  - Future: Only this mode copies files
  - Question: Timeline for removing from player-data-fetcher?

### Multi-Season Support

- [ ] **Season folder structure:** Does folder structure handle multiple seasons correctly?
  - Path: `historical_data/{SEASON}/{WEEK}/`
  - Validation: Confirm ConfigManager.nfl_season returns int (e.g., 2025)
- [ ] **Cross-season data:** Any concerns about mixing data from different seasons?
  - Answer: No - season is part of folder path

### File Format & Future Compatibility

- [ ] **JSON format versioning:** Should we include format version in JSON?
  - Example: `{"version": "1.0", "players": {player_id: score}}`
  - Options: A) No - simple format unlikely to change, B) Yes - future-proof
- [ ] **league_config.json copy:** Should we also copy league_config.json for reproducibility?
  - Context: Scoring parameters come from league_config.json
  - Question: If scoring params change, can we reproduce old scores?
  - Recommendation: Yes - copy league_config.json to historical_data
- [ ] **Consumability:** Should saved JSON be usable by any existing/planned features?
  - Context: JSON is just {player_id: score}, no metadata
  - Future use: Could compare scores across weeks, analyze trends
  - Question: Any additional metadata needed (timestamp, config_name, etc.)?

### Idempotency & Race Conditions

- [ ] **Idempotent behavior:** If user runs mode twice for same week, what happens?
  - Context: player-data-fetcher skips if folder exists
  - Options: A) Skip if folder exists (idempotent), B) Overwrite always, C) Prompt user
  - Recommendation: Match player-data-fetcher - skip if exists
- [ ] **Race conditions:** What if player-data-fetcher runs simultaneously?
  - Context: Both write to same historical_data folder
  - Risk: File corruption or partial writes
  - Mitigation: Document that user shouldn't run both at once? Or add file locking?

### Additional File Considerations

- [ ] **drafted_data.csv:** Should we copy drafted_data.csv to historical_data?
  - Context: Tracks which players are on user's roster
  - Use case: Reproduce draft state at that week
  - Recommendation: Add to files_to_copy list

---

## Notes for Phase 2 Investigation

**ITERATION 1 COMPLETE:** Added 12 questions on edge cases, error conditions, configuration
**ITERATION 2 COMPLETE:** Added 11 questions on logging, performance, testing, integration
**ITERATION 3 COMPLETE:** Added 11 questions on relationships, cross-cutting concerns

**Total new questions:** 34 (in addition to 12 already identified)

**Next step:** Codebase verification rounds to answer questions from code where possible
