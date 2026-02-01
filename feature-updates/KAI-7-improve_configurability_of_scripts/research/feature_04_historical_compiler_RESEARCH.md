# Feature 04: Historical Compiler - Research Findings

**Feature:** feature_04_historical_compiler
**Researched:** 2026-01-29
**Researcher:** Secondary-C

---

## Discovery Context Summary

From DISCOVERY.md lines 303-322:

**Purpose:** Enhance historical compiler with debug/E2E modes and additional args

**Scope:**
- Enhance argparse (add --debug, --e2e-test, --timeout, --rate-limit-delay, --log-level)
- Add debug mode (DEBUG logging + single week compilation)
- Add E2E test mode (compile minimal dataset, ≤3 min)
- Unit tests for argument handling

**Recommended Approach:** Script-specific args from constants.py (User Answer Q1)

**Key Design Decisions:**
- E2E mode: compile minimal dataset with limited data
- Debug mode: DEBUG logging + behavioral changes (single week)
- Integration tests: validate exit code AND specific outcomes

---

## Components Researched

### 1. Main Runner Script (compile_historical_data.py)

**File:** `compile_historical_data.py` (312 lines)
**Lines Examined:** 1-312

**Current Argparse Structure (lines 59-96):**
```python
parser.add_argument("--year", type=int, required=False,
                    help=f"NFL season year to compile (>= {MIN_SUPPORTED_YEAR})")
parser.add_argument("--verbose", "-v", action="store_true",
                    help="Enable verbose logging")
parser.add_argument("--output-dir", type=Path, default=None,
                    help="Override output directory (default: simulation/sim_data/{YEAR})")
```

**Key Findings:**
- **Already has argparse** (lines 66-96) - ahead of player/schedule/league_helper
- 3 existing arguments: --year, --verbose, --output-dir
- Verbose flag controls log level: DEBUG if verbose, else INFO (line 259)
- If no year provided, iterates through YEARS array [2021-2025] (lines 56, 269)
- Default output: `simulation/sim_data/{YEAR}/` (line 278)
- Error handling with cleanup_on_error() on failure (lines 152-162, 301-306)

**Main Compilation Workflow (lines 165-220):**
1. Phase 1: Fetch schedule data (await fetch_and_write_schedule)
2. Phase 2: Fetch game data with weather (await fetch_and_write_game_data)
3. Phase 3: Fetch player data (await fetch_player_data)
4. Phase 4: Calculate team data (calculate_and_write_team_data)
5. Phase 5: Generate weekly snapshots (generate_weekly_snapshots)

**Actual Method Signatures:**
- `parse_args() -> argparse.Namespace` (line 59)
- `validate_year(year: int) -> None` (line 99)
- `create_output_directories(output_dir: Path) -> None` (line 116)
- `async compile_season_data(year: int, output_dir: Path) -> None` (line 165)
- `main() -> int` (line 249)

---

### 2. Constants Module (historical_data_compiler/constants.py)

**File:** `historical_data_compiler/constants.py` (157 lines)
**Lines Examined:** 1-157

**The 4 Configurable Constants (from Discovery Iteration 2):**

| Constant | Line | Type | Default Value | Purpose |
|----------|------|------|---------------|---------|
| MIN_SUPPORTED_YEAR | 85 | int | 2021 | Minimum year for weekly data availability |
| REGULAR_SEASON_WEEKS | 88 | int | 17 | Number of regular season weeks to process |
| REQUEST_TIMEOUT | 98 | float | 30.0 | HTTP request timeout in seconds |
| RATE_LIMIT_DELAY | 101 | float | 0.3 | Delay between API requests in seconds |

**Additional Constants (potentially configurable):**
- MAX_RETRY_ATTEMPTS = 3 (line 104) - HTTP retry attempts
- VALIDATION_WEEKS = 18 (line 91) - Includes week 18 for validation

**Output Format Toggles (in compile_historical_data.py):**
- GENERATE_CSV = False (line 53) - Legacy CSV output
- GENERATE_JSON = True (line 54) - New JSON output

---

### 3. HTTP Client Module (historical_data_compiler/http_client.py)

