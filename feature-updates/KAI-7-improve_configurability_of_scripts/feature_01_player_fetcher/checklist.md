# Feature 01 Checklist: Player Fetcher Configurability

**Purpose:** Track user questions and decisions for this feature

**Status:** 6 questions pending user answers

---

## Questions for User

### Question 1: Argument Naming Convention ✅ RESOLVED

**Context:** Epic doesn't specify CLI argument naming. run_game_data_fetcher.py uses `--current-week` but simpler `--week` is more concise.

**Options:**
- **Option A:** Use `--week` (concise, matches config constant name minus prefix)
  - Pros: Shorter to type, clearer mapping to CURRENT_NFL_WEEK
  - Cons: Inconsistent with existing game_data_fetcher pattern
- **Option B:** Use `--current-week` (matches game_data_fetcher pattern)
  - Pros: Consistency across fetcher scripts
  - Cons: More verbose, doesn't match config constant name

**Epic Reference:** DISCOVERY.md doesn't specify argument naming style

**Recommendation:** Option A (--week) for consistency with config.py constant name

**Why this is a question:** Genuine unknown about naming convention preference. Both options are valid.

**Impact on spec.md:** Will determine argument names in Requirement 1 (21 arguments list)

**User Answer:** A - Use `--week` (concise naming)
**Resolved:** 2026-01-30

---

### Question 2: E2E Player Limit ✅ RESOLVED

**Context:** E2E test mode needs to complete in ≤3 minutes. Research shows ESPN_PLAYER_LIMIT=50 should work, but haven't validated timing.

**Options:**
- **Option A:** 50 players (very fast, ~1-2 min estimated)
  - Pros: Well under 3-minute target, minimal API calls
  - Cons: May not catch issues that appear with larger datasets
- **Option B:** 100 players (moderate, ~2-3 min estimated)
  - Pros: Better coverage, still under target
  - Cons: Closer to time limit, more API calls
- **Option C:** 200 players (slower, ~4-5 min estimated)
  - Pros: Even better coverage
  - Cons: Likely exceeds 3-minute target

**Epic Reference:** DISCOVERY.md:246 specifies "≤3 min" for E2E mode

**Recommendation:** Option A (50 players) to safely stay under 3-minute limit

**Why this is a question:** Genuine unknown about acceptable trade-off between speed and coverage. Need user's risk tolerance.

**Impact on spec.md:** Will determine ESPN_PLAYER_LIMIT value in Requirement 3 (E2E Mode Behavior)

**User Answer:** B - 100 players (moderate speed, better coverage)
**Resolved:** 2026-01-30

---

### Question 3: Debug vs E2E Mode Exclusivity ✅ RESOLVED

**Context:** Both --debug and --e2e-test modify config values. Epic doesn't specify if they can be combined.

**Options:**
- **Option A:** Mutually exclusive (error if both specified)
  - Pros: Clear semantics, prevents confusion
  - Cons: Can't debug E2E tests
- **Option B:** Allow both (apply both sets of overrides)
  - Pros: Flexibility to debug E2E tests
  - Cons: Conflicting overrides need precedence rules (e.g., ESPN_PLAYER_LIMIT: debug=100, e2e=100)
- **Option C:** E2E takes precedence (debug logging only)
  - Pros: E2E behavior consistent, gets debug logging
  - Cons: Debug behavioral changes ignored

**Epic Reference:** DISCOVERY.md doesn't address mode combination

**Recommendation:** Option B with E2E precedence for data limiting, debug precedence for logging

**Why this is a question:** Genuine unknown about intended behavior. Both modes are independent features.

**Impact on spec.md:** Will determine precedence logic in Requirement 2 and Requirement 3, update Algorithm section

**User Answer:** B - Allow both (E2E precedence for data, debug for logging)
**Resolved:** 2026-01-30

---

### Question 4: Debug Mode Output Formats ✅ RESOLVED

**Context:** Debug mode is for rapid iteration. Should it force minimal output formats for speed, or respect user's output preferences?

**Options:**
- **Option A:** Force minimal output (CSV only)
  - Pros: Faster debug cycles, consistent behavior
  - Cons: Can't debug Excel/JSON generation issues
- **Option B:** Respect existing config/args
  - Pros: Flexibility, can debug specific output formats
  - Cons: Slower if Excel enabled

**Epic Reference:** DISCOVERY.md:245 says "DEBUG logging + minimal data fetch" but doesn't mention output formats

**Recommendation:** Option B (respect config) - user can explicitly disable formats with --no-excel if desired

**Why this is a question:** "Minimal" could apply to data OR outputs. Need clarification on scope of debug changes.

**Impact on spec.md:** May add output format overrides to Requirement 2 (Debug Mode Behavior)

**User Answer:** A - Force minimal output (CSV + position JSON only, files that go to data folder)
**Resolved:** 2026-01-30

---

### Question 5: E2E Mode Logging Level ✅ RESOLVED

**Context:** E2E tests should be fast and quiet. Should they use DEBUG logging for visibility or INFO for speed?

**Options:**
- **Option A:** Keep at INFO level (faster, less output)
  - Pros: Cleaner output, faster execution
  - Cons: Less visibility into what E2E test is doing
- **Option B:** Enable DEBUG logging (verbose)
  - Pros: Better debugging of E2E test failures
  - Cons: More output, slightly slower

**Epic Reference:** DISCOVERY.md:246 doesn't specify logging level for E2E mode

**Recommendation:** Option A (INFO) - E2E is for integration testing, not debugging. Use --debug for detailed logs.

**Why this is a question:** Trade-off between visibility and speed. Need user's preference.

**Impact on spec.md:** May add LOGGING_LEVEL override to Requirement 3 (E2E Mode Behavior)

**User Answer:** A - Keep at INFO level (use --debug --e2e-test for verbose E2E)
**Resolved:** 2026-01-30

---

### Question 6: Argument Validation Strictness ✅ RESOLVED

**Context:** Invalid arguments (week=25, season=1999) could cause runtime errors. Should script fail fast or be lenient?

**Options:**
- **Option A:** Strict validation (error immediately on invalid args)
  - Pros: Fail fast, clear error messages, prevents confusing runtime errors
  - Cons: May reject edge cases that ESPN API actually supports
- **Option B:** Lenient validation (warn but continue)
  - Pros: Flexibility, lets ESPN API be the validator
  - Cons: Confusing errors from ESPN if arguments actually invalid
- **Option C:** No validation (trust user + ESPN API)
  - Pros: Simplest implementation
  - Cons: Poor user experience on typos

**Epic Reference:** DISCOVERY.md doesn't specify validation requirements

**Recommendation:** Option A (strict) with reasonable ranges: week 1-18, season 2020-2030

**Why this is a question:** User experience vs flexibility trade-off. Need guidance on error handling philosophy.

**Impact on spec.md:** Will determine validation logic in Requirement 6 (Error Handling)

**User Answer:** C - No validation (trust user + ESPN API, simplest implementation)
**Resolved:** 2026-01-30

---

## Checklist Status

**Total Questions:** 6
**Answered:** 6
**Pending:** 0

✅ **ALL QUESTIONS RESOLVED** - Acceptance criteria created and USER APPROVED (2026-01-30)

**Categories:**
- User Preferences: 5 questions (Q1, Q2, Q3, Q4, Q5)
- Error Handling: 1 question (Q6)

**Note:** All questions are genuine unknowns that require user decision. None are research gaps.
