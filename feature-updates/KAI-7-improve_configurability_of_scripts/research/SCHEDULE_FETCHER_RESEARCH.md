# Feature 02 Research: schedule_fetcher Configurability

**Feature:** feature_02_schedule_fetcher
**Researcher:** Secondary-A
**Research Date:** 2026-01-29
**Phase:** S2.P1 - Feature-Specific Research

---

## Discovery Context Summary

From `../DISCOVERY.md` Feature 02 section:

**Purpose:** Add argparse and debug/E2E modes to schedule data fetcher

**Scope:**
- Add argparse with arguments (--season, --output-path, --debug, --e2e-test, --log-level)
- Add debug mode (DEBUG logging)
- Add E2E test mode (fetch single week schedule, ≤3 min)
- Unit tests

**Dependencies:** None (benefits from Feature 01 patterns)

**Discovery Basis:**
- Finding: schedule-data-fetcher has no config file (Iteration 2)
- User Answer Q1: Script-specific args from constants
- User Answer Q3: Fetchers use real APIs with data limiting
- User Answer Q4: Debug mode = behavioral changes + DEBUG logging

---

## Components Researched

### Component 1: run_schedule_fetcher.py

**File:** `run_schedule_fetcher.py` (65 lines)
**Lines:** 1-65
**Purpose:** Runner script for schedule data fetcher

**Current Implementation:**
- **No argparse currently** - hardcoded configuration
- **Hardcoded season:** `NFL_SEASON = 2025` (line 25)
- **Hardcoded output path:** `Path(__file__).parent / "data" / "season_schedule.csv"` (line 32)
- **Async execution:** Uses `asyncio.run(main())` (line 63)
- **Exit code:** Returns 0 on success, 1 on failure (lines 53, 59)
- **Error handling:** Try/except with traceback on exception (lines 55-59)

**Method Signatures:**
```python
async def main():  # Lines 28-59
    # No parameters currently
    # Returns int exit code (0 or 1)
```

**Configurable Elements Identified:**
1. `NFL_SEASON` (line 25) → should become `--season` argument
2. `output_path` (line 32) → should become `--output-path` argument
3. No log level configuration → should become `--log-level` argument

---

### Component 2: ScheduleFetcher Class

**File:** `schedule-data-fetcher/ScheduleFetcher.py` (241 lines)
**Lines:** 19-241
**Purpose:** Core schedule fetching and export logic

**Class Signature:**
```python
class ScheduleFetcher:
    def __init__(self, output_path: Path):
        # Lines 27-36
        self.output_path = output_path
        self.logger = setup_logger(name="ScheduleFetcher", level="INFO")  # Line 35 - hardcoded INFO
        self.client: Optional[httpx.AsyncClient] = None
```

**Key Methods:**
```python
async def fetch_full_schedule(self, season: int) -> Dict[int, Dict[str, str]]:
    # Lines 76-156
    # Fetches weeks 1-18 from ESPN API
    # Rate limiting: 0.2 sec between requests (line 144)
    # Returns: {week_number: {team: opponent}}

def export_to_csv(self, schedule: Dict[int, Dict[str, str]]):
    # Lines 190-240
    # Exports to CSV with bye weeks
    # Creates parent directory if missing (line 208)
```

**Current Behavior:**
- **Weeks fetched:** Hardcoded weeks 1-18 (line 93)
- **Log level:** Hardcoded "INFO" in __init__ (line 35)
- **Rate limiting:** 0.2 seconds between week requests (line 144)
- **HTTP timeout:** 30.0 seconds (line 41)
- **Team normalization:** WAS → WSH (lines 130-131)

**Configurable Elements Identified:**
1. Log level in __init__ (line 35) - needs parameter
2. Weeks range (lines 93, 179, 215) - currently 1-18, could be configurable for E2E
3. Rate limit delay (line 144) - currently 0.2s, could be configurable for debug

---

### Component 3: LoggingManager Integration

**File:** `utils/LoggingManager.py` (lines 1-50 examined)
**Lines:** 20-50
**Purpose:** Centralized logging configuration

**setup_logger Signature:**
```python
def setup_logger(
    name: str,
    level: Union[str, int] = 'INFO',  # Line 47 - supports level parameter
    log_to_file: bool = False,
    log_file_path: Optional[Union[str, Path]] = None,
    log_format: str = 'standard',
```

**Supported Log Levels:**
- DEBUG, INFO, WARNING, ERROR, CRITICAL (lines 34-40 in LEVEL_MAP)

**Current Usage in ScheduleFetcher:**
- `setup_logger(name="ScheduleFetcher", level="INFO")` (ScheduleFetcher.py:35)
- **Needs to accept level parameter from arguments**

---

## Existing Test Patterns

**Test File Found:** `tests/simulation/test_scheduler.py`
- May not be related to schedule fetcher (likely simulation scheduler)
- Need to create new test file: `tests/root_scripts/test_run_schedule_fetcher.py`

**Integration Test Pattern:**
- Location: `tests/integration/`
- Existing examples: `test_accuracy_simulation_integration.py`
- Pattern: Test multiple argument combinations, validate exit codes and outcomes

---

## Interface Dependencies

**External Dependencies:**
1. **ESPN API:**
   - URL: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
   - Parameters: seasontype=2, week=N, dates=YYYY
   - Response: JSON with events/competitions/competitors structure
   - **Used by:** `fetch_full_schedule()` (ScheduleFetcher.py:97)

2. **httpx AsyncClient:**
   - Async HTTP client for API requests
   - Timeout: 30.0 seconds (ScheduleFetcher.py:41)
   - **Used by:** All API requests via `_make_request()` (ScheduleFetcher.py:49-74)

