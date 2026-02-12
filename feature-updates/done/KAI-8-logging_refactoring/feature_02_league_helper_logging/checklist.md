# Feature Checklist: league_helper_logging

**Part of Epic:** KAI-8-logging_refactoring
**Created:** 2026-02-06
**Last Updated:** 2026-02-06 21:45
**Status:** ✅ ALL QUESTIONS RESOLVED (5/5)

---

## Purpose

This checklist contains **questions and decisions that require user input**.

**Agent created questions during S2.P1.I1 research. User must review and answer ALL questions. Only after user approval can spec be finalized and S5 implementation begin.**

---

## Functional Questions

### ❓ Question 1: Subprocess Wrapper Argument Forwarding Strategy

**Category:** CLI Integration (Subprocess Wrapper)

**Context:**
run_league_helper.py is a subprocess wrapper that calls league_helper/LeagueHelperManager.py. Currently it passes only DATA_FOLDER as argument. With the new --enable-log-file flag, we need to forward CLI arguments from the wrapper to the target script.

**Research Findings (RESEARCH_NOTES.md Section 1):**
- Discovery Iteration 5 recommended sys.argv[1:] forwarding (Option B - simpler, future-proof)
- Current subprocess.run() args: [sys.executable, script, DATA_FOLDER]
- Two approaches available:
  - **Option A:** Forward ALL args using sys.argv[1:] (append all CLI args)
  - **Option B:** Parse args in wrapper, filter to known args (--enable-log-file only)

**Options:**

**Option A: Forward ALL Args (sys.argv[1:])** - RECOMMENDED
- Implementation: `subprocess.run([sys.executable, script, DATA_FOLDER] + sys.argv[1:])`
- Pros: Simpler, future-proof (handles any future flags automatically), aligns with Discovery
- Cons: Wrapper doesn't validate args (target script gets all args, including invalid ones)
- Example: User runs `python run_league_helper.py --enable-log-file --foo` → Both flags forwarded to target

**Option B: Parse and Filter Args**
- Implementation: Parse --enable-log-file in wrapper, only forward known args
- Pros: Explicit control, wrapper can validate args before forwarding
- Cons: More complex, need to update wrapper for every new flag
- Example: User runs `python run_league_helper.py --enable-log-file --foo` → Only --enable-log-file forwarded

**Question:** Should run_league_helper.py forward ALL args (sys.argv[1:]) or parse and filter to known args only?

**My Recommendation:** Option A (forward all args) - simpler, aligns with Discovery Iteration 5 recommendation, future-proof

**User Decision:** ☑ Option A (forward all args)

**Status:** ✅ RESOLVED (2026-02-06)

---

### ❓ Question 2: LOGGING_TO_FILE Constant Handling

**Category:** Technical (Constants Deprecation)

**Context:**
league_helper/constants.py currently defines `LOGGING_TO_FILE = False` (line 25). After CLI integration, this constant is no longer used (replaced by `args.enable_log_file` from CLI flag).

**Research Findings (RESEARCH_NOTES.md Section 3):**
- Current: constants.LOGGING_TO_FILE = False (hardcoded)
- After change: setup_logger() uses args.enable_log_file (from CLI)
- Constant becomes unused but still exists in codebase

**Options:**

**Option A: Keep as Fallback** - RECOMMENDED
- Keep constant in constants.py
- Add deprecation comment: "# NOTE: Deprecated - use --enable-log-file CLI flag instead"
- Provides fallback if script called without CLI parsing (e.g., from tests)
- Backward compatible

**Option B: Remove Constant**
- Delete LOGGING_TO_FILE from constants.py
- Always use CLI arg (args.enable_log_file)
- Cleaner codebase (no unused constants)
- May break tests or other code that imports this constant

**Option C: Keep Without Deprecation**
- Keep constant as-is (no comment)
- Just use CLI flag instead
- Most minimal change

**Question:** Should we keep LOGGING_TO_FILE constant (with deprecation note), remove it entirely, or keep it as-is?

**My Recommendation:** Option A (keep as fallback with deprecation comment) - backward compatible, clear deprecation notice for future developers

**User Decision:** ☑ Option B (remove constant)

**Status:** ✅ RESOLVED (2026-02-06)

---

### ❓ Question 4: Log Quality Audit Scope (Mode Managers)

**Category:** Log Quality Improvements (Scope)

**Context:**
Research found 6 mode managers in league_helper/, but Discovery only mentioned 4. Need user decision on whether to audit all 6 or limit to Discovery scope.

**Research Findings (RESEARCH_NOTES.md Section 7):**
- Discovery mentioned 4 mode managers: AddToRosterModeManager, StarterHelperModeManager, TradeSimulatorModeManager, ModifyPlayerDataModeManager
- Actual codebase has 6 mode managers (2 additional):
  - ReserveAssessmentModeManager (not mentioned in Discovery)
  - SaveCalculatedPointsManager (not mentioned in Discovery)
- Discovery Q6 answered: "System-wide (Option B)" - suggests comprehensive scope

**Options:**

**Option A: All 6 Mode Managers (Comprehensive)** - RECOMMENDED
- Audit all mode managers found in codebase
- Aligns with Discovery Q6 (system-wide scope)
- Ensures complete log quality across entire league_helper
- More work but more thorough

**Option B: Only 4 From Discovery (Scope-Limited)**
- Audit only the 4 mode managers mentioned in Discovery
- Narrower scope, less work
- May leave log quality issues in 2 additional managers
- Incomplete if Discovery scope was unintentional

