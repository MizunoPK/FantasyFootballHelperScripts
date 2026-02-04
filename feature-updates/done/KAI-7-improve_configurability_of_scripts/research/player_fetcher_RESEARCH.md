# Feature 01: Player Fetcher - Research Findings

**Feature:** player_fetcher
**Research Date:** 2026-01-29
**Researcher:** Primary Agent (S2.P1 Research Phase)

---

## Research Goal

Understand player fetcher implementation to determine:
1. What arguments should be added (from config.py constants)
2. How debug mode should behave
3. How E2E test mode should work
4. Current structure and patterns to follow

---

## Component Research

### 1. Current Runner Script Structure

**File:** `run_player_fetcher.py` (52 lines)
**Current Implementation:**
- Simple subprocess wrapper
- No argparse (needs to be added)
- Changes to player-data-fetcher/ directory
- Calls player_data_fetcher_main.py directly
- No argument passing

**Key Code:**
```python
# Lines 36-39
result = subprocess.run([
    sys.executable,
    "player_data_fetcher_main.py"
], check=True)
```

**Findings:**
- Needs complete argparse implementation
- Pattern available in run_game_data_fetcher.py:56-84
- Will need to parse args and pass to underlying fetcher

---

### 2. Configuration Constants (config.py)

**File:** `player-data-fetcher/config.py` (90 lines)

**Frequently Modified Constants (candidates for CLI arguments):**

| Constant | Type | Default | Line | Purpose |
|----------|------|---------|------|---------|
| `CURRENT_NFL_WEEK` | int | 17 | 13 | Current NFL week (1-18) |
| `NFL_SEASON` | int | 2025 | 14 | Current NFL season year |
| `PRESERVE_LOCKED_VALUES` | bool | False | 17 | Keep locked players between updates |
| `LOAD_DRAFTED_DATA_FROM_FILE` | bool | True | 20 | Load drafted state from CSV |
| `DRAFTED_DATA` | str | "../data/drafted_data.csv" | 21 | Path to drafted player CSV |
| `MY_TEAM_NAME` | str | "Sea Sharp" | 22 | Fantasy team name |
| `OUTPUT_DIRECTORY` | str | "./data" | 25 | Output folder |
| `CREATE_CSV` | bool | True | 26 | Generate CSV output |
| `CREATE_JSON` | bool | False | 27 | Generate JSON output |
| `CREATE_EXCEL` | bool | False | 28 | Generate Excel output |
| `CREATE_CONDENSED_EXCEL` | bool | False | 29 | Generate condensed Excel |
| `CREATE_POSITION_JSON` | bool | True | 30 | Generate position-based JSON files |
| `POSITION_JSON_OUTPUT` | str | "../data/player_data" | 34 | Position JSON output folder |
| `TEAM_DATA_FOLDER` | str | '../data/team_data' | 37 | Per-team historical data folder |
| `GAME_DATA_CSV` | str | '../data/game_data.csv' | 38 | Game data output file |
| `ENABLE_HISTORICAL_DATA_SAVE` | bool | False | 42 | Auto-save weekly snapshots |
| `ENABLE_GAME_DATA_FETCH` | bool | True | 45 | Fetch game data during collection |
| `LOGGING_LEVEL` | str | 'INFO' | 51 | Log level |
| `LOGGING_TO_FILE` | bool | False | 52 | Console vs file logging |
| `LOGGING_FILE` | str | './data/log.txt' | 54 | Log file path |
| `PROGRESS_UPDATE_FREQUENCY` | int | 10 | 58 | Progress every N players |

**Total:** 21 configurable constants identified

---

### 3. Main Script Structure

**File:** `player-data-fetcher/player_data_fetcher_main.py`

**Entry Point:** Line 537 - `async def main()`

**Current Flow:**
1. Setup logger from config (line 540)
2. Load Settings() object from config (line 546)
3. Create NFLProjectionsCollector (line 550)
4. Collect projection data (line 551)
5. Export data (line 558)
6. Optionally fetch game data if `ENABLE_GAME_DATA_FETCH` (line 562)
7. Optionally save historical data if `ENABLE_HISTORICAL_DATA_SAVE` (line 573)
8. Print summary (line 585)

