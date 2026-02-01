# Feature 03 Research: Game Data Fetcher Enhancement

**Feature:** feature_03_game_data_fetcher
**Researched:** 2026-01-29
**Researcher:** Secondary-B

---

## Discovery Context Summary

**From DISCOVERY.md (lines 282-300):**

- **Purpose:** Enhance existing argparse with debug/E2E modes
- **Key Discovery Findings:**
  - `run_game_data_fetcher.py` already has argparse with --season, --output, --weeks (Discovery Iteration 1, line 50)
  - User Answer Q3: Fetchers use real APIs with data limiting
  - User Answer Q4: Debug = behavioral changes + DEBUG logging
- **Approach:** Add 3 universal flags (--debug, --e2e-test, --log-level) to existing argparse
- **Size:** SMALL (enhancement to existing script)

---

## Components Researched

### Component 1: run_game_data_fetcher.py (Runner Script)

**Discovery Scope Reference:** Feature enhances existing argparse structure

**Found in Codebase:**
- File: `run_game_data_fetcher.py` (lines 1-174)
- Function: `main()` (lines 54-173)
- Existing argparse: Lines 56-84

**Actual Code Structure:**

```python
# Current argparse (lines 56-84)
parser = argparse.ArgumentParser(
    description="Fetch NFL game data (venue, weather, scores) from ESPN and Open-Meteo APIs"
)
parser.add_argument('--season', type=int, default=None)
parser.add_argument('--output', type=str, default=None)
parser.add_argument('--weeks', type=str, default=None)
parser.add_argument('--current-week', type=int, default=None)
```

**How It Works Today:**
1. Parses 4 arguments (season, output, weeks, current-week)
2. Changes to player-data-fetcher directory (line 97)
3. Imports fetch_game_data function (line 104)
4. Sets up logger with INFO level, hardcoded (line 109)
5. Determines season/week from args or config (lines 112-118)
6. Calls fetch_game_data() with parsed parameters (lines 143-148)
7. Prints summary statistics (lines 152-160)

