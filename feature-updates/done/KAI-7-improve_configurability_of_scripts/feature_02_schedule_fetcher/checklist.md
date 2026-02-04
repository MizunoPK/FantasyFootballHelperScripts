# Feature 02 Checklist: schedule_fetcher Configurability

**Feature:** feature_02_schedule_fetcher
**Created:** 2026-01-29
**Status:** PENDING USER APPROVAL

---

## Open Questions

### Functional Questions

#### Question 1: Debug Mode Weeks Reduction

**Context:**
Debug mode should enable DEBUG logging + behavioral changes (per User Answer Q4 from Discovery). For schedule fetcher, behavioral change could mean reducing weeks fetched for faster debugging cycles.

**Current Behavior:**
- Normal mode: Fetches weeks 1-18 (full regular season)
- Time: ~4-5 seconds with 0.2s rate limiting between weeks

**Options:**

**Option A: No weeks reduction (fetch full 1-18)**
- **Pros:** Complete data even in debug mode, consistent behavior
- **Cons:** Debug runs take same time as normal (~4-5 sec), defeats purpose of "faster debugging"

**Option B: Reduce to weeks 1-2**
- **Pros:** Very fast (~0.5 sec), demonstrates schedule fetching works, includes week data variety
- **Cons:** Incomplete season data, bye weeks not visible

**Option C: Configurable via --debug-weeks argument**
- **Pros:** Maximum flexibility, user controls week range
- **Cons:** More complex, additional argument to document/test

**Epic Reference:**
- User Answer Q4: "Debug mode = behavioral changes + logging"
- Discovery doesn't specify what behavioral changes for schedule fetcher

**Recommendation:** **Option B (weeks 1-2)**

**Reasoning:**
1. Aligns with "faster debugging" intent from Discovery
2. Demonstrates API fetching, parsing, and CSV export
3. Simple implementation (no additional arguments)
4. Consistent with other fetchers' debug modes (minimal data subset)

**Impact on spec.md:**
- If Option A: No changes needed
- If Option B: Update R2, Algorithm 2 (weeks = range(1, 3) in debug mode)
- If Option C: Add --debug-weeks argument to R1, update parse_arguments algorithm

**User Answer:**
**Option: Custom (6 weeks)** - Debug mode fetches weeks 1-6 to include bye weeks

**Answered:** 2026-01-30
**Reasoning:** 6 weeks provides enough data to test bye week detection while keeping debug runs reasonably fast (~1.5 seconds vs 4-5 seconds for full season)

**Impact on spec.md:**
- Update R2 (Debug Mode Behavior): weeks = range(1, 7) in debug mode
- Update Algorithm 2: Add debug mode case with weeks 1-6

---

#### Question 2: E2E Test Validation Criteria

**Context:**
E2E test mode fetches week 1 schedule. Need to determine what constitutes a "passing" test beyond exit code 0.

**Epic Reference:**
- User Answer Q5: "Tests check exit code AND verify expected outcomes (specific logs, result counts)"
- Discovery specifies integration tests validate specific outcomes, not just exit code

**Options:**

**Option A: Exit code 0 only**
- **Pros:** Simplest, relies on exception handling
- **Cons:** Doesn't validate actual data fetched, could pass with empty schedule

**Option B: Exit code + verify >0 games fetched in week 1**
- **Pros:** Validates API returned data, catches empty response errors
- **Cons:** Doesn't validate all teams present (bye week detection not tested)

**Option C: Exit code + verify all 32 teams present in week 1**
- **Pros:** Most thorough, validates complete schedule structure
- **Cons:** Will fail if any team has week 1 bye (rare but possible), overly strict

**Recommendation:** **Option B (exit code + >0 games)**

**Reasoning:**
1. Aligns with User Answer Q5 (validate specific outcomes)
2. Week 1 typically has 14-16 games (all teams play), so >0 is safe check
3. More meaningful than exit code alone
4. Not overly strict (doesn't require all 32 teams)
5. Fast to validate (simple len(schedule[1]) > 0 check)

**Impact on spec.md:**
- If Option A: No validation code in Algorithm 2
- If Option B: Add validation in Algorithm 2 (if len(schedule[1]) == 0 → fail)
- If Option C: Add team count validation (check all 32 teams present)

**User Answer:**
**Option C** - Exit code + verify all 32 teams present in week 1

**Answered:** 2026-01-30
**Reasoning:** Most thorough validation, ensures complete schedule structure is fetched

**Impact on spec.md:**
- Update R3 (E2E Test Mode Behavior): Add team count validation (verify all 32 teams present)
- Update Algorithm 2: Add validation logic to check len(set(all teams)) == 32

---

### Technical Questions

(None - all technical details researched in S2.P1)

---

### Integration Questions

(None - feature is independent, no integration concerns)

---

### Error Handling Questions

(None - existing error handling in ScheduleFetcher is sufficient)

---

### Testing Questions

(None - test approach clear from Discovery User Answer Q5)

---

### Dependencies & Blockers

(None - all dependencies verified in research)

---

## Question Summary

**Total Questions:** 2
- Functional: 2
- Technical: 0
- Integration: 0
- Error Handling: 0
- Testing: 0
- Dependencies: 0

**Status:**
- Open: 0
- Answered: 2
- Resolved: 2

---

## User Approval

**Approval Status:** ✅ APPROVED (Gate 2 PASSED)
**Approved Date:** 2026-01-30
**Approved By:** User

**Gate 2 Status:** PASSED
**All questions answered:** 2/2 complete
**User Comments:** Q1 = 6 weeks (custom), Q2 = Option C (all 32 teams)

**Next Action:** Update spec.md with user answers, proceed to S2.P3 Refinement Phase

---

## Notes

**Why Only 2 Questions:**
Research Phase (S2.P1) was thorough and answered most technical questions:
- Component structure researched (run_schedule_fetcher.py, ScheduleFetcher.py)
- Existing patterns identified (run_game_data_fetcher.py argparse pattern)
- Data structures documented (ESPN API response, CSV schema)
- Edge cases identified (WAS→WSH normalization, bye weeks)

Questions here are genuine user preferences, not research gaps.
