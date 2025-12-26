# Update Historical Data Fetcher for New Player Data - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `update_historical_data_fetcher_for_new_player_data_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Output structure:** Each week folder (week_01/ ... week_17/) should contain 6 JSON files - confirm structure
  - **RESEARCH:** Current structure has `players.csv` and `players_projected.csv` in each week folder
  - **✅ RESOLUTION:** Each week folder will contain:
    - If GENERATE_CSV=True: 2 CSV files (players.csv, players_projected.csv)
    - If GENERATE_JSON=True: 6 JSON files (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json)
    - Both can coexist (see Decision 1)

- [x] **Backward compatibility:** Do we need to keep CSV generation for any use case, or completely replace?
  - **RESEARCH FINDINGS:**
    - **Current consumers of CSV:** SimulatedLeague loads `players.csv` from week folders (line 165, 286, 298)
    - **SimulationManager validation:** Checks for `players.csv` existence (line 210-211)
    - **AccuracySimulationManager:** Uses `players.csv` (line 314)
    - **ParallelAccuracyRunner:** Uses `players.csv` (line 203)
  - **✅ RESOLUTION:** Add boolean toggles at top of compile_historical_data.py
    - `GENERATE_CSV = True` (default: True to maintain backward compatibility)
    - `GENERATE_JSON = True` (default: True to enable new format)
    - Keep CSV implementation but make it optional via toggle
    - **Simulation updates are OUT OF SCOPE** (future feature)
  - **RATIONALE:** Maximum flexibility, zero risk, clean configuration

- [x] **Data model:** Should historical compiler use ESPNPlayerData or continue with PlayerData?
  - **RESOLUTION:** Keep PlayerData for historical compiler, but add raw_stats field
  - **RATIONALE:** PlayerData is simpler and historical-specific. Can add raw_stats array to bridge to JSON exporter without full ESPNPlayerData overhead

---

## Data Structure & JSON Format Questions

### JSON File Structure

- [x] **Root key format:** Confirmed as `{position}_data` (e.g., `qb_data`) from example files
  - **VERIFIED:** Checked data/player_data/qb_data.json line 2: `"qb_data": [`
  - **SOURCE:** player-data-fetcher-new-data-format specs.md confirms this format

- [x] **File naming:** Confirmed as `qb_data.json`, `rb_data.json`, etc. (not `qb.json`)
  - **VERIFIED:** Actual files in data/player_data/ use `{position}_data.json` naming
  - **CONSISTENT:** Matches player-data-fetcher output

- [x] **Player filtering:** Should all players be included or filter by minimum criteria (e.g., minimum points)?
  - **RESEARCH:** Current player-data-fetcher includes all players from ESPN API (up to ESPN_PLAYER_LIMIT=1500)
  - **RESEARCH:** Historical compiler currently includes all players with any stats (PlayerData model)
  - **✅ RESOLUTION:** Include all players from ESPN API response (no filtering)
  - **RATIONALE:** Match current exporter behavior, provides complete data set for future analysis

### Field Mapping

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `id` | [x] | From ESPN API: player.id (already in PlayerData) |
| `name` | [x] | From ESPN API: player.fullName (already in PlayerData) |
| `team` | [x] | From ESPN API: player.proTeamId mapped to abbrev (already in PlayerData) |
| `position` | [x] | From ESPN API: player.defaultPositionId mapped (already in PlayerData) |
| `injury_status` | [x] | From ESPN API: player.injuryStatus (already in PlayerData) |
| `drafted_by` | [x] | **RESOLUTION:** Always null for historical data (no league context for past seasons) |
| `locked` | [x] | **RESOLUTION:** Always false for historical data (no locked state for past seasons) |
| `average_draft_position` | [x] | From ESPN API: ownership.averageDraftPosition (already in PlayerData) |
| `player_rating` | [x] | **RESOLUTION:** Use same algorithm as CSV generator - Week 1: draft-based, Week 2+: cumulative performance (see Decision 2) |
| `projected_points` | [x] | **RESOLUTION:** Array of 17 from statSourceId=1, with point-in-time logic (see Decision 2 and Decision 4 for quality verification) |
| `actual_points` | [x] | Array of 17 - source is statSourceId=0 (ESPN API stats array), verified available for historical data |