3. **LoggingManager:**
   - Provides `setup_logger()` function
   - **Used by:** ScheduleFetcher.__init__ (ScheduleFetcher.py:35)

---

## Edge Cases Identified

### Edge Case 1: Team Name Normalization
**Code:** ScheduleFetcher.py lines 130-131
```python
team1 = 'WSH' if team1 == 'WAS' else team1
team2 = 'WSH' if team2 == 'WAS' else team2
```
**Impact:** ESPN uses "WAS" for Washington, but system uses "WSH"
**Requirement:** Must preserve this normalization in any refactoring

### Edge Case 2: Bye Week Detection
**Code:** ScheduleFetcher.py lines 158-188 (_identify_bye_weeks)
**Logic:** Teams not in week's schedule have a bye
**Impact:** CSV export includes bye weeks (empty opponent)
**Requirement:** E2E mode must still handle bye weeks correctly (even with single week)

### Edge Case 3: Week 18 Handling
**Code:** ScheduleFetcher.py line 93 (weeks 1-18), but bye detection is 1-17 (line 179)
**Logic:** Week 18 is typically playoffs, not included in bye detection
**Impact:** Ensure E2E mode week selection doesn't cause issues (week 1 is safe)

### Edge Case 4: API Rate Limiting
**Code:** ScheduleFetcher.py line 144 (asyncio.sleep(0.2))
**Logic:** 0.2 second delay between week requests
**Impact:** E2E mode with single week won't need rate limiting, but code structure should support it

---

## Implementation Approach for This Feature

### Required Changes to run_schedule_fetcher.py

**Add argparse with arguments:**
1. `--season` (int, default: 2025) - NFL season year
2. `--output-path` (str, default: "data/season_schedule.csv") - Output CSV path
3. `--log-level` (str, default: "INFO", choices: DEBUG/INFO/WARNING/ERROR/CRITICAL) - Logging level
4. `--debug` (flag) - Enable debug mode (DEBUG logging + verbose output)
5. `--e2e-test` (flag) - Enable E2E test mode (single week fetch)

**Argparse pattern to follow:**
- Based on `run_game_data_fetcher.py` (lines 56-80)
- Use ArgumentParser with description
- Parse args in main(), pass to fetcher

**Debug mode behavioral changes:**
1. Set log level to DEBUG (override --log-level)
2. Print verbose output (each week's schedule details)
3. Reduce weeks fetched to 1-2 (for faster debugging)

**E2E test mode behavioral changes:**
1. Fetch only week 1 (instead of weeks 1-18)
2. Use real ESPN API (per Discovery User Answer Q3)
3. Verify basic schedule structure (at least some games in week 1)
4. Should complete in <1 minute (well under 3 min limit)

### Required Changes to ScheduleFetcher class

**Modify __init__ signature:**
```python
def __init__(self, output_path: Path, log_level: str = "INFO"):
    self.output_path = output_path
    self.logger = setup_logger(name="ScheduleFetcher", level=log_level)  # Use parameter
    self.client: Optional[httpx.AsyncClient] = None
```

**Add method for E2E mode:**
```python
async def fetch_week_schedule(self, season: int, week: int) -> Dict[int, Dict[str, str]]:
    # Fetch single week instead of full 1-18 range
    # Return: {week: {team: opponent}}
```

OR

**Modify fetch_full_schedule to accept weeks parameter:**
```python
async def fetch_full_schedule(self, season: int, weeks: range = range(1, 19)) -> Dict[int, Dict[str, str]]:
    # Use weeks parameter instead of hardcoded range(1, 19)
```

---

## Research Completeness

**Files Read:** 4
- run_schedule_fetcher.py (65 lines)
- schedule-data-fetcher/ScheduleFetcher.py (241 lines)
- run_game_data_fetcher.py (first 80 lines - argparse pattern)
- utils/LoggingManager.py (first 50 lines - setup_logger signature)

**Code Snippets Collected:** 7
- ScheduleFetcher.__init__ signature (line 27-36)
- fetch_full_schedule signature and loop (lines 76-93)
- setup_logger signature (LoggingManager.py:45-50)
- run_game_data_fetcher argparse pattern (lines 56-80)
- Team normalization logic (lines 130-131)
- Bye week detection range (line 179)
- Rate limiting (line 144)

**Components Identified:** 3
- run_schedule_fetcher.py (runner script)
- ScheduleFetcher class (core logic)
- LoggingManager (logging infrastructure)

**Interfaces Mapped:** 3
- ESPN API endpoint and parameters
- httpx AsyncClient usage
- LoggingManager.setup_logger()

**Edge Cases Documented:** 4
- Team name normalization (WAS → WSH)
- Bye week detection (weeks 1-17)
- Week 18 handling (playoffs)
- API rate limiting

---

## Next Steps (for S2.P2 Specification Phase)

1. Create detailed spec.md sections:
   - Requirements (based on Discovery + research findings)
   - Argument specifications (5 arguments documented above)
   - Debug mode behavior (specific changes listed)
   - E2E mode behavior (single week fetch details)
   - ScheduleFetcher class interface changes

2. Create checklist.md questions for user:
   - Q1: Should --season default to current year (2025) or configurable in constants?
   - Q2: Should E2E mode fetch week 1 specifically, or allow --e2e-week arg?
   - Q3: Should debug mode reduce to 1-2 weeks or allow --debug-weeks arg?
   - Q4: Should rate limit delay be configurable via --rate-limit argument?
   - Q5: Should output-path default to "data/season_schedule.csv" or allow per-season naming?

3. Verify traceability:
   - All requirements trace to Discovery or code analysis
   - No assumptions without user confirmation
   - Questions for uncertain items go in checklist.md

---

**Research Phase Complete:** Ready for S2.P2 (Specification Phase)
