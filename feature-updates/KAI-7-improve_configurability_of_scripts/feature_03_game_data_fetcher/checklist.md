# Feature 03 Checklist: Game Data Fetcher Enhancement

**Status:** OPEN (awaiting user answers)
**Created:** 2026-01-29
**Feature:** feature_03_game_data_fetcher

---

## Checklist Questions

### Question 1: Flag Priority When --debug and --log-level Conflict

**Status:** [x] RESOLVED (2026-01-30 - User approved Option A)

**Context:**
When user specifies both `--debug` and `--log-level` arguments, we need to decide priority.

Example: `python run_game_data_fetcher.py --debug --log-level ERROR`

**Discovery Reference:**
- User Answer Q4 says "debug = behavioral + logging" but doesn't specify interaction with --log-level arg
- Current spec (Requirement 3) assumes --debug forces DEBUG level, ignoring --log-level

**Options:**

**Option A: --debug Forces DEBUG Level (Current Spec)**
- Behavior: --debug always sets log_level = "DEBUG", --log-level arg ignored if --debug present
- Pros: Simpler logic, --debug is clear shortcut for "DEBUG everything"
- Cons: User can't combine debug behavior with non-DEBUG logging

**Option B: --log-level Takes Precedence**
- Behavior: --debug enables behavioral changes only, --log-level controls logging independently
- Pros: More flexible, user can debug with WARNING-level logs
- Cons: --debug flag loses its "enable DEBUG logs" meaning

**Option C: Error When Both Specified**
- Behavior: Script exits with error if both --debug and --log-level present
- Pros: Forces user to choose explicitly
- Cons: Less convenient, unnecessary restriction

**Recommendation:** Option A (--debug forces DEBUG level)

**Rationale:**
- --debug is convenience shortcut for common case (DEBUG logs + single week fetch)
- If user wants fine-grained control, use --log-level without --debug
- Matches typical CLI tool behavior (debug flag = verbose output)

**Why This Is a Question:**
Genuine user preference - both options are valid, depends on intended use case for --debug flag

**USER DECISION:** **Option A** - --debug forces DEBUG level
**Date:** 2026-01-30
**Impact:** No spec changes needed (spec already assumes Option A)

---

### Question 2: E2E Mode Target Week Selection

**Status:** [x] RESOLVED (2026-01-30 - User approved Option A)

**Context:**
E2E test mode needs to fetch limited data (≤3 min). Current spec always fetches week 1.

**Discovery Reference:**
- User Answer Q3: "Fetchers: real APIs with data limiting args"
- Discovery doesn't specify WHICH week to use for E2E mode

**Options:**

**Option A: Always Fetch Week 1 (Current Spec)**
- Behavior: `--e2e-test` always fetches week 1 of specified season
- Pros: Consistent test target, week 1 data always available (past week), predictable output
- Cons: Week 1 might have anomalies, doesn't test "current week" scenario

**Option B: Fetch Current Week Minus 1**
- Behavior: `--e2e-test` fetches previous week (current_week - 1)
- Pros: Tests recent data, closer to production usage
- Cons: Week 0 edge case at season start, less predictable test output

**Option C: Configurable via --e2e-week Argument**
- Behavior: `--e2e-test --e2e-week 5` fetches week 5
- Pros: Maximum flexibility for testing different scenarios
- Cons: Additional argument complexity, default still needed

**Recommendation:** Option A (always week 1)

**Rationale:**
- Week 1 is stable target (full season of past data available)
- Simplest implementation (no edge cases like week 0)
- Integration tests can rely on consistent output
- If user wants different week for testing, can use --weeks 5 (without --e2e-test)

**Why This Is a Question:**
Genuine unknown - Discovery specifies "data limiting" but not specific strategy. User preference for test consistency vs recency.

**USER DECISION:** **Option A** - Always fetch week 1 for E2E mode
**Date:** 2026-01-30
**Impact:** No spec changes needed (spec already assumes Option A)

---

## Summary

**Total Questions:** 2
**Open Questions:** 0
**Resolved Questions:** 2

**Categories:**
- User Preferences: 2 (flag priority, E2E week selection)
- Business Logic: 0
- Edge Cases: 0

**All Questions Valid:**
- ✅ Both questions ask about genuine user preferences
- ✅ Not researchable from codebase (design decisions)
- ✅ Clear options with trade-offs
- ✅ Recommendations provided with rationale

---

## User Approval

**Approval Status:** ✅ APPROVED
**Date:** 2026-01-30
**Checklist Status:** All questions resolved (both Option A recommendations approved)

**User Decision Summary:**
- Question 1: Option A (--debug forces DEBUG level)
- Question 2: Option A (Always fetch week 1 for E2E mode)

**Impact:** No spec changes needed - spec already assumes both Option A choices

---

**Gate 2:** ✅ PASSED (2026-01-30)
**Next Step:** Proceed to S2.P3 (Refinement Phase)