---

## API/Data Source Questions

### ESPN Historical API

- [x] **Historical stats availability:** Does ESPN API provide week-by-week stats (statSourceId=0 and 1) for past seasons?
  - **VERIFIED:** Historical compiler currently fetches ESPN data with `scoringPeriodId=0` (all weeks)
  - **CONFIRMED:** `_extract_weekly_points()` in player_data_fetcher.py extracts both statSourceId=0 and 1
  - **ANSWER:** YES - statSourceId=0 (actual) is available. statSourceId=1 (projected) availability TBD

- [x] **raw_stats availability:** Does historical API response include raw_stats array needed for detailed stat extraction?
  - **RESEARCH:** Current historical compiler uses `stats` array from ESPN API (player_data_fetcher.py:419)
  - **RESEARCH:** Current player-data-fetcher saves entire `raw_stats` array to ESPNPlayerData.raw_stats
  - **✅ RESOLUTION:** Add `raw_stats: List[Dict[str, Any]]` field to PlayerData model
  - **IMPLEMENTATION:** Populate from `player_info.get('stats', [])` in _create_player_data() method
  - **DOCUMENTED:** See specs.md Implementation Approach Step 3

- [x] **API endpoint:** Is the same ESPN Fantasy API endpoint used with just a different year parameter?
  - **VERIFIED:** constants.py line 17-19: `ESPN_FANTASY_API_URL = ...seasons/{year}/...`
  - **ANSWER:** YES - same endpoint, different year in URL

- [x] **Stat IDs consistency:** Are stat IDs (e.g., '3' for passing yards) consistent across years?
  - **RESEARCH:** ESPN stat IDs are standard across API (passing=3, rushing=24, etc.)
  - **ASSUMPTION:** Stat IDs are consistent across years (ESPN standard)
  - **ANSWER:** YES - stat IDs should be consistent

### Data Extraction

- [x] **statSourceId=0 (actual):** How to extract week-by-week actual stats for historical seasons?
  - **VERIFIED:** Already implemented in historical_data_compiler/player_data_fetcher.py:436-448
  - **ANSWER:** `stat.get('statSourceId') == 0` from stats array, `stat.get('appliedTotal')` for points

- [x] **statSourceId=1 (projected):** Do historical projections exist, or should we use actuals for both arrays?
  - **RESEARCH:** Current historical compiler extracts statSourceId=1 (player_data_fetcher.py:445-446)
  - **RESEARCH:** Stores in `projected_weeks` dict (line 462)
  - **✅ RESOLUTION:** Option A - Test first, then decide (with mandatory user verification)
  - **IMPLEMENTATION APPROACH:**
    1. Implement standard path: Use statSourceId=1 for projected_points array
    2. During smoke testing, generate 2023 week 1 JSON
    3. **MANDATORY STOP POINT:** Agent must verify projection quality with user:
       - Inspect 3-5 sample players (QB, RB, WR, TE, K)
       - Compare projected_points vs actual_points
       - Present findings to user with evidence
    4. **USER DECISION REQUIRED:** If projections are poor/missing, user will decide on fallback approach
    5. **DO NOT** automatically implement fallback without user approval
  - **RATIONALE:** Evidence-based decision with user oversight before any changes

- [x] **appliedStats vs stats:** Current exporter uses `stats` dict, historical uses `appliedTotal` - verify correct field
  - **RESEARCH FINDINGS:**
    - Historical compiler: Uses `stat.get('appliedTotal')` for fantasy points (player_data_fetcher.py:437)
    - Current exporter: Uses `stats_dict = stat.get('stats', {})` for individual stat extraction (player_data_exporter.py:643)
    - **BOTH ARE CORRECT:** `appliedTotal` = fantasy points total, `stats` = dict of individual stats (stat ID → value)
  - **ANSWER:** Use `appliedTotal` for points arrays, `stats` dict for position-specific stat extraction

