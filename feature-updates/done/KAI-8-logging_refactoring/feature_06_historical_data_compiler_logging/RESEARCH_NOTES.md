# Research Notes: Feature 06 (historical_data_compiler_logging)

**Created:** 2026-02-06
**Phase:** S2.P1.I1 (Feature-Level Discovery)

---

## Entry Point Research

### compile_historical_data.py

**File:** `/compile_historical_data.py`
**Total Lines:** 312
**Current Logging Setup:** Lines 258-260

```python
# Current setup (line 258-260)
log_level = "DEBUG" if args.verbose else "INFO"
setup_logger(name="historical_data_compiler", level=log_level)
logger = get_logger()
```

**Key Findings:**
- Uses `setup_logger()` from `utils.LoggingManager`
- Logger name: `"historical_data_compiler"` ✅ (matches folder name requirement from Feature 01)
- **NO `log_to_file` parameter** - currently missing
- Has `--verbose` flag (lines 85-87) but NO `--enable-log-file` flag

**Required Changes:**
1. Add `--enable-log-file` flag to argument parser (after line 87)
2. Pass `log_to_file=args.enable_log_file` to `setup_logger()` call (line 260)
3. Follow Feature 01 integration contract: `log_file_path=None` (let LoggingManager auto-generate)

**Example modification:**
```python
# Add to parser (after line 87):
parser.add_argument(
    "--enable-log-file",
    action="store_true",
    help="Enable file logging to logs/historical_data_compiler/"
)

# Modify setup_logger call (line 260):
setup_logger(
    name="historical_data_compiler",
    level=log_level,
    log_to_file=args.enable_log_file,  # NEW
    log_file_path=None  # NEW (let LoggingManager auto-generate)
)
```

**Logger Usage in compile_historical_data.py:**
- Line 131: `logger = get_logger()` (in create_output_directories)
- Line 159: `logger = get_logger()` (in cleanup_on_error)
- Line 179: `logger = get_logger()` (in compile_season_data)
- Total ~22 logger.info/warning/error calls throughout main workflow

---

## Module Research

### Modules Using Logging

Found 7 modules in `historical_data_compiler/` that use logging:

1. **http_client.py** (204 lines)
   - Line 79: `self.logger = get_logger()`
   - Usage: 5 logger calls (3 debug, 1 error)
   - Focus: HTTP request lifecycle

2. **player_data_fetcher.py** (517 lines)
   - Line 150: `self.logger = get_logger()`
   - Usage: ~7 logger calls (1 debug, 4 info, 1 warning)
   - Focus: Player data fetching progress

3. **json_exporter.py** (436 lines)
   - Line 76: `self.logger = get_logger()`
   - Usage: ~5 logger calls (2 debug, 2 warning, 1 info)
   - Focus: JSON export progress

4. **weekly_snapshot_generator.py** (~180 lines)
   - Uses `get_logger()`
   - Usage: ~3 logger calls (1 debug, 2 info)
   - Focus: Weekly snapshot generation

5. **team_data_calculator.py** (~260 lines)
   - Uses `get_logger()`
   - Usage: ~6 logger calls (all info)
   - Focus: Team data calculation progress

6. **game_data_fetcher.py** (~424 lines)
   - Uses `get_logger()`
   - Usage: ~13 logger calls (3 debug, 4 info, 3 warning, 3 error)
   - Focus: Game data fetching with weather

7. **schedule_fetcher.py** (~193 lines)
   - Uses `get_logger()`
   - Usage: ~6 logger calls (2 debug, 4 info)
   - Focus: Schedule fetching progress

**Total Logger Calls:** ~69 across all files
- compile_historical_data.py: ~22 calls
- Modules: ~47 calls

**Integration with Feature 01:**
- All modules use `get_logger()` (not direct logger creation)
- Logger name set in compile_historical_data.py: `"historical_data_compiler"`
- Feature 01's LineBasedRotatingHandler will be used automatically when `log_to_file=True`
- Log folder: `logs/historical_data_compiler/` (auto-created by Feature 01)

---

## Log Quality Analysis

