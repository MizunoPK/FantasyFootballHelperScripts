# Epic Final Review Examples - Stage 6c

**Purpose:** Common mistakes, real-world examples, and best practices for Stage 6c
**When to Use:** Reference while completing epic_final_review.md workflow
**Main Guide:** `stages/stage_6/epic_final_review.md`

---

## Overview

This reference provides practical examples for Stage 6c (Epic Final Review):

**Common Mistakes (7 anti-patterns to avoid)**
**Real-World Example (complete epic final review walkthrough)**
**Best Practices (what good looks like)**

Use these examples to avoid common pitfalls and ensure thorough epic-level validation.

---

## Common Mistakes to Avoid

### ❌ MISTAKE 1: "Repeating feature-level PR review at epic level"

**Why this is wrong:**
- Stage 5c already did feature-level PR review for each feature
- Stage 6c focuses on EPIC-WIDE concerns (cross-feature impacts)
- Repeating feature-level checks wastes time

**What to do instead:**
- ✅ Focus on epic-wide architectural consistency
- ✅ Review cross-feature impacts (not individual features)
- ✅ Validate design patterns applied consistently
- ✅ Check for duplicated code BETWEEN features (not within)

**Example:**
```
BAD: Reviewing Feature 01's code quality in isolation
GOOD: Comparing code quality ACROSS all features (consistency check)

BAD: Checking if Feature 01 has unit tests
GOOD: Checking if epic-level integration tests exist (cross-feature scenarios)
```

---

### ❌ MISTAKE 2: "Fixing issues inline and continuing Stage 6"

**Why this is wrong:**
- Bug fixes may affect areas already checked in Stage 6
- Cannot assume previous QC results still valid
- Partial Stage 6 completion creates gaps in validation

**What to do instead:**
- ✅ Document ALL issues in epic_lessons_learned.md
- ✅ Create bug fixes using bug fix workflow (Stage 2 → 5a → 5b → 5c)
- ✅ COMPLETELY RESTART Stage 6 after fixes (from STAGE_6a)
- ✅ Re-run ALL steps (smoke testing, QC 1-3, PR review)

**Example:**
```
BAD:
- Find architectural issue in Step 6.9
- Fix it with quick code change
- Continue to Step 8 (Final Verification)

GOOD:
- Find architectural issue in Step 6.9
- Document in epic_lessons_learned.md
- Create bugfix_high_architecture_inconsistency/
- Run bug fix through Stage 2 → 5a → 5b → 5c
- RESTART Stage 6 from STAGE_6a (smoke testing)
- Re-run STAGE_6a, 6b, 6c (all steps)
- Only then proceed to Stage 7
```

---

### ❌ MISTAKE 3: "Skipping Architecture category review"

**Why this is wrong:**
- Architecture (Step 6.9) is the MOST IMPORTANT category for epic-level review
- Architectural inconsistencies cause long-term maintainability issues
- Missing this check means shipping brittle epic

**What to do instead:**
- ✅ Spend EXTRA time on Architecture category (Step 6.9)
- ✅ Verify design patterns consistent across ALL features
- ✅ Check for architectural inconsistencies (Manager vs functions, classes vs modules)
- ✅ Validate interfaces between features are clean

**Example:**
```
BAD:
✅ Correctness: PASS
✅ Code Quality: PASS
✅ Architecture: PASS (didn't check, assumed consistent)

GOOD:
✅ Correctness: PASS (verified cross-feature workflows)
✅ Code Quality: PASS (checked consistency across features)
✅ Architecture: PASS (verified Manager pattern used in ALL features)
  - Feature 01: ADPManager ✅
  - Feature 02: MatchupManager ✅
  - Feature 03: PerformanceTracker ✅
  - Design pattern: Manager pattern used consistently ✅
```

---

### ❌ MISTAKE 4: "Comparing to specs instead of original epic request"