**Question:** Should log quality audit include all 6 mode managers (comprehensive) or only 4 mentioned in Discovery (scope-limited)?

**My Recommendation:** Option A (all 6 mode managers) - Discovery Q6 specified system-wide scope, and 2 additional managers are part of league_helper system

**User Decision:** ☑ Option A (all 6 mode managers - comprehensive)

**Status:** ✅ RESOLVED (2026-02-06)

---

## Technical Questions

### ❓ Question 5: LOG_NAME Consistency Verification

**Category:** Integration with Feature 01 (Contract Compliance)

**Context:**
Feature 01 spec specifies logger name must match folder name for consistency. Need to verify "league_helper" constant is correct.

**Research Findings (RESEARCH_NOTES.md Section 3):**
- constants.LOG_NAME = "league_helper" (line 26)
- Feature 01 contract: Logger name = folder name (logs/league_helper/)
- Must use consistent name (not "LeagueHelper" or "league-helper")

**Contract Requirements from Feature 01:**
1. Logger name = folder name
2. Use lowercase with underscores (not camelCase or hyphens)
3. Name used in setup_logger() first argument

**Current Value:** "league_helper" (matches Feature 01 contract ✅)

**Question:** Confirm that "league_helper" is the correct logger name (will create logs/league_helper/ folder)?

**My Analysis:**
- ✅ Matches Feature 01 contract (lowercase, underscore separator)
- ✅ Consistent with script name pattern (run_league_helper.py)
- ✅ No changes needed (already correct)

**User Decision:** ☑ Confirmed: "league_helper" is correct

**Status:** ✅ RESOLVED (2026-02-06)

---

## Testing Questions

### ❓ Question 3: Integration Test Log Assertions

**Category:** Testing Strategy

**Context:**
Integration test (test_league_helper_integration.py) tests end-to-end workflows. Log quality improvements may change log output. Need decision on whether to add log capture assertions.

**Research Findings (RESEARCH_NOTES.md Section 6):**
- Integration test creates temp data, tests draft/starter/trade workflows
- No log-related assertions found in preliminary review (lines 1-100)
- Log quality changes should not affect functional behavior (tests should still pass)

**Options:**

**Option A: No Log Assertions (Functional Focus)** - RECOMMENDED
- Keep integration tests focused on functional behavior (not log output)
- Logs are implementation detail (tests shouldn't depend on exact log messages)
- Simpler tests, less brittle (log changes don't break tests)
- Still verify tests pass after log changes (functional behavior unchanged)

**Option B: Add Log Capture Assertions**
- Capture log output during tests
- Assert on expected log patterns (e.g., "Interactive league helper started")
- Verifies log quality improvements actually work
- More brittle (tests break if log messages change)

**Question:** Should we add log capture assertions to integration tests, or keep tests focused on functional behavior?

**My Recommendation:** Option A (no log assertions) - Tests should verify functional behavior, not implementation details. Log changes are internal refactoring that shouldn't affect test outcomes.

**User Decision:** ☑ Option A (no log assertions - functional focus)

**Status:** ✅ RESOLVED (2026-02-06)

---

## Derived Questions

**No derived questions at this time** - All questions above are from S2.P1.I1 research findings.

---

## Open Questions (Uncategorized)

**No uncategorized questions** - All questions categorized above.

---

## Resolution Summary

| Question | Status | User Answer | Date Resolved |
|----------|--------|-------------|---------------|
| Q1: Subprocess wrapper forwarding | ✅ RESOLVED | Option A (forward all args) | 2026-02-06 |
| Q2: LOGGING_TO_FILE constant | ✅ RESOLVED | Option B (remove constant) | 2026-02-06 |
| Q3: Integration test log assertions | ✅ RESOLVED | Option A (no log assertions) | 2026-02-06 |
| Q4: Log quality audit scope | ✅ RESOLVED | Option A (all 6 mode managers) | 2026-02-06 |
| Q5: LOG_NAME consistency | ✅ RESOLVED | Confirmed: "league_helper" | 2026-02-06 |

**All Questions Resolved:** ☑ YES (5/5 answered)

---

## Impact on Spec

**After all questions resolved:**
- Spec.md will be updated based on user answers
- Implementation approach confirmed for all 4 requirements
- Scope finalized (all 6 mode managers or only 4)
- Technical decisions documented

**No spec changes needed if:**
- Q1 → Option A (already reflected in spec)
- Q2 → Option A (already reflected in spec)
- Q3 → Option A (already reflected in spec)
- Q4 → Option A (already reflected in spec)
- Q5 → Confirmed (already correct in spec)

**Spec updates needed if:**
- Q1 → Option B (update Requirement 1 with parse/filter approach)
- Q2 → Option B or C (update Integration Points section)
- Q3 → Option B (update Testing Strategy section)
- Q4 → Option B (update Requirement 3/4 scope to 4 managers only)
- Q5 → Change name (update all references to logger name)

---

## User Approval

**User Status:** ✅ APPROVED (2026-02-06)
**Ready for S5:** ☑ YES (after Primary completes S2.P2 and epic completes S3/S4)

**Next Steps After User Approval:**
1. Agent updates spec.md based on user answers (S2.P1.I2)
2. Agent runs Validation Loop on updated spec (S2.P1.I3)
3. Agent presents final spec for Gate 3 approval (S2.P1.I3)
4. After Gate 3 → Agent stops, waits for Primary to run S2.P2

---

**Created:** S2.P1.I1 (Feature-Level Discovery - research complete)
**Next:** S2.P1.I2 (Checklist Resolution - user answers questions one-at-a-time)