**File:** `historical_data_compiler/http_client.py`
**Lines Examined:** 1-100

**BaseHTTPClient Constructor (lines 62-78):**
```python
def __init__(
    self,
    timeout: float = REQUEST_TIMEOUT,
    rate_limit_delay: float = RATE_LIMIT_DELAY,
    user_agent: str = ESPN_USER_AGENT
):
    self.timeout = timeout
    self.rate_limit_delay = rate_limit_delay
    self.user_agent = user_agent
```

**Key Finding:**
- **Already accepts timeout and rate_limit_delay as constructor params**
- Default values come from constants (lines 64-65)
- To make configurable via CLI: pass args to BaseHTTPClient() constructor
- HTTP client instantiated in compile_season_data() (line 183)

**Implementation Approach:**
```python
# Current (line 183):
http_client = BaseHTTPClient()

# Enhanced with CLI args:
http_client = BaseHTTPClient(
    timeout=args.timeout,
    rate_limit_delay=args.rate_limit_delay
)
```

---

### 4. Test Structure

**Test Directory:** `tests/historical_data_compiler/`

**Existing Test Files:**
1. `test_constants.py` (6105 bytes) - Constants validation
2. `test_game_data_fetcher.py` (8097 bytes) - Game data fetching tests
3. `test_json_exporter.py` (13063 bytes) - JSON export tests
4. `test_player_data_fetcher.py` (4251 bytes) - Player data fetching tests
5. `test_team_data_calculator.py` (6617 bytes) - Team data calculation tests
6. `test_weekly_snapshot_generator.py` (20478 bytes) - Weekly snapshot tests

**Test Pattern:** Unit tests for individual modules (no integration tests yet)

**Missing:** Integration test for compile_historical_data.py main script

---

## Implementation Approach for This Feature

### 1. Enhance Argparse (compile_historical_data.py)

**Add 5 new arguments:**

| Argument | Type | Default | Help Text |
|----------|------|---------|-----------|
| --debug | flag | False | Enable debug mode (DEBUG logging + single week compilation) |
| --e2e-test | flag | False | Run E2E test mode (minimal dataset, ≤3 min) |
| --timeout | float | 30.0 | HTTP request timeout in seconds |
| --rate-limit-delay | float | 0.3 | Delay between API requests in seconds |
| --log-level | str | "INFO" | Logging level (DEBUG/INFO/WARNING/ERROR) |

**Notes:**
- --verbose flag becomes deprecated (use --log-level DEBUG instead)
- Or keep --verbose as shorthand for --log-level DEBUG

### 2. Add Debug Mode Behavioral Changes

**Debug mode (--debug flag) should:**
- Set log level to DEBUG
- **Limit compilation to single week** (week 1 only)
- **Use single year** (first year in YEARS array or --year arg)
- Enable verbose API logging
- Skip cleanup on error (preserve partial output for debugging)

**Implementation location:** main() function (lines 249-307)

```python
if args.debug:
    # Debug behavioral changes
    weeks_to_compile = [1]  # Single week only
    year_array = [year_array[0]]  # Single year only
    # Don't cleanup on error in debug mode
```

### 3. Add E2E Test Mode

**E2E mode (--e2e-test flag) should:**
- **Compile minimal dataset**: Single year (2024), weeks 1-2 only
- **Use faster timeouts**: REQUEST_TIMEOUT = 10.0 (vs 30.0)
- **Use faster rate limit**: RATE_LIMIT_DELAY = 0.1 (vs 0.3)
- **Target runtime:** ≤3 minutes
- **Generate JSON only** (skip CSV generation)

**Implementation location:** main() function

```python
if args.e2e_test:
    year_array = [2024]  # Fixed year for E2E
    weeks_to_compile = [1, 2]  # Weeks 1-2 only
    http_client = BaseHTTPClient(timeout=10.0, rate_limit_delay=0.1)
```

### 4. Pass Arguments to HTTP Client

**Modification needed in compile_season_data() (line 183):**