- [x] **Current week filtering:** Historical data has no "current week" - all weeks are complete. How to handle?
  - **RESEARCH:** Current exporter uses `CURRENT_NFL_WEEK` to filter statSourceId=0 (player_data_exporter.py:607-612)
  - **REASONING:** ESPN pre-populates statSourceId=0 for future weeks with projection data
  - **✅ RESOLUTION:** For point-in-time snapshots, each week folder has its own "current_week" (1-17)
  - **IMPLEMENTATION:** Week N snapshot uses weeks 1 to N-1 for actuals, zeros for N to 17 (see Decision 2)
  - **RATIONALE:** Not "all weeks complete" - each snapshot simulates being at that week in the season

---

## Algorithm/Logic Questions

### Weekly Snapshot Point-in-Time Logic

The current weekly_snapshot_generator creates point-in-time snapshots for CSV where:
- Week N's players.csv: actual for weeks 1 to N-1, projected for N to 17
- Week N's players_projected.csv: historical projections for past weeks, current projection for future

**Questions:**
- [x] **Point-in-time for JSON:** Do we apply same logic to JSON files? (past=actual, future=projected)
  - **RESEARCH:** Current CSV logic is in weekly_snapshot_generator.py:193-209 (players.csv) and :276-296 (players_projected.csv)
  - **CURRENT BEHAVIOR:** Week N uses actual for weeks 1 to N-1, projected for N to 17
  - **✅ RESOLUTION:** YES - Apply point-in-time logic to JSON arrays (Option A)
  - **RATIONALE:** Consistency with CSV snapshots, realistic simulation, clear semantics

- [x] **projected_points array:** For week N snapshot, should weeks >= N use week N's projection?
  - **RESEARCH:** players_projected.csv logic (line 276-296): past weeks use historical projection, future weeks use current week's projection
  - **✅ RESOLUTION:** YES - Follow same pattern as CSV
    - Weeks 1 to N-1: Use historical projections (statSourceId=1 for each week)
    - Weeks N to 17: Use current week N's projection (repeated)
  - **RATIONALE:** Matches existing CSV behavior, represents "best available projection at that time"

- [x] **actual_points array:** For week N snapshot, should weeks >= N be zeros (game not played yet)?
  - **✅ RESOLUTION:** YES - Use zeros for weeks >= N (games not yet played)
  - **IMPLEMENTATION:** For week N, `actual_points[N-1 through 16] = 0.0`
  - **RATIONALE:** Clear semantics (0 = game not played), matches point-in-time model

- [x] **Stat arrays:** Should position-specific stats (passing, rushing, etc.) follow same point-in-time logic?
  - **✅ RESOLUTION:** YES - Extract stats for weeks 1 to N-1 only, zeros for weeks >= N
  - **IMPLEMENTATION:** For week N snapshot, all stat arrays (passing, rushing, receiving, etc.) have zeros for weeks >= N
  - **RATIONALE:** Stats represent actual performance (like actual_points), consistent semantics

### Player Rating Calculation

Current CSV logic (weekly_snapshot_generator.py:47-108):
- Week 1: Use draft-based rating from ESPN
- Week 2+: Calculate from cumulative actual points through (current_week - 1)

**Questions:**
- [x] **Rating for historical JSON:** Use same algorithm as CSV?
  - **✅ RESOLUTION:** YES - reuse existing algorithm from weekly_snapshot_generator.py
  - **RATIONALE:** Algorithm already works correctly, tested, matches point-in-time semantics

- [x] **Rating recalculation:** Does each week's JSON need different player_rating values (point-in-time)?
  - **RESEARCH:** Current CSV generates different ratings per week based on cumulative performance
  - **✅ RESOLUTION:** YES - each week folder has different player_rating values (point-in-time)
  - **IMPLEMENTATION:** Use existing _calculate_player_ratings() method from weekly_snapshot_generator.py
  - **DOCUMENTED:** See Decision 2 in specs.md (player_rating recalculation algorithm)
  - **IMPLEMENTATION:** Call `_calculate_player_ratings(players, current_week)` for each week

- [x] **Rating for final JSON:** If generating for completed season, use final cumulative ratings?
  - **ANSWER:** N/A - we generate per-week snapshots, not a single season file
  - **CLARIFICATION:** Each week_NN folder has its own JSON files with point-in-time ratings

### Historical Projections

- [x] **Projection availability:** Did ESPN have pre-game projections for historical seasons that we can access?
  - **RESOLUTION:** Will test during smoke testing and verify with user
  - **ACTION:** Agent must stop and present findings before proceeding