**Implementation Approach for This Feature:**
- Add 3 new arguments to existing parser:
  - `--debug` (flag, enables DEBUG logging + limits to single week)
  - `--e2e-test` (flag, fetches single week only, ≤3 min)
  - `--log-level` (str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO')
- Modify setup_logger() call to use args.log_level instead of hardcoded "INFO" (line 109)
- Add conditional logic for debug mode (if args.debug: enable DEBUG + limit weeks)
- Add conditional logic for E2E mode (if args.e2e_test: force weeks=[1])

---

### Component 2: player-data-fetcher/game_data_fetcher.py (Fetcher Module)

**Discovery Scope Reference:** Module called by runner, needs to understand interface

**Found in Codebase:**
- File: `player-data-fetcher/game_data_fetcher.py`
- Main function: `fetch_game_data()` (lines 517-569)
- Main class: `GameDataFetcher` (lines 36-514)

**Actual Code Signatures:**

```python
# fetch_game_data function (lines 517-522)
def fetch_game_data(
    output_path: Optional[Path] = None,
    season: int = NFL_SEASON,
    current_week: int = CURRENT_NFL_WEEK,
    weeks: Optional[List[int]] = None
) -> Path
```

**How It Works Today:**
1. Gets logger via get_logger() (line 535)
2. Creates GameDataFetcher instance with season/current_week (lines 547-551)
3. If weeks specified: fetches each week individually (lines 558-563)
4. If no weeks: uses fetch_all() to fetch weeks 1 to current_week (line 566)
5. Returns CSV file path (line 569)

**Implementation Approach for This Feature:**
- No changes needed to fetch_game_data() signature (weeks parameter already supports single week)
- For E2E mode: pass weeks=[1] from runner
- For debug mode: pass weeks=[current_week] from runner (single week only)
- Fetcher module doesn't need modification (uses existing weeks parameter)

---

### Component 3: utils/LoggingManager.py (Logging Infrastructure)

**Discovery Scope Reference:** Must understand logging setup for --debug and --log-level args

**Found in Codebase:**
- File: `utils/LoggingManager.py` (lines 1-100+)
- Function: `setup_logger()` (lines 45-69)
- Supported levels: DEBUG, INFO, WARNING, ERROR, CRITICAL (lines 34-40)

**Actual Code Signature:**

```python
# setup_logger function (lines 45-53)
def setup_logger(
    name: str,
    level: Union[str, int] = 'INFO',
    log_to_file: bool = False,
    log_file_path: Optional[Union[str, Path]] = None,
    log_format: str = 'standard',
    enable_console: bool = True,
    max_file_size: int = 10 * 1024 * 1024,
    backup_count: int = 5
) -> logging.Logger
```

**How It Works Today:**
- Accepts level as string ('DEBUG', 'INFO', etc.) or int
- Maps string levels to logging constants (lines 81-83)
- Supports three format styles: detailed, standard, simple (lines 27-29)
- Creates console handler with specified level (lines 88-93)

**Current Usage in run_game_data_fetcher.py:**
```python
# Line 109
logger = setup_logger("game_data_fetcher", "INFO", False, None, "standard")
```

**Implementation Approach for This Feature:**
- Change hardcoded "INFO" to args.log_level (from new --log-level argument)
- For --debug flag: set log_level to "DEBUG"
- No changes needed to LoggingManager itself (already supports all required levels and formats)

---

## Existing Test Patterns

**Test Files Found:**
- `tests/player-data-fetcher/test_game_data_fetcher.py` (unit tests for fetcher module)
- `tests/historical_data_compiler/test_game_data_fetcher.py` (integration with compiler)

**Test Structure:** (Need to examine for patterns, but not blocking for spec creation)

**Implementation Approach for This Feature:**
- Create unit tests for new argument parsing (test --debug, --e2e-test, --log-level)
- Create unit tests for debug mode behavior (verify DEBUG logging enabled)
- Create unit tests for E2E mode behavior (verify single week fetch)
- Follow existing test patterns from similar fetcher tests

---

## Interface Dependencies

### Dependency 1: fetch_game_data() Function

**Interface:**
```python
fetch_game_data(
    output_path: Optional[Path] = None,
    season: int = NFL_SEASON,
    current_week: int = CURRENT_NFL_WEEK,
    weeks: Optional[List[int]] = None
) -> Path
```

**How Feature Will Use:**
- Pass weeks=[1] for E2E mode (single week fetch)
- Pass weeks=[current_week] for debug mode (single week fetch)
- Use default None for normal operation (fetches 1 to current_week)

### Dependency 2: setup_logger() Function

**Interface:**
```python
setup_logger(
    name: str,
    level: Union[str, int] = 'INFO',
    ...
) -> logging.Logger
```

**How Feature Will Use:**
- Pass args.log_level instead of hardcoded "INFO"
- For --debug flag: pass "DEBUG" level

### Dependency 3: parse_weeks() Function

**Interface:**
```python
# Lines 28-51 in run_game_data_fetcher.py
def parse_weeks(weeks_str: str) -> list
```

**How Feature Will Use:**
- No changes needed (E2E mode just passes weeks=[1] directly, not via --weeks arg)
- Existing function continues to work for user-specified --weeks

---

## Edge Cases Identified

### Edge Case 1: Conflicting Flags

**Scenario:** User specifies both --debug and --e2e-test
- **Current Behavior:** No handling (doesn't exist yet)
- **Proposed Behavior:** --e2e-test takes precedence (E2E mode is primary goal)
- **Implementation:** if args.e2e_test: weeks=[1] elif args.debug: weeks=[current_week]

### Edge Case 2: --weeks with --e2e-test

**Scenario:** User specifies --weeks 1-18 --e2e-test
- **Current Behavior:** No handling (--e2e-test doesn't exist)
- **Proposed Behavior:** --e2e-test overrides --weeks (E2E mode forces single week)
- **Implementation:** Check args.e2e_test first, then args.weeks

### Edge Case 3: --log-level with --debug

**Scenario:** User specifies --log-level WARNING --debug
- **Current Behavior:** No handling
- **Proposed Behavior:** --debug forces DEBUG level (debug flag takes precedence)
- **Implementation:** if args.debug: log_level = "DEBUG" else: log_level = args.log_level

### Edge Case 4: Historical Season with E2E

**Scenario:** User specifies --season 2024 --e2e-test
- **Current Behavior:** Historical seasons set current_week=18 (line 117)
- **Proposed Behavior:** E2E mode fetches week 1 regardless of season
- **Implementation:** E2E mode uses weeks=[1], ignores current_week

---

## Research Completeness

### Components Researched:
1. [✅] `run_game_data_fetcher.py` - Existing argparse structure, main() logic
2. [✅] `player-data-fetcher/game_data_fetcher.py` - fetch_game_data() function, GameDataFetcher class
3. [✅] `utils/LoggingManager.py` - setup_logger() function, supported levels
4. [✅] Test files - Existing test patterns identified

### Code Evidence Collected:
1. [✅] Exact argparse structure (lines 56-84 in runner)
2. [✅] fetch_game_data() signature (lines 517-522 in fetcher)
3. [✅] setup_logger() signature (lines 45-53 in LoggingManager)
4. [✅] Current logger call (line 109 in runner)
5. [✅] Weeks processing logic (lines 127-130 in runner)

### Discovery Alignment:
1. [✅] Verified existing --weeks argument (supports E2E single week fetch)
2. [✅] Confirmed logging infrastructure supports DEBUG level
3. [✅] Identified no need for module changes (runner-only enhancement)
4. [✅] Confirmed real API usage (no mocking infrastructure exists)

---

## Implementation Summary

**What Needs to Change:**
1. Add 3 arguments to argparse in `run_game_data_fetcher.py` (--debug, --e2e-test, --log-level)
2. Replace hardcoded "INFO" with args.log_level in setup_logger() call
3. Add conditional logic for debug mode (enable DEBUG + limit weeks)
4. Add conditional logic for E2E mode (force weeks=[1])
5. Add unit tests for new arguments and modes

**What Stays the Same:**
1. Existing --season, --output, --weeks, --current-week arguments
2. `fetch_game_data()` function signature (no changes)
3. GameDataFetcher class (no changes)
4. LoggingManager (no changes)
5. Overall runner structure (directory changes, imports, summary stats)

**Estimated Complexity:** LOW (enhancement to existing script, minimal changes)

**Ready for Specification Phase:** YES (all research complete, clear implementation path)

---

**Research Complete:** 2026-01-29 03:25
**Next Phase:** S2.P2 (Specification Phase)