**Key Finding:**
- Settings class uses pydantic BaseSettings (line 42)
- Loads from config.py constants
- No current argument override mechanism
- Will need to modify Settings instantiation to accept overrides

---

### 4. Reference Pattern (run_game_data_fetcher.py)

**File:** `run_game_data_fetcher.py` (174 lines)

**Argparse Pattern (lines 56-84):**
```python
parser = argparse.ArgumentParser(
    description="Fetch NFL game data..."
)
parser.add_argument('--season', type=int, default=None, help='...')
parser.add_argument('--output', type=str, default=None, help='...')
parser.add_argument('--weeks', type=str, default=None, help='...')
parser.add_argument('--current-week', type=int, default=None, help='...')
args = parser.parse_args()
```

**Argument Handling (lines 112-124):**
```python
# Use args if provided, else fall back to config
season = args.season if args.season else NFL_SEASON
current_week = args.current_week if args.current_week else CURRENT_NFL_WEEK

# Construct output path from args or default
if args.output:
    output_path = script_dir / args.output
else:
    output_path = script_dir / "data" / "game_data.csv"
```

**Pattern Found:** Args override config defaults

---

## Pattern Research

### Argparse Implementation Pattern

Based on run_game_data_fetcher.py analysis:

1. **Add main() function to runner script**
2. **Create ArgumentParser with description**
3. **Add arguments for each config constant**
   - Use `default=None` to distinguish "not provided" vs explicit value
   - Use appropriate types (int, str, bool)
   - Add help text describing each argument
4. **Parse arguments:** `args = parser.parse_args()`
5. **Override config with args:** `value = args.value if args.value else CONFIG_VALUE`
6. **Pass overrides to underlying fetcher**

### Boolean Argument Pattern

For boolean flags like `--debug`, `--e2e-test`, `--create-csv`:
- Use `action='store_true'` for flags that enable features
- Use `action='store_false'` for flags that disable features
- Default to `None` to detect if user provided flag

---

## Data Research

### E2E Test Mode Requirements (from Discovery Q3)

**User Answer:** Fetchers use real APIs with data limiting

**E2E Mode for Player Fetcher:**
- Use real ESPN API (no mocking)
- Limit data fetch to reduce time
- Target: ≤3 minutes

**Possible E2E Data Limiting Strategies:**
1. Fetch only specific positions (e.g., QB only)
2. Limit player count via ESPN_PLAYER_LIMIT (line 68: default 2000)
3. Skip optional features (game data fetch, historical save)
4. Reduce progress update frequency

**Recommended E2E Behavior:**
- Set `ESPN_PLAYER_LIMIT = 50` (vs 2000 default)
- Set `ENABLE_GAME_DATA_FETCH = False`
- Set `ENABLE_HISTORICAL_DATA_SAVE = False`
- Set `CREATE_EXCEL = False` (only CSV for speed)
- Keep real API calls (as per Discovery Q3 answer)

---

### Debug Mode Requirements (from Discovery Q4)

**User Answer:** Option C - Both logging AND behavioral changes

**Debug Mode for Player Fetcher:**

**Logging Changes:**
- Set `LOGGING_LEVEL = 'DEBUG'`
- Enable verbose output
- Show detailed API responses

**Behavioral Changes:**
- Reduce player limit for faster execution
- Skip optional expensive operations
- Enable progress tracking with high frequency

**Recommended Debug Behavior:**
- Set `LOGGING_LEVEL = 'DEBUG'`
- Set `ESPN_PLAYER_LIMIT = 100` (vs 2000 default)
- Set `PROGRESS_UPDATE_FREQUENCY = 5` (vs 10 default)
- Set `ENABLE_GAME_DATA_FETCH = False` (skip expensive operation)
- Set `ENABLE_HISTORICAL_DATA_SAVE = False` (skip file I/O)

---

## Discovery Context Verification

### From DISCOVERY.md Feature 01 Scope

