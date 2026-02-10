# Feature Checklist: historical_data_compiler_logging

**Part of Epic:** KAI-8-logging_refactoring
**Created:** 2026-02-06
**Last Updated:** 2026-02-06
**Status:** 🔄 TO BE POPULATED IN S2

---

## Purpose

This checklist will contain **questions and decisions that require user input**.

**Agent creates questions during S2 research. User reviews and answers ALL questions. Only after user approval can S5 begin.**

---

## Functional Questions

### Q1: Log Level - "No coordinates" Message

**Context:** game_data_fetcher.py line 346 logs "No coordinates for {team}/{city}, skipping weather" at DEBUG level.

**Current:** DEBUG (implementation detail)

**Question:** Should this be INFO instead? This is a user-visible decision (weather data skipped for game), not just an implementation detail.

**Options:**
- A) Keep as DEBUG (implementation detail)
- B) Change to INFO (user awareness - weather data unavailable)

**Status:** ANSWERED

**User Answer:** B - Change to INFO (user-visible outcome affecting data quality)

---

### Q2: Log Level - "Error parsing event" Message

**Context:** schedule_fetcher.py line 124 logs "Error parsing event in week {week}: {e}" at DEBUG level.

**Current:** DEBUG

**Question:** Should this be WARNING instead? This is a non-fatal error (parsing failed, but script continues), which typically warrants WARNING level.

**Options:**
- A) Keep as DEBUG (debugging information)
- B) Change to WARNING (non-fatal error requiring user awareness)

**Status:** ANSWERED

**User Answer:** B - Change to WARNING (non-fatal error with data quality impact)

---

## Technical Questions

### Q3: Add Configuration Logging at Startup

**Context:** compile_historical_data.py has GENERATE_CSV/GENERATE_JSON toggles (lines 53-54) that control output format, but these values aren't logged.

**Current:** No logging of these configuration values

**Question:** Should I add INFO log at startup to show configuration: "Output format: CSV={GENERATE_CSV}, JSON={GENERATE_JSON}"?

**Rationale:** Helps users understand which output format is being generated (improves debugging)

**Options:**
- A) Add INFO log for configuration visibility
- B) Skip (configuration not important enough to log)

**Status:** ANSWERED

**User Answer:** A - Add INFO log (improves configuration visibility and debugging)

---

### Q4: Add HTTP Client Configuration Logging

**Context:** http_client.py __init__ accepts timeout and rate_limit_delay parameters, but doesn't log them.

**Current:** No logging of HTTP client configuration

**Question:** Should I add INFO log at __init__ to show configuration: "HTTP client initialized (timeout={timeout}s, rate_limit={rate_limit_delay}s)"?

**Rationale:** Helps debug API issues (knowing timeout/rate limit values)

**Options:**
- A) Add INFO log for configuration visibility
- B) Skip (configuration not important enough to log)

**Status:** ANSWERED

**User Answer:** B - Skip (configuration not important enough to log)

---

### Q5: Add Weather Fetch DEBUG Logging

**Context:** game_data_fetcher.py fetches weather data from API but doesn't log before API call.

**Current:** No DEBUG log before weather fetch

**Question:** Should I add DEBUG log before weather API call: "Fetching weather for {game_date} at {lat},{lon}"?

**Rationale:** Helps debug weather fetch issues (know which coordinates are being used)

**Options:**
- A) Add DEBUG log for tracing
- B) Skip (weather fetch not important enough to log)

**Status:** ANSWERED

**User Answer:** A - Add DEBUG log (helps trace API calls with coordinates)

---

### Q6: Add Player Parsing DEBUG Logging

**Context:** player_data_fetcher.py parses player data from ESPN API but doesn't log transformations.

**Current:** Only throttled progress log (every 100 players)

**Question:** Should I add DEBUG log for player parsing transformations showing before/after data?

**Rationale:** Helps debug player parsing issues (data transformation visibility)

**Options:**
- A) Add DEBUG log for data transformations
- B) Skip (existing throttled log sufficient)

**Status:** ANSWERED

**User Answer:** B - Skip (existing throttled progress log is sufficient)

---

## Integration Questions

{No integration questions - Feature 01 integration is straightforward}

---

## Error Handling Questions

{No error handling questions - Feature 01 handles all file logging errors}

---

## Testing Questions

### Q7: Test Assertion Update Scope

**Context:** 3 test files (test_weekly_snapshot_generator.py, test_game_data_fetcher.py, test_team_data_calculator.py) have logging assertions.

**Current:** Unknown which assertions will break until tests run

**Question:** Should I:
- A) Update ALL logging assertions preemptively (review all 3 test files, update to match new log messages)
- B) Run tests first, only update assertions that actually fail

**Rationale:** Option A is safer (catch all issues upfront), Option B is faster (only fix what breaks)

**Status:** ANSWERED

**User Answer:** B - Reactive approach (run tests first, fix only what fails - more efficient)

---

## Open Questions (Uncategorized)

{No uncategorized questions}

---

## User Approval

**User Status:** ✅ APPROVED
**Approved:** 2026-02-06 22:45
**Gate 3:** PASSED - All questions answered and spec approved

---

## Checklist Summary

- [x] Q1: Change "No coordinates" to INFO
- [x] Q2: Change "Error parsing event" to WARNING
- [x] Q3: Add configuration INFO log for CSV/JSON toggles
- [x] Q4: Skip HTTP client configuration logging
- [x] Q5: Add weather fetch DEBUG log with coordinates
- [x] Q6: Skip player parsing transformation logging
- [x] Q7: Reactive test update approach

**Total Questions:** 7
**Answered:** 7
**Resolved:** 7 (all approved by user at Gate 3)