```python
# Current:
http_client = BaseHTTPClient()

# Enhanced:
http_client = BaseHTTPClient(
    timeout=timeout,
    rate_limit_delay=rate_limit_delay
)
```

**Function signature change:**
```python
async def compile_season_data(
    year: int,
    output_dir: Path,
    timeout: float = REQUEST_TIMEOUT,
    rate_limit_delay: float = RATE_LIMIT_DELAY
) -> None:
```

### 5. Add Unit Tests

**New test file:** `tests/test_compile_historical_data_args.py`

**Test cases:**
1. Test argparse with all new arguments
2. Test debug mode limits to single week/year
3. Test E2E mode uses fast timeouts
4. Test timeout/rate-limit args passed to HTTP client
5. Test log level configuration
6. Test backward compatibility with --verbose flag

---

## E2E Mode Design

**Goal:** Complete compilation in ≤3 minutes

**Strategy:**
- **Single year:** 2024 (most recent complete season)
- **Limited weeks:** Weeks 1-2 only (instead of 1-17)
- **Faster HTTP settings:** timeout=10s, rate_limit_delay=0.1s
- **JSON only:** Skip legacy CSV generation
- **No retry delays:** Fail fast on errors

**Expected Data Volume:**
- Schedule: ~16 games per week × 2 weeks = 32 games
- Player data: ~2,000 players × 2 weeks
- Team data: 32 teams
- Output: ~2-3 MB total

**Runtime Estimate:**
- Schedule fetch: ~5 seconds
- Game data fetch: ~10 seconds
- Player data fetch: ~60 seconds (30s per week)
- Team data calc: ~5 seconds
- Weekly snapshots: ~30 seconds
- **Total: ~110 seconds (1.8 minutes)** ✅ Under 3-minute target

---

## Debug Mode Design

**Goal:** Help developers debug compilation issues

**Behavioral Changes:**
- **Single week:** Week 1 only (vs weeks 1-17)
- **Single year:** First year in array or --year arg
- **DEBUG logging:** Full API request/response logging
- **Preserve partial output:** Don't cleanup on error (for inspection)
- **Verbose progress:** Log each API call and data transformation

**Use Case:**
```bash
python compile_historical_data.py --year 2024 --debug
```

**Expected Output:**
- DEBUG logs for HTTP requests
- Single week compilation only
- Partial data preserved on failure
- Runtime: ~30 seconds (vs ~10 minutes for full compilation)

---

## Existing Test Patterns

**From test_json_exporter.py (largest test file):**
- Uses pytest framework
- Mock data fixtures for testing
- Tests for data validation and export logic
- File I/O tests with temporary directories

**Pattern to Follow:**
```python
import pytest
from pathlib import Path
from compile_historical_data import parse_args

def test_argparse_debug_flag():
    args = parse_args(['--debug'])
    assert args.debug is True

def test_argparse_timeout():
    args = parse_args(['--timeout', '15.0'])
    assert args.timeout == 15.0
```

---

## Edge Cases Identified

1. **Invalid timeout value:** Should validate timeout > 0
2. **Invalid rate limit delay:** Should validate delay >= 0
3. **Debug + E2E conflict:** Both flags set - which takes precedence?
   - **Resolution:** E2E mode overrides debug mode settings
4. **Year validation with E2E:** E2E should ignore --year arg (always use 2024)
5. **Output directory with E2E:** Should append "_e2e" suffix to avoid overwriting prod data

---

## Research Completeness

**Components researched:**
- [x] Main runner script (compile_historical_data.py)
- [x] Constants module (constants.py)
- [x] HTTP client module (http_client.py)
- [x] Test structure (tests/historical_data_compiler/)

**Evidence collected:**
- [x] File paths with line numbers
- [x] Actual method signatures
- [x] Constant data types and default values
- [x] Current argparse structure
- [x] HTTP client constructor signature

**Implementation approach defined:**
- [x] Argparse enhancements (5 new args)
- [x] Debug mode behavioral changes
- [x] E2E mode design (runtime target: 1.8 minutes)
- [x] HTTP client parameter passing
- [x] Test strategy

**Ready for Phase 1.5 audit:** YES

---

**End of Research Document**