**Expected Arguments (Discovery basis):**
- 13+ arguments from config.py constants ✅ (21 constants identified)
- --debug flag (debug mode) ✅ (behavior defined above)
- --e2e-test flag (E2E mode) ✅ (behavior defined above)
- --week (CURRENT_NFL_WEEK) ✅ (line 13 in config.py)
- --season (NFL_SEASON) ✅ (line 14 in config.py)
- --output-dir (OUTPUT_DIRECTORY) ✅ (line 25 in config.py)
- --create-csv/json/excel ✅ (lines 26-29 in config.py)
- --log-level (LOGGING_LEVEL) ✅ (line 51 in config.py)

**Discovery validation:** All expected arguments found in config.py

---

## Integration Points

### 1. run_player_fetcher.py → player_data_fetcher_main.py

**Current:** Direct subprocess call, no args
**Needed:** Pass parsed args to main()

**Options:**
A. Modify player_data_fetcher_main.py main() to accept kwargs
B. Set environment variables before subprocess call
C. Modify config.py values directly before import

**Recommendation:** Option C (least invasive)
- Override config.py module-level constants from runner
- Import player_data_fetcher_main after setting overrides
- Pattern used in run_game_data_fetcher.py (lines 105-106)

### 2. Settings Class Integration

**Current:** Settings() loads from config.py constants (line 546)
**Needed:** Override with CLI args

**Implementation:**
```python
# In run_player_fetcher.py after parsing args
import player_data_fetcher_main
import config

# Override config constants with args
if args.week:
    config.CURRENT_NFL_WEEK = args.week
if args.season:
    config.NFL_SEASON = args.season
# ... etc

# Then import and run main (config overrides will be picked up)
import asyncio
asyncio.run(player_data_fetcher_main.main())
```

---

## Research Completeness Evidence

### Component Understanding ✅

**Evidence:**
- run_player_fetcher.py: 52 lines, subprocess wrapper (lines 36-39)
- config.py: 21 configurable constants identified (lines 13-58)
- player_data_fetcher_main.py: main() at line 537, Settings at line 42
- run_game_data_fetcher.py: argparse pattern lines 56-84

### Pattern Understanding ✅

**Evidence:**
- Argparse pattern found in run_game_data_fetcher.py
- Config override pattern: lines 112-124
- Boolean flag pattern: action='store_true'
- Main() wrapper pattern documented

### Data Requirements ✅

**Evidence:**
- E2E mode: ESPN_PLAYER_LIMIT=50, skip game/historical data
- Debug mode: LOGGING_LEVEL='DEBUG', ESPN_PLAYER_LIMIT=100
- Both modes defined with specific config overrides

### Discovery Alignment ✅

**Evidence:**
- 13+ arguments requirement met (21 identified)
- Debug behavior matches Discovery Q4 answer (logging + behavioral)
- E2E behavior matches Discovery Q3 answer (real API + limiting)
- All Discovery-specified arguments found in config.py

---

## Open Questions for Checklist

1. **Argument Naming Convention:** Should we use `--week` or `--current-week`? (Game fetcher uses `--current-week`)

2. **E2E Player Limit:** Is 50 players adequate for E2E testing, or should it be higher/lower?

3. **Debug vs E2E Overlap:** Should `--debug` and `--e2e-test` be mutually exclusive, or can both be used together?

4. **Output Format Defaults in E2E/Debug:** Should these modes force specific output formats, or respect existing config?

5. **Logging in E2E Mode:** Should E2E mode also enable DEBUG logging, or keep at INFO level?

6. **Historical Data Flag:** Should there be a `--no-historical-save` flag to explicitly disable, or only enable via `--enable-historical-save`?

---

## Next Steps

1. Complete S2.P1 Phase 1.5 (Research Completeness Audit)
2. Proceed to S2.P2 (Specification Phase)
3. Create spec.md with detailed argument specifications
4. Create checklist.md with the 6 open questions above

---

**Research Status:** COMPLETE
**Gate 1 (Research Completeness Audit):** Ready for evaluation