### Current Logging Patterns

**DEBUG Level Usage:**
- http_client.py:
  - ✅ GOOD: "Created new HTTP client session" (lifecycle event)
  - ✅ GOOD: "Making {method} request to: {url}" (function entry with params)
  - ✅ GOOD: "Request successful" (outcome)
- game_data_fetcher.py:
  - ✅ GOOD: "Loaded coordinates for {N} stadiums" (data transformation outcome)
  - ✅ GOOD: "Fetching game data for week {week}/{total}" (progress in loop)
  - ⚠️ CHECK: "No coordinates for {team}/{city}, skipping weather" (conditional branch taken)
- schedule_fetcher.py:
  - ✅ GOOD: "Fetching schedule for week {week}/{total}" (progress in loop)
  - ⚠️ CHECK: "Error parsing event in week {week}: {e}" (could be warning instead?)
- json_exporter.py:
  - ✅ GOOD: "Generated {position} JSON: {N} players" (outcome with counts)
  - ✅ GOOD: "Generated {N} JSON files for week {week}" (summary outcome)
- weekly_snapshot_generator.py:
  - ✅ GOOD: "Generated week {week} snapshot" (outcome per iteration)

**INFO Level Usage:**
- compile_historical_data.py:
  - ✅ GOOD: "Starting compilation for {year} season" (script start with config)
  - ✅ GOOD: "[1/5] Fetching schedule data..." (major phase transition)
  - ✅ GOOD: "  - Schedule fetched for {N} weeks" (significant outcome)
  - ✅ GOOD: "Compilation complete for {year} season" (script complete)
  - ✅ GOOD: "Output written to: {path}" (significant outcome with location)
  - ✅ GOOD: "Created output directory: {path}" (major phase outcome)
- player_data_fetcher.py:
  - ✅ GOOD: "Fetching all players for {year} season" (phase start with config)
  - ✅ GOOD: "Fetched {N} players for {year} season" (phase complete with outcome)
  - ✅ GOOD: "Writing players to {path}" (phase start)
  - ✅ GOOD: "Wrote {N} players to {path}" (phase complete with outcome)
- team_data_calculator.py:
  - ✅ GOOD: "Calculating team data from player stats" (phase start)
  - ✅ GOOD: "Calculated data for {N} teams" (phase complete with outcome)
- game_data_fetcher.py:
  - ✅ GOOD: "Fetching game data for {year} season (weeks 1-{N})" (phase start with config)
  - ✅ GOOD: "Fetched {N} games for {year} season" (phase complete with outcome)

**WARNING Level Usage:**
- All warning usages appear appropriate (partial data, non-fatal errors, user alerts)

**ERROR Level Usage:**
- All error usages appear appropriate (fatal errors with exc_info=True)

### Log Quality Gaps

**Potential Improvements:**

1. **Missing DEBUG logs for data transformations:**
   - player_data_fetcher.py: Could add DEBUG for player parsing logic (before/after transformation)
   - team_data_calculator.py: Could add DEBUG for team aggregation calculations

2. **Missing INFO logs for configuration:**
   - compile_historical_data.py: Could log GENERATE_CSV/GENERATE_JSON toggle values at startup
   - http_client.py: Could log configuration (timeout, rate_limit_delay) at initialization

3. **Potential level adjustments:**
   - schedule_fetcher.py line 124: "Error parsing event" is DEBUG - should this be WARNING?
   - game_data_fetcher.py line 346: "No coordinates, skipping weather" is DEBUG - should this be INFO?

4. **Missing parameter logging:**
   - Some functions don't log entry parameters (e.g., year, output_dir values)
   - Player count in loops could use throttled logging (every 100 players)

**Overall Assessment:**
- **Current quality: GOOD** - Most logs follow INFO/DEBUG criteria from Discovery
- **Improvement opportunity: MEDIUM** - ~10-15 additions/adjustments recommended
- **Priority: MEDIUM** - Not critical, but would improve debugging experience

---

## Test Impact Analysis

### Test Files with Logging Assertions

Found 3 test files with logging assertions:

1. **tests/historical_data_compiler/test_weekly_snapshot_generator.py**
   - Uses caplog or mock logging
   - May assert on specific log messages

2. **tests/historical_data_compiler/test_game_data_fetcher.py**
   - Uses caplog or mock logging
   - May assert on specific log messages

3. **tests/historical_data_compiler/test_team_data_calculator.py**
   - Uses caplog or mock logging
   - May assert on specific log messages

**Impact:**
- If log messages change (wording, level, added/removed), test assertions may fail
- Need to update assertions to match new log messages
- Tests may verify log call count - changes to logging could break these

**Strategy:**
- Review each test file during implementation
- Update assertions to match modified log messages
- Ensure 100% test pass rate before commit (mandatory per workflow)

---

## Integration Points

### Feature 01 (core_logging_infrastructure) - DEPENDENCY

**What Feature 01 Provides:**
- `LineBasedRotatingHandler` class (500-line rotation, 50-file cleanup)
- Modified `setup_logger()` API accepting `log_to_file` parameter
- Centralized `logs/{script_name}/` folder structure
- Timestamped filenames: `historical_data_compiler-{YYYYMMDD_HHMMSS}.log`

**Integration Contracts (from Feature 01 spec):**
1. **Logger name = folder name:** Use consistent name `"historical_data_compiler"`
   - ✅ VERIFIED: compile_historical_data.py line 260 uses `"historical_data_compiler"`
2. **log_file_path=None:** Don't specify custom paths (let LoggingManager auto-generate)
   - ✅ PLAN: Will pass `log_file_path=None` in modified setup_logger call
3. **log_to_file driven by CLI:** Wire `--enable-log-file` flag to `log_to_file` parameter
   - ✅ PLAN: Will add `--enable-log-file` flag and pass to setup_logger

**Expected Behavior After Integration:**
```bash
# User runs with --enable-log-file flag:
python compile_historical_data.py --year 2024 --enable-log-file

# Logs written to:
logs/historical_data_compiler/historical_data_compiler-20260206_143522.log

# Log rotation:
# - Rotates at 500 lines
# - Max 50 files in logs/historical_data_compiler/
# - Oldest files auto-deleted
```

---

## Scope Summary

### In Scope

1. **CLI Integration:**
   - Add `--enable-log-file` flag to compile_historical_data.py
   - Modify `setup_logger()` call to pass `log_to_file` parameter
   - Default: file logging OFF (per Discovery Q4)

2. **Log Quality Review:**
   - Review all ~69 logger calls in compile_historical_data.py and modules
   - Apply DEBUG/INFO criteria from Discovery Iteration 3
   - Add ~10-15 improvements (new logs, level adjustments, parameter logging)

3. **Test Updates:**
   - Update logging assertions in 3 test files
   - Ensure 100% test pass rate

### Out of Scope

- Changing logger name (already correct: `"historical_data_compiler"`)
- Custom log file paths (using Feature 01 auto-generation)
- Console logging changes (only affects file logging)
- Log format changes (keeping existing formats)
- LineBasedRotatingHandler implementation (Feature 01 responsibility)

---

## Open Questions

{To be populated during checklist resolution - S2.P1.I2}

None yet - may identify questions during spec drafting.

---

## Code Locations

**Primary Files:**
- `compile_historical_data.py` (lines 66-96 args, line 260 setup_logger)

**Secondary Files (log quality):**
- `historical_data_compiler/http_client.py`
- `historical_data_compiler/player_data_fetcher.py`
- `historical_data_compiler/json_exporter.py`
- `historical_data_compiler/weekly_snapshot_generator.py`
- `historical_data_compiler/team_data_calculator.py`
- `historical_data_compiler/game_data_fetcher.py`
- `historical_data_compiler/schedule_fetcher.py`

**Test Files:**
- `tests/historical_data_compiler/test_weekly_snapshot_generator.py`
- `tests/historical_data_compiler/test_game_data_fetcher.py`
- `tests/historical_data_compiler/test_team_data_calculator.py`

---

**Research Complete:** Ready to draft spec.md