- [x] **Projection fallback:** If no historical projections, use actual stats as "projections" for testing purposes?
  - **RESOLUTION:** User will decide on fallback approach ONLY if testing reveals poor projection quality
  - **PROCESS:** Agent presents evidence → User approves approach → Agent implements

- [x] **Projection semantics:** Should projected_points represent "what ESPN predicted before season" or "what happened"?
  - **RESOLUTION:** Prefer pre-game projections (statSourceId=1) if quality is good
  - **VERIFICATION:** Test quality during smoke testing with user approval before any changes

---

## Architecture Questions

### Code Structure

- [x] **PlayerData vs ESPNPlayerData:** Should historical compiler switch to ESPNPlayerData model?
  - **DECISION:** Keep PlayerData, add raw_stats field
  - **RESOLUTION:** Add `raw_stats: List[Dict[str, Any]] = field(default_factory=list)` to PlayerData in player_data_fetcher.py

- [x] **raw_stats population:** If using ESPNPlayerData, how to populate raw_stats array from historical API?
  - **RESOLUTION:** Add raw_stats to PlayerData, populate from `player_info.get('stats', [])`in `_parse_single_player()`
  - **IMPLEMENTATION:** `player_data.raw_stats = player_info.get('stats', [])` before returning PlayerData

- [x] **Exporter reuse:** Can we reuse player-data-fetcher/player_data_exporter.py code?
  - **RESEARCH FINDINGS:**
    - Current exporter has all stat extraction logic (lines 615-803)
    - Depends on ESPNPlayerData model and DraftedRosterManager
    - Uses config values like CURRENT_NFL_WEEK, DRAFTED_DATA
  - **✅ RESOLUTION:** Option C - Bridge Adapter Pattern
  - **IMPLEMENTATION:**
    - Create `historical_data_compiler/json_exporter.py` with adapter layer
    - Import stat extraction methods from player_data_exporter
    - Convert PlayerData → minimal ESPNPlayerData-like object
    - Reuse existing stat extraction methods (zero changes to current exporter)
  - **RATIONALE:**
    - Zero risk to current system (no changes to working code)
    - Minimal duplication (~50 lines adapter vs 200+ lines stat extraction)
    - Proven adapter design pattern
    - Historical-specific needs handled in adapter (no draft state, current_week=18)

- [x] **Module location:** Should JSON export code live in historical_data_compiler or reuse current exporter?
  - **✅ RESOLUTION:** New file `historical_data_compiler/json_exporter.py` with bridge adapter
  - **IMPLEMENTATION:** Adapter imports from player-data-fetcher, calls stat extraction methods
  - **STRUCTURE:**
    - `json_exporter.py`: Adapter layer + JSON file generation (~150 lines)
    - Reuses: `player_data_exporter.py` stat extraction methods (~200 lines)
    - Net savings: ~120 lines vs full duplication

### File Organization

- [x] **weekly_snapshot_generator.py:** Modify existing file or create new JSON-specific generator?
  - **CURRENT FILE:** 344 lines, generates CSV files
  - **✅ RESOLUTION:** Option A - Add method to call json_exporter from existing WeeklySnapshotGenerator
  - **IMPLEMENTATION:** Add `_generate_json_files()` method that calls json_exporter.generate_json_snapshots()
  - **RATIONALE:** Keeping CSV (Decision 1), so integrate JSON generation into existing workflow
  - **DOCUMENTED:** See specs.md Implementation Step 5

- [x] **Entry point:** Does compile_historical_data.py need changes beyond calling JSON generator?
  - **ANSWER:** Minimal changes needed
  - **CHANGES:** Update Phase 5 call from `generate_weekly_snapshots()` to also call JSON generation
  - **OUTPUT:** Update docstring to show JSON files in week folders

- [x] **Constants:** Need to add new constants for JSON file names?
  - **ANSWER:** YES
  - **IMPLEMENTATION:** Add to constants.py:
    ```python
    # JSON file names (add after line 117)
    QB_DATA_FILE = "qb_data.json"
    RB_DATA_FILE = "rb_data.json"
    WR_DATA_FILE = "wr_data.json"
    TE_DATA_FILE = "te_data.json"
    K_DATA_FILE = "k_data.json"
    DST_DATA_FILE = "dst_data.json"
    POSITION_JSON_FILES = [QB_DATA_FILE, RB_DATA_FILE, WR_DATA_FILE, TE_DATA_FILE, K_DATA_FILE, DST_DATA_FILE]
    ```