**Why this is wrong:**
- Specs evolved during implementation (may have scope creep)
- Specs may have deviated from user's original vision
- Step 6.11 (Scope & Changes) validates against USER'S GOALS, not intermediate specs

**What to do instead:**
- ✅ Re-read ORIGINAL {epic_name}.txt file
- ✅ Validate against user's stated goals (from epic notes)
- ✅ Verify expected outcomes delivered (from user's perspective)
- ✅ Check for scope creep (features not in original request)

**Example:**
```
BAD:
- Check if Feature 01 matches feature_01/spec.md ✅
- Mark Scope & Changes as PASS

GOOD:
- Re-read integrate_new_player_data_into_simulation.txt
- User requested: "Integrate ADP data" ✅
- User requested: "Add matchup projections" ✅
- User requested: "Track performance" ✅
- Epic delivered all 3 ✅
- No undocumented features added ✅
- Mark Scope & Changes as PASS
```

---

### ❌ MISTAKE 5: "Accepting low priority issues instead of creating bug fixes"

**Why this is wrong:**
- "Low priority" issues accumulate and degrade epic quality
- Architectural inconsistencies labeled "low" are often HIGH impact
- Deferring issues means they may never get fixed

**What to do instead:**
- ✅ Use priority determination correctly:
  - **HIGH:** Breaks functionality, security, architecture, performance >100% regression
  - **MEDIUM:** Affects quality (consistency, error messages, minor performance)
  - **LOW:** Cosmetic only (comments, variable names)
- ✅ Create bug fixes for HIGH and MEDIUM issues
- ✅ Only defer LOW issues (truly cosmetic)

**Example:**
```
BAD:
Issue: Feature 01 uses Manager pattern, Feature 02 uses functions
Priority: low (it works, just inconsistent)
Action: Document, don't fix

GOOD:
Issue: Feature 01 uses Manager pattern, Feature 02 uses functions
Priority: HIGH (architectural inconsistency, maintainability impact)
Action: Create bugfix_high_architecture_inconsistency
```

---

### ❌ MISTAKE 6: "Not documenting PR review results"

**Why this is wrong:**
- Future agents can't see what was reviewed
- Can't prove epic was thoroughly reviewed
- Lessons learned lost (can't improve process)

**What to do instead:**
- ✅ Document PR review results in epic_lessons_learned.md (Step 6.12)
- ✅ Include: Date, reviewer, epic name, all 11 categories, status, notes
- ✅ If issues found: Document issues, bug fixes created, restart log
- ✅ Update EPIC_README.md with review completion

**Example:**
```
BAD:
- Complete PR review mentally
- Mark Step 6 as complete
- Proceed to Step 8

GOOD:
- Complete PR review (all 11 categories)
- Document results in epic_lessons_learned.md:
  ## Stage 6c - Epic PR Review (11 Categories)
  **Date:** 2025-01-02
  **Overall Status:** ✅ APPROVED
  **Issues Found:** 0
- Update EPIC_README.md: "Epic PR review: ✅ PASSED"
- Proceed to Step 8
```

---

### ❌ MISTAKE 7: "Proceeding to Stage 7 with pending issues"

**Why this is wrong:**
- Stage 7 is final cleanup (commits, merge to main, move to done/)
- Cannot commit epic with known issues
- User will find issues after "completion"

**What to do instead:**
- ✅ Verify NO pending issues before Step 8 (Final Verification)
- ✅ All bug fixes must be COMPLETE (Stage 5c)
- ✅ Stage 6 must be RESTARTED after bug fixes
- ✅ Only proceed to Stage 7 when verification checklist 100% complete

**Example:**
```
BAD:
Step 8.1: Verification Checklist
- ✅ Epic smoke testing passed
- ✅ QC rounds passed
- ✅ Epic PR review passed
- ⚠️ 1 pending bug fix (bugfix_high_performance - Stage 5b)
- ✅ Tests passing
→ Proceed to Stage 7 anyway

GOOD:
Step 8.1: Verification Checklist
- ✅ Epic smoke testing passed
- ✅ QC rounds passed
- ✅ Epic PR review passed
- ⚠️ 1 pending bug fix (bugfix_high_performance - Stage 5b)
→ STOP - Cannot proceed
→ Complete bug fix (finish Stage 5c)
→ RESTART Stage 6 from STAGE_6a
→ Re-run all steps
→ Re-verify checklist (all items ✅)
→ Then proceed to Stage 7
```

---

## Real-World Example

### Example: Epic Final Review for "Improve Draft Helper" Epic

**Context:**
- Epic: Improve Draft Helper
- Features: 3 (ADP Integration, Matchup System, Performance Tracking)
- STAGE_6a complete: Epic smoke testing passed
- STAGE_6b complete: QC Rounds 1, 2, 3 passed
- Now starting STAGE_6c: Epic Final Review

---

**STEP 6: Epic PR Review (11 Categories)**

**Step 6.1: Correctness (Epic Level)**

```python
# Verify cross-feature workflow correctness
from feature_01.adp_manager import ADPManager
from feature_02.matchup_manager import MatchupManager
from league_helper.util.FantasyPlayer import FantasyPlayer

# Test integration correctness
adp_mgr = ADPManager(data_folder=Path("data"))
matchup_mgr = MatchupManager(data_folder=Path("data"))

player = FantasyPlayer("Patrick Mahomes", "QB", 300.0)
adp_mult, adp_rank = adp_mgr.get_adp_data("Patrick Mahomes")
matchup_diff = matchup_mgr.get_matchup_difficulty("Patrick Mahomes", week=5)

final_score = player.score * adp_mult * matchup_diff
# Verify: 300 * 1.2 * 0.9 = 324
assert 320 <= final_score <= 330, "Integration calculation incorrect"
```

**Result:** ✅ PASS (all cross-feature workflows correct)

---

**Step 6.9: Architecture (Epic Level - CRITICAL)**

```python
# Check architectural consistency
# Feature 01:
class ADPManager:  # ✅ Manager pattern
    def __init__(self, data_folder: Path):
        self.data_folder = data_folder

# Feature 02:
def get_matchup_difficulty(player_name: str, week: int) -> float:  # ❌ Standalone function
    # ...

# Feature 03:
class PerformanceTracker:  # ✅ Manager pattern
    def __init__(self, data_folder: Path):
        self.data_folder = data_folder
```

**Result:** ❌ FAIL - Architectural inconsistency

**Issue:** Feature 02 uses standalone functions instead of Manager pattern

---

**Step 6.12: Document PR Review Results**

```markdown
## Stage 6c - Epic PR Review (11 Categories)

**Date:** 2025-01-02
**Reviewer:** Claude Agent
**Epic:** improve_draft_helper

**Review Results:**

| Category | Status | Notes |
|----------|--------|-------|
| 1. Correctness | ✅ PASS | Cross-feature workflows correct |
| 2. Code Quality | ✅ PASS | Consistent quality across features |
| 3. Comments & Docs | ✅ PASS | Epic-level docs complete |
| 4. Organization | ✅ PASS | Consistent structure |
| 5. Testing | ✅ PASS | Epic integration tests exist, 100% pass |
| 6. Security | ✅ PASS | No vulnerabilities |
| 7. Performance | ✅ PASS | 3.2s (acceptable) |
| 8. Error Handling | ✅ PASS | Consistent, graceful degradation |
| 9. Architecture | ❌ FAIL | Feature 02 uses functions instead of Manager pattern |
| 10. Compatibility | ✅ PASS | No breaking changes |
| 11. Scope | ✅ PASS | Matches original request |

**Overall Status:** ❌ REJECTED

**Issues Found:** 1

**Issue 1: Architectural Inconsistency (Category 9: Architecture)**
- Feature 01 and 03 use Manager pattern, Feature 02 uses standalone functions
- Impact: HIGH - Architectural inconsistency
- Fix Required: Refactor Feature 02 to MatchupManager class

**Next Action:** Create bug fix, then RESTART Stage 6
```

---

**STEP 7: Handle Issues**

**Step 7.1: Document Issues**

```markdown
## Stage 6c Issues Found

**Date:** 2025-01-02

**Issue 1: Architectural Inconsistency in Feature 02**
- **Discovered In:** Step 6.9 (Epic PR Review - Architecture)
- **Description:** Feature 02 uses standalone functions, Features 01 and 03 use Manager pattern
- **Impact:** HIGH - Architectural inconsistency makes epic hard to maintain
- **Root Cause:** Different implementation approach for Feature 02
- **Fix Required:** Refactor Feature 02 to MatchupManager class
- **Priority:** high
```

**Step 7.2: Determine Priority**

```markdown
## Issue Prioritization

**HIGH priority (create bug fixes now):**
- Issue 1: Architectural inconsistency → bugfix_high_architecture_inconsistency
```

**Step 7.3: Present to User**

```markdown
I found 1 issue during Stage 6c Epic PR Review that requires a bug fix:

**ISSUE 1: Architectural Inconsistency (HIGH priority)**
- **Problem:** Feature 02 uses standalone functions instead of Manager pattern
- **Impact:** Architectural inconsistency makes epic hard to maintain
- **Fix:** Refactor Feature 02 to MatchupManager class
- **Estimated time:** 2-3 hours (Stage 2 → 5a → 5b → 5c)

After fixing, I'll RESTART Stage 6 from STAGE_6a.

Should I proceed?
```

**Step 7.4: Create Bug Fix**

```
bugfix_high_architecture_inconsistency/
├── notes.txt ("Refactor Feature 02 to Manager pattern")
├── spec.md (bug fix specification)
├── implementation_plan.md (refactoring tasks)
├── code_changes.md (actual code changes)
└── lessons_learned.md (what we learned)
```

**Run through:** Stage 2 → 5a → 5b → 5c (bug fix complete)

**Step 7.5: RESTART Stage 6**

```markdown
## Stage 6 Restart Log

**Restart Date:** 2025-01-02
**Reason:** 1 bug fix completed (bugfix_high_architecture_inconsistency)

**Bug Fix:** Refactored Feature 02 to MatchupManager class

**Restart Actions:**
- ✅ Re-ran STAGE_6a: Epic Smoke Testing (all 4 parts) - PASSED
- ✅ Re-ran STAGE_6b: QC Round 1 - PASSED
- ✅ Re-ran STAGE_6b: QC Round 2 - PASSED
- ✅ Re-ran STAGE_6b: QC Round 3 - PASSED
- ✅ Re-ran STAGE_6c: Epic PR Review (all 11 categories) - PASSED
  - Architecture category now PASSED (all features use Manager pattern)

**Result:** Stage 6 complete after restart (no new issues)
```

---

**STEP 8: Final Verification**

**Step 8.1: Verify All Issues Resolved**

```markdown
## Stage 6c Final Verification

**Date:** 2025-01-02 16:00

**Verification Results:**
- ✅ Epic smoke testing passed
- ✅ QC Round 1 passed
- ✅ QC Round 2 passed
- ✅ QC Round 3 passed
- ✅ Epic PR review passed (all 11 categories, including Architecture)
- ✅ NO pending issues or bug fixes
- ✅ ALL tests passing (2247/2247 tests)

**Result:** Stage 6 verification PASSED
```

**Step 8.2: Update EPIC_README.md**

```markdown
## Epic Progress Tracker

**Stage 6 - Epic Final QC:** ✅ COMPLETE
- Epic smoke testing passed: ✅
- Epic QC rounds passed: ✅ (Rounds 1, 2, 3)
- Epic PR review passed: ✅ (11 categories)
- Issues found: 1 (architectural inconsistency - resolved)
- Bug fixes completed: 1
- Stage 6 restarts: 1 (after bug fix)
- Date completed: 2025-01-02
```

**Step 8.3: Update epic_lessons_learned.md**

```markdown
## Stage 6c Lessons Learned (Epic Final Review)

**What Went Well:**
- Architectural consistency check caught Manager pattern inconsistency
- Bug fix workflow smooth (2-3 hours to refactor Feature 02)
- Stage 6 restart ensured quality maintained

**Issues Found & Resolved:**
1. **Architectural Inconsistency:** Feature 02 used standalone functions instead of Manager pattern
   - Fixed: Refactored to MatchupManager class
   - Prevention: Add "Architecture Pattern" to Stage 2 spec template

**Insights for Future Epics:**
- Establish architectural patterns early (Stage 2)
- Document patterns in EPIC_README.md
- Review architectural consistency after EACH feature (Stage 5d)
```

**Step 8.4: Update Agent Status**

```markdown
## Agent Status

**Current Stage:** Stage 6c - Epic Final Review
**Status:** ✅ COMPLETE
**Completed:** 2025-01-02 16:15

**Stage 6 Summary:**
- Epic PR review: ✅ PASSED (11 categories)
- Issues found: 1 (architectural inconsistency - resolved)
- Bug fixes completed: 1
- Stage 6 restarts: 1
- All tests passing: ✅ (2247/2247)

**Next Stage:** stages/stage_7/epic_cleanup.md
```

---

## Best Practices Summary

### What Good Looks Like

**Epic-Level Focus (Not Feature-Level):**
- ✅ Review cross-feature consistency
- ✅ Check architectural patterns across all features
- ✅ Validate epic-wide integration points
- ❌ Don't re-review individual feature correctness

**Thorough Architecture Review:**
- ✅ Spend extra time on Architecture category (Step 6.9)
- ✅ Verify design patterns consistent
- ✅ Check for pattern inconsistencies between features
- ❌ Don't assume architecture is consistent

**Proper Issue Handling:**
- ✅ Document ALL issues comprehensively
- ✅ Create bug fixes using full workflow
- ✅ RESTART Stage 6 completely after fixes
- ❌ Don't fix issues inline and continue

**Validate Against Original Request:**
- ✅ Re-read {epic_name}.txt
- ✅ Verify user's goals achieved
- ✅ Check for scope creep
- ❌ Don't just compare to evolved specs

**Complete Documentation:**
- ✅ Document PR review results
- ✅ Document all issues found
- ✅ Document restart log (if applicable)
- ✅ Update EPIC_README.md and epic_lessons_learned.md
- ❌ Don't skip documentation

**Zero Issues Before Stage 7:**
- ✅ Verify ALL issues resolved
- ✅ All bug fixes complete (Stage 5c)
- ✅ 100% test pass rate
- ❌ Don't proceed to Stage 7 with pending issues

---

## Quick Reference: Stage 6c Steps

**STEP 6: Epic PR Review**
- Apply 11-category checklist to epic-wide changes
- Focus on Architecture (Step 6.9) - most important
- Document results in epic_lessons_learned.md

**STEP 7: Handle Issues (if issues found)**
- Document all issues
- Prioritize (HIGH/MEDIUM create bug fixes, LOW document only)
- Create bug fixes using full workflow
- RESTART Stage 6 from STAGE_6a after fixes

**STEP 8: Final Verification**
- Verify all issues resolved
- Update EPIC_README.md (Epic Progress Tracker, Agent Status)
- Update epic_lessons_learned.md with insights
- Confirm ready for Stage 7

---

**See Also:**
- Main Guide: `stages/stage_6/epic_final_review.md`
- PR Review Checklist: `reference/stage_6/epic_pr_review_checklist.md`
- Templates: `reference/stage_6/epic_final_review_templates.md`

---

**END OF EPIC FINAL REVIEW EXAMPLES**
