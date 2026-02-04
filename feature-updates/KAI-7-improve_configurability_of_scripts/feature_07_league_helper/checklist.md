# Feature 07 Checklist: League Helper Configurability

**Status:** COMPLETE (S2.P3 Phase 3)
**Created:** 2026-01-29
**Last Updated:** 2026-01-30
**Total Questions:** 5
**Resolved:** 5
**Open:** 0

---

## Instructions

**For User:**
1. Review each question below
2. Fill in your answer in the "User Answer:" field
3. Mark checkbox [x] when answered
4. Agent will update spec.md based on your answers

**For Agent:**
- Do NOT mark checkboxes (only user can)
- Update spec.md immediately after user answers each question
- Move resolved items to "Resolved Questions" section

---

## Open Questions

---

### Question 2: E2E Mode Error Handling

**Context:** If E2E mode fails midway through 5 modes (e.g., Mode 3 fails), should it continue or abort?

**Why uncertain:** User didn't specify error handling strategy for E2E test suite

**Options:**
- **Option A:** Abort on first failure (fail-fast)
  - Pros: Immediate feedback, clear failure point
  - Cons: Doesn't test remaining modes
  
- **Option B:** Continue through all 5 modes, report all failures at end
  - Pros: Complete test coverage, identifies all issues
  - Cons: Later modes may depend on earlier modes

- **Option C:** Skip failed mode, continue with remaining (best-effort)
  - Pros: Maximum coverage
  - Cons: May hide cascading failures

**Epic Reference:** User Answer Q5 mentioned "validate exit code AND outcomes" but didn't specify multi-mode failure handling

**Recommendation:** Option A (fail-fast) - clearest for debugging

**User Answer:**


**Impact on spec.md:** Will add error handling section to Requirement 3

---

### Question 3: --silent Flag Behavior

**Context:** What should --silent flag suppress?

**Why uncertain:** Epic mentioned --silent flag but didn't define behavior scope

**Options:**
- **Option A:** Suppress ALL output (including errors)
  - Pros: Truly silent
  - Cons:** May hide critical errors
  
- **Option B:** Suppress INFO/DEBUG, show WARNING/ERROR
  - Pros: Errors still visible
  - Cons: Not completely silent

- **Option C:** Suppress console, still log to file
  - Pros: Quiet console, full logs available
  - Cons: Requires --log-to-file also enabled

**Epic Reference:** DISCOVERY.md mentioned --silent as derived requirement, no user specification

**Recommendation:** Option B (suppress INFO/DEBUG only) - safety over silence

**User Answer:**


**Impact on spec.md:** Will add --silent behavior to Requirement 1

---

### Question 4: --log-to-file File Location

**Context:** When --log-to-file enabled, where should log file be created?

**Why uncertain:** constants.py has LOGGING_FILE = './data/log.txt' but user may prefer different location

**Options:**
- **Option A:** Use constants.py default ('./data/log.txt')
  - Pros: Consistent with existing code
  - Cons: Logs mixed with data files
  
- **Option B:** Create logs/ directory at project root
  - Pros: Organized separation
  - Cons: New directory to create/manage

- **Option C:** Make log file path an additional argument (--log-file)
  - Pros: Fully configurable
  - Cons: Another argument to add

**Epic Reference:** constants.py line 27 has existing path, but no user preference stated

**Recommendation:** Option A (use existing default) - least complexity

**User Answer:**


**Impact on spec.md:** Will document log file location in Requirement 1 or 4

---

### Question 5: Invalid --mode Error Messaging

**Context:** When user provides invalid --mode value (e.g., --mode 99), what should happen?

**Why uncertain:** User preference for error messages not specified

**Options:**
- **Option A:** Print error + show full help (argparse default)
  - Pros: Maximum guidance for user
  - Cons: Verbose output
  
- **Option B:** Print error + show just --mode usage
  - Pros: Focused guidance
  - Cons: Requires custom error handler

- **Option C:** Print error only, no help
  - Pros: Minimal output
  - Cons: User must run --help separately

**Epic Reference:** No guidance on error message verbosity

**Recommendation:** Option B (error + mode usage) - helpful but not overwhelming

**User Answer:**


**Impact on spec.md:** Will add validation section to Requirement 2

---

## Resolved Questions

### Question 1: E2E Test Data Selection
- [x] **RESOLVED:** Option B - Use dynamic test data

**User's Answer:**
User selected Option B (dynamic test data approach)

**Implementation Impact:**
- E2E tests will use dynamic selection (highest-ranked QB, any valid trade, etc.)
- Added to spec.md as "E2E Test Data Strategy" under R3
- Ensures tests remain valid across seasons when player rosters change

**Updated:** 2026-01-30 23:05
**Spec Updated:** Yes - R3 now includes E2E Test Data Strategy section

---

### Question 2: E2E Mode Error Handling
- [x] **RESOLVED:** Option B - Continue through all modes, report all failures

**User's Answer:**
User selected Option B (continue through all 5 modes)

**Implementation Impact:**
- E2E mode tracks each mode's result independently
- All 5 modes execute regardless of individual failures
- Final report lists all failures
- Exit code 0 = all pass, 1 = any failed
- Added to spec.md as "E2E Error Handling Strategy" under R3

**Updated:** 2026-01-30 23:08
**Spec Updated:** Yes - R3 now includes E2E Error Handling Strategy section

---

### Question 3: --silent Flag Behavior
- [x] **RESOLVED:** Option B - Suppress INFO/DEBUG, show WARNING/ERROR

**User's Answer:**
User selected Option B (suppress INFO/DEBUG only)

**Implementation Impact:**
- --silent sets logging level to WARNING
- INFO and DEBUG messages suppressed
- WARNING and ERROR still visible
- Does not affect --log-to-file behavior
- Added to spec.md as "--silent Flag Behavior" under R1

**Updated:** 2026-01-30 23:10
**Spec Updated:** Yes - R1 now includes --silent Flag Behavior section

---

### Question 4: --log-to-file File Location
- [x] **RESOLVED:** Option B - Create logs/ directory at project root

**User's Answer:**
User selected Option B with additional context: wants it clear where log came from and when. The old log.txt setup needs updating.

**Implementation Impact:**
- Create `logs/` directory at project root (auto-create if doesn't exist)
- Log filename format: `logs/league_helper_YYYYMMDD_HHMMSS.log`
- Includes script name and timestamp for clarity
- Replaces old `./data/log.txt` approach
- Added to spec.md as "--log-to-file Location" under R1

**Updated:** 2026-01-30 23:12
**Spec Updated:** Yes - R1 now includes --log-to-file Location section

---

### Question 5: Invalid --mode Error Messaging
- [x] **RESOLVED:** Option B - Print error + show just --mode usage

**User's Answer:**
User selected Option B (focused error message with --mode usage)

**Implementation Impact:**
- Custom error handler for --mode validation
- Error format: "error: invalid mode: 'X'. Valid modes: 1-5 or 'all'"
- Show --mode usage line (not full help)
- Exit code 2 (argparse convention)
- Added to spec.md as "Invalid --mode Error Handling" under R2

**Updated:** 2026-01-30 23:14
**Spec Updated:** Yes - R2 now includes Invalid --mode Error Handling section

---

## Notes

**Question Quality Check:**
- All questions are about user preferences/decisions (not research gaps)
- All questions have clear options with tradeoffs
- All questions cite why they're uncertain
- All questions explain impact on spec

**Next Steps:**
1. User answers questions above
2. Agent updates spec.md with answers
3. Agent marks questions [x] resolved
4. Agent proceeds to Phase 2.5 (Spec Alignment Check)