### Integration Points

- [x] **Simulation system:** Does simulation expect exact same structure as current player data?
  - **RESEARCH:** Simulation currently loads CSV files only (SimulatedLeague.py, SimulationManager.py)
  - **ANSWER:** No - simulation expects CSV format, not JSON
  - **IMPLICATION:** Need to keep CSV or update simulation (out of scope vs in scope decision)

- [x] **Data loading:** What code loads the historical JSON files? Need to verify compatibility
  - **RESEARCH:** No code currently loads historical JSON files (JSON format doesn't exist yet)
  - **✅ RESOLUTION:** Option A - Future Simulation System (No Consumer Yet)
  - **USER CONTEXT:** JSON files will eventually be used by:
    1. Updated simulation system (future feature)
    2. Updated league helper classes with new stats for scoring (future feature)
    3. Optimization of scoring weights for new metrics (future feature)
  - **IN SCOPE:** Generate JSON files with correct structure
  - **OUT OF SCOPE:** Building the consumer (simulation updates, league helper updates)
  - **TESTING:** Structure validation against current player_data/*.json files

- [x] **Testing:** Can we test with real historical data (e.g., 2023 season)?
  - **✅ RESOLUTION:** YES - include in smoke testing protocol
  - **COMMAND:** `python compile_historical_data.py --year 2023 --weeks 1-3`
  - **VERIFICATION:** Compare generated JSON structure to current player_data/*.json structure
  - **DOCUMENTED:** See specs.md Smoke Testing Protocol Part 2

---

## Output Consumer Validation (MANDATORY)

### Consumer Identification

| Output | Consumer(s) | Consumer Location | What Consumer Expects |
|--------|-------------|-------------------|----------------------|
| week_NN/players.csv | SimulatedLeague | simulation/win_rate/SimulatedLeague.py:165,286,298 | CSV with specific column format |
| week_NN/players.csv | SimulationManager | simulation/win_rate/SimulationManager.py:210-211 | File existence check |
| week_NN/players.csv | AccuracySimulationManager | simulation/accuracy/AccuracySimulationManager.py:314 | CSV format |
| week_NN/players.csv | ParallelAccuracyRunner | simulation/accuracy/ParallelAccuracyRunner.py:203 | CSV format |
| week_NN/{position}_data.json | Future Simulation System | **OUT OF SCOPE** (future feature) | Same structure as data/player_data/*.json |

### Roundtrip Test Requirements

```
✅ Output: sim_data/YEAR/weeks/week_NN/{6 JSON files}
  ✅ Consumer: Future Simulation System (out of scope for this feature)
    ✅ Required files: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
    ✅ Required structure: Same as data/player_data/*.json files
    ✅ Roundtrip test: Structure validation against current player_data/*.json
      - Load generated JSON and verify schema matches
      - Verify all required fields present
      - Verify point-in-time logic in arrays
      - Manual inspection of sample week
```

**Action items:**
- [x] **User clarification:** What will consume the historical JSON files?
  - **ANSWER:** Future simulation system and league helper updates (out of scope)
  - **THIS FEATURE:** Generate JSON files with correct structure for future use
- [x] **Simulation update scope:** Is updating simulation to load JSON in scope, or future work?
  - **ANSWER:** OUT OF SCOPE - future work (see Decision 1)
- [x] **CSV continuation:** Based on consumer needs, keep CSV generation?
  - **ANSWER:** YES - Keep CSV with boolean toggle (see Decision 1)

---

## Edge Cases

### Bye Weeks

- [x] **Bye week representation:** In stat arrays, should bye weeks be 0.0 or null?
  - **RESEARCH:** Current player-data-fetcher uses 0 (never null) - Decision 11 in specs
  - **ANSWER:** Use 0.0 for bye weeks (consistent with current format)

- [x] **Bye week consistency:** Verify bye week handling matches current JSON exporter
  - **VERIFIED:** Current exporter puts 0 for bye weeks in all arrays
  - **ANSWER:** Match this behavior

### Incomplete Historical Data

- [x] **Missing players:** What if a player has no stats for some weeks in historical data?
  - **RESEARCH:** Current historical compiler includes players with any stats (player_data_fetcher.py:246-259)
  - **ANSWER:** Include player with 0 for weeks without stats

- [x] **Injured players:** How to represent players who were injured all season?
  - **RESEARCH:** injury_status field from ESPN API (player_data_fetcher.py:371)
  - **ANSWER:** Include player with injury_status field, zeros for weeks injured

- [x] **Mid-season additions:** Players who joined team mid-season - how to handle early weeks?
  - **ANSWER:** Zeros for weeks before they joined (same as current behavior)

### Position-Specific Stats

- [x] **Stat availability:** Are all stat IDs available for historical seasons (e.g., targets, sacks)?
  - **ASSUMPTION:** ESPN stat IDs are consistent across years
  - **ANSWER:** Should be available, verify during testing

- [x] **Missing stats:** If a stat is missing from historical API, use 0.0?
  - **RESEARCH:** Current exporter returns 0.0 for missing stats (player_data_exporter.py:646)
  - **ANSWER:** YES - use 0.0 for missing stats

- [x] **DST special cases:** Do DST stats work same way for historical data?
  - **RESEARCH:** DST can have negative points, special handling exists (player_data_fetcher.py:452-453, 460-461)
  - **ANSWER:** Same logic applies to historical data

### Data Validation

- [x] **Negative values:** DST can have negative points - ensure this works for historical
  - **VERIFIED:** Historical compiler already handles DST negatives (player_data_fetcher.py:452-457)
  - **ANSWER:** Already handled

- [x] **NaN/null handling:** How to handle NaN or null values from ESPN API?
  - **RESEARCH:** Historical compiler checks for NaN (player_data_fetcher.py:442)
  - **ANSWER:** Skip NaN values, use 0 for missing data

- [x] **Zero points:** How to distinguish "no data" from "scored zero points"?
  - **ANSWER:** No distinction needed - both represented as 0.0 in arrays

---

## Testing & Validation

### Unit Tests

- [x] **Test coverage:** What tests need to be added for JSON generation?
  - **✅ RESOLUTION:** Implementation detail - will be in TODO file
  - **REQUIRED TESTS:**
    - Test JSON structure matches current player_data format
    - Test stat extraction from raw_stats array
    - Test point-in-time logic (past vs future weeks)
    - Test player rating calculation per week
    - Test all 6 position files generated
    - Test array lengths (17 elements)
    - Test bye week handling (zeros in arrays)
  - **DOCUMENTED:** See specs.md Testing Strategy section

- [x] **Mock data:** Need mock ESPN historical API responses?
  - **✅ RESOLUTION:** YES - create mock API response fixture
  - **PURPOSE:** Fast unit tests without network calls
  - **IMPLEMENTATION DETAIL:** Will be in TODO file

- [x] **Stat extraction:** Test individual stat extraction from raw_stats
  - **✅ RESOLUTION:** Port tests from test_player_data_exporter.py for stat extraction methods
  - **IMPLEMENTATION DETAIL:** Will be in TODO file

### Integration Tests

- [x] **Full compilation:** Test complete historical data compilation for one season
  - **✅ RESOLUTION:** Include in smoke testing protocol (not automated integration test)
  - **VERIFICATION:** Check all week folders have 6 JSON files
  - **DOCUMENTED:** See specs.md Smoke Testing Protocol Part 2

- [x] **Format validation:** Verify JSON structure matches current player_data format
  - **✅ RESOLUTION:** Include in smoke testing protocol
  - **IMPLEMENTATION:** Load generated JSON and compare keys/structure to data/player_data/qb_data.json
  - **DOCUMENTED:** See specs.md Smoke Testing Protocol Part 3

- [x] **Roundtrip test:** Load generated JSON and verify it can be consumed by simulation
  - **✅ RESOLUTION:** OUT OF SCOPE - no consumer yet (see Decision 5)
  - **ALTERNATIVE:** Structure validation only (documented in smoke testing protocol)
  - **FUTURE:** Automated roundtrip test when simulation consumer is built

### Smoke Tests

- [x] **Real data test:** Compile 2023 season and verify output
  - **✅ RESOLUTION:** Part of smoke testing protocol (Decision 4)
  - **COMMAND:** `python compile_historical_data.py --year 2023 --weeks 1-3`
  - **VERIFICATION:** Check simulation/sim_data/2023/weeks/week_01/ has 6 JSON files
  - **VALIDATION:** Manually inspect one JSON file for correctness
  - **DOCUMENTED:** See specs.md Smoke Testing Protocol Parts 2, 4, 5
  - **🛑 MANDATORY STOP POINT:** Historical projection quality verification with user (Decision 4)

- [x] **Comparison:** Compare week 1 2024 historical JSON to current 2024 player_data JSON structure
  - **✅ RESOLUTION:** Part of structure validation in smoke testing
  - **PURPOSE:** Verify historical JSON matches current JSON format exactly
  - **METHOD:** Diff keys and structure between files
  - **DOCUMENTED:** See specs.md Smoke Testing Protocol Part 3

- [x] **File count:** Verify each week folder has exactly 6 JSON files
  - **✅ RESOLUTION:** Part of smoke testing manual verification
  - **CHECK:** Each week folder has 6 position files (if GENERATE_JSON=True)
  - **DOCUMENTED:** See specs.md Smoke Testing Protocol Part 4

---

## Performance Considerations

### I/O Operations

- [x] **JSON writing:** 17 weeks × 6 files = 102 JSON files - any performance concerns?
  - **✅ RESOLUTION:** No performance concerns - use simple synchronous writes
  - **RESEARCH:** Current player-data-fetcher writes 6 JSON files with aiofiles (async I/O)
  - **DECISION:** Use synchronous json.dump() to match existing CSV write pattern
  - **ESTIMATE:** 102 small JSON files (~1-5MB total) should write in < 1 second
  - **RATIONALE:** Historical compilation is batch operation (not time-critical), consistency with CSV approach

- [x] **Memory usage:** Loading all player data for JSON generation - optimize if needed?
  - **✅ RESOLUTION:** No optimization needed
  - **CURRENT:** Historical compiler loads all players into memory (list of PlayerData)
  - **ESTIMATE:** ~1500 players × ~500 bytes = ~750KB (minimal)
  - **ANSWER:** Memory usage is negligible, no optimization required

- [x] **Async I/O:** Should JSON writing be async like current exporter?
  - **✅ RESOLUTION:** NO - use synchronous writes to match CSV approach
  - **RESEARCH:** Current exporter uses `aiofiles` for async writes
  - **CURRENT:** Historical compiler uses synchronous CSV writes
  - **RATIONALE:** Consistency with existing historical compiler pattern, simpler implementation
  - **RECOMMENDATION:** Keep synchronous for consistency with historical compiler patterns
  - **ALTERNATIVE:** Use async if reusing current exporter code

### API Calls

- [x] **Rate limiting:** Does historical API have same rate limits as current API?
  - **RESEARCH:** Historical compiler uses same BaseHTTPClient with RATE_LIMIT_DELAY=0.3s
  - **ANSWER:** YES - same rate limiting applies

- [x] **Batch requests:** Can we batch player requests for historical seasons?
  - **RESEARCH:** Historical compiler fetches all players in one request (scoringPeriodId=0)
  - **ANSWER:** Already batched

- [x] **Caching:** Should we cache API responses during development?
  - **CURRENT:** No caching implemented
  - **RECOMMENDATION:** Not needed - compilation is one-time per season

---

## Documentation

- [x] **README updates:** Document new JSON output format in compile_historical_data.py
  - **LOCATION:** Docstring lines 10-18 needs update
  - **CHANGE:** Add JSON files to output structure documentation

- [x] **Constants documentation:** Document new constants for JSON filenames
  - **DONE:** See Architecture section - constants to add listed

- [x] **Migration guide:** Document transition from CSV to JSON for users
  - **✅ RESOLUTION:** No migration guide needed
  - **RATIONALE:** Keeping CSV with boolean toggles (Decision 1), both formats coexist
  - **USERS:** Can enable/disable each format independently via toggles
  - **FUTURE:** When simulation is updated to use JSON, users can toggle GENERATE_CSV=False

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Player basic info | ESPN API (historical) | ✅ Working (same endpoint, year parameter) |
| Weekly actual points (statSourceId=0) | ESPN API stats array | ✅ Verified - currently extracted |
| Weekly projected points (statSourceId=1) | ESPN API stats array | ⚠️ Extracted but quality needs verification |
| Detailed stats (passing, rushing, etc.) | ESPN API stats dict | ✅ Available - need to add raw_stats to PlayerData |
| Player ratings | Calculated from cumulative points | ✅ Algorithm exists in CSV generator |
| Bye weeks | Derived from schedule | ✅ Working |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| **API Endpoint** | Same ESPN endpoint with year parameter | 2025-12-25 |
| **Stat IDs** | Consistent across years (ESPN standard) | 2025-12-25 |
| **File naming** | {position}_data.json format verified | 2025-12-25 |
| **Root key** | "{position}_data" key verified | 2025-12-25 |
| **Bye week handling** | Use 0.0 in arrays (never null) | 2025-12-25 |
| **DST negatives** | Already handled correctly | 2025-12-25 |
| **NaN handling** | Skip NaN, use 0 for missing | 2025-12-25 |
| **Edge cases** | Missing players, injuries all use 0 for absent weeks | 2025-12-25 |
| **Constants needed** | 6 position JSON file name constants | 2025-12-25 |
| **PlayerData model** | Keep existing, add raw_stats field | 2025-12-25 |
| **Backward compatibility** | Boolean toggles (GENERATE_CSV, GENERATE_JSON) in compile_historical_data.py | 2025-12-25 |
| **Simulation updates** | OUT OF SCOPE - future feature | 2025-12-25 |
| **Historical projections** | Test-first approach with MANDATORY user verification before any fallback | 2025-12-25 |
| **Point-in-time logic** | Apply to all JSON arrays (actual_points, projected_points, stat arrays) | 2025-12-25 |
| **Player rating calculation** | Reuse existing CSV algorithm (Week 1: draft-based, Week 2+: cumulative) | 2025-12-25 |
| **Code reuse strategy** | Bridge adapter pattern - import stat extraction from player_data_exporter | 2025-12-25 |
| **Module location** | New file: historical_data_compiler/json_exporter.py | 2025-12-25 |

---

## Critical User Decisions Needed (Top Priority)

### 1. Backward Compatibility (BLOCKS EVERYTHING)
**Question:** Keep CSV generation alongside JSON, or remove CSV entirely?
- **Impact:** Affects simulation system (currently uses CSV)
- **Options:** A) Dual output (CSV + JSON), B) JSON only + update simulation, C) JSON only (breaks simulation)
- **Recommendation:** Option A (dual output) initially

### 2. Historical Projections Quality
**Question:** Are ESPN's historical statSourceId=1 projections meaningful pre-game projections?
- **Impact:** Affects projected_points array semantics
- **Action:** Test with 2023 data to verify quality
- **Fallback:** Use actuals if projections are poor/missing

### 3. Point-in-Time Logic for JSON
**Question:** Apply same point-in-time logic as CSV to JSON arrays?
- **Current CSV:** Week N has actuals for weeks 1 to N-1, projections for N to 17
- **For JSON:** Use same logic for actual_points and stat arrays?
- **Impact:** Data semantics and usefulness

### 4. Code Reuse Strategy
**Question:** How to reuse existing stat extraction code?
- **Options:** A) Copy methods, B) Refactor exporter, C) Bridge adapter
- **Impact:** Code maintainability and implementation complexity

### 5. Consumer Identification
**Question:** What will consume the historical JSON files?
- **Impact:** Determines if simulation update is in scope
- **Affects:** Testing strategy and validation approach

---

## Next Steps After User Decisions

1. **IF keeping CSV:** Implement dual output (minimal changes)
2. **IF removing CSV:** Update simulation system to load JSON (larger scope)
3. **Test historical projections:** Run against 2023 data to verify quality
4. **Implement raw_stats:** Add field to PlayerData and populate from API
5. **Implement JSON generation:** Based on code reuse decision
6. **Update point-in-time logic:** Based on user decision
7. **Testing:** Unit tests, integration tests, smoke tests
