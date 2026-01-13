# Epic Final Review Templates - S9.P3

**Purpose:** Templates for documenting S9.P3 results and lessons learned
**When to Use:** Steps 6-8 of epic_final_review.md workflow
**Main Guide:** `stages/s9/s6_p4_epic_final_review.md`

---

## Overview

This reference provides all templates needed during S9.P3 (Epic Final Review):

**Step 6 Templates:**
- Epic PR Review Results (documenting review outcome)

**Step 7 Templates:**
- Issues Found Documentation (epic_lessons_learned.md)
- Issue Prioritization (determining bug fix priorities)
- User Presentation (presenting issues for approval)
- Bug Fix Folder Structure (creating bug fix folders)
- Restart Documentation (documenting S9 restart)

**Step 8 Templates:**
- Final Verification Checklist (verifying completion)
- Epic Progress Tracker Update (EPIC_README.md)
- S9.P3 Lessons Learned (insights and improvements)
- Agent Status Update (EPIC_README.md)

---

## Template 1: Epic PR Review Results (Step 6)

**Purpose:** Document PR review outcome in epic_lessons_learned.md
**When to Use:** After completing Step 6 (Epic PR Review)
**Location:** Add to `KAI-{N}-{epic_name}/epic_lessons_learned.md`

### Basic Template

```markdown
## S9.P3 - Epic PR Review Results

**Date:** {YYYY-MM-DD}
**Epic:** {epic_name}
**Review Rounds:** {N} rounds total
**Final Status:** PASSED (2 consecutive clean rounds achieved)

**Review Summary:**
- Round 1 (Specialized): {brief summary of findings}
- Round 2+ (Comprehensive): {brief summary of iterations}
- Total issues found and fixed: {count}
- Epic-level concerns addressed: {list any architectural/integration fixes}

**pr_review_issues.md file:** `KAI-{N}-{epic_name}/pr_review_issues.md`

**Epic is ready for Step 8 (Final Verification)**
```

### Example (Completed Review)

```markdown
## S9.P3 - Epic PR Review Results

**Date:** 2025-01-02
**Epic:** integrate_new_player_data_into_simulation
**Review Rounds:** 3 rounds total
**Final Status:** PASSED (Rounds 2-3 both clean)

**Review Summary:**
- Round 1a (Code Quality): Found 2 issues (duplication between features) - Fixed
- Round 1b (Test Coverage): Found 1 issue (missing epic integration test) - Fixed
- Round 1c (Security): No issues
- Round 1d (Documentation): No issues
- Round 2 (Comprehensive): 0 issues found ✅
- Round 3 (Comprehensive): 0 issues found ✅

**Total issues found and fixed:** 3
**Epic-level concerns addressed:** Extracted shared CSV loading logic to utils/csv_utils.py, added epic integration test

**pr_review_issues.md file:** `KAI-3-integrate_new_player_data_into_simulation/pr_review_issues.md`

**Epic is ready for Step 8 (Final Verification)**
```

---

## Template 2: Issues Found Documentation (Step 7.1)

**Purpose:** Document all issues discovered during Step 6
**When to Use:** When ANY category fails in Step 6 PR review
**Location:** Add to `KAI-{N}-{epic_name}/epic_lessons_learned.md`

### Template

```markdown
## S9.P3 Issues Found

**Date:** {YYYY-MM-DD}

**Issue 1: {Issue Name}**
- **Discovered In:** Step 6.{N} (Epic PR Review - {Category})
- **Description:** {What is the problem?}
- **Impact:** {HIGH/MEDIUM/LOW} - {Why does it matter?}
- **Root Cause:** {Why did this happen?}
- **Fix Required:** {What needs to be done?}
- **Priority:** {high/medium/low}

**Issue 2: {Issue Name}**
- **Discovered In:** Step 6.{N} (Epic PR Review - {Category})
- **Description:** {What is the problem?}
- **Impact:** {HIGH/MEDIUM/LOW} - {Why does it matter?}
- **Root Cause:** {Why did this happen?}
- **Fix Required:** {What needs to be done?}
- **Priority:** {high/medium/low}

[Repeat for all issues found]
```

### Example (Multiple Issues)

```markdown
## S9.P3 Issues Found

**Date:** 2025-01-02

**Issue 1: Architectural Inconsistency**
- **Discovered In:** Step 6.9 (Epic PR Review - Architecture)
- **Description:** Feature 01 uses Manager class pattern, Feature 02 uses standalone functions
- **Impact:** HIGH - Architectural inconsistency makes epic hard to maintain
- **Root Cause:** Different agents implemented features with different patterns
- **Fix Required:** Refactor Feature 02 to Manager pattern (MatchupManager class)
- **Priority:** high

**Issue 2: Performance Regression**
- **Discovered In:** Step 6.7 (Epic PR Review - Performance)
- **Description:** Epic execution time 12.5s (baseline 2.5s, +400% regression)
- **Impact:** HIGH - Unacceptable performance for user
- **Root Cause:** N+1 queries in Feature 02 (loading matchup data per player in loop)
- **Fix Required:** Implement batch loading for matchup data
- **Priority:** high

**Issue 3: Inconsistent Error Messages**
- **Discovered In:** Step 6.8 (Epic PR Review - Error Handling)
- **Description:** Feature 01 uses "Player not found", Feature 02 uses "No player data"
- **Impact:** LOW - User confusion but not functional
- **Root Cause:** Different error message templates
- **Fix Required:** Standardize error messages to "Player '{name}' not found in {feature} data"
- **Priority:** medium
```

---

## Template 3: Issue Prioritization (Step 7.2)

**Purpose:** Determine which issues require bug fixes vs documentation only
**When to Use:** After documenting all issues in Step 7.1
**Location:** Add to `KAI-{N}-{epic_name}/epic_lessons_learned.md` or work notes

### Template

```markdown
## Issue Prioritization

**HIGH priority (create bug fixes now):**
- Issue {N}: {Brief description} → bugfix_high_{name}
- Issue {N}: {Brief description} → bugfix_high_{name}

**MEDIUM priority (create bug fixes after high):**
- Issue {N}: {Brief description} → bugfix_medium_{name}

**LOW priority (document only, no bug fix):**
- Issue {N}: {Brief description} (documented for future improvement)
```

### Priority Guidelines

**HIGH Priority - Create Bug Fix Immediately:**
- Issue breaks epic functionality OR unacceptable quality
- Epic won't work correctly
- User-facing failures
- Architectural inconsistencies
- Security vulnerabilities
- Performance regressions >100%

**MEDIUM Priority - Create Bug Fix After High:**
- Issue affects quality but not functionality
- Inconsistencies (error messages, code style)
- Minor performance issues (<100% regression)
- Incomplete documentation

**LOW Priority - Document Only:**
- Issue is cosmetic or minor
- Code style nitpicks
- Optional refactoring
- Nice-to-have improvements

### Example

```markdown
## Issue Prioritization

**HIGH priority (create bug fixes now):**
- Issue 1: Architectural inconsistency → bugfix_high_architecture_inconsistency
- Issue 2: Performance regression → bugfix_high_performance_regression

**MEDIUM priority (create bug fixes after high):**
- Issue 3: Inconsistent error messages → bugfix_medium_error_messages

**LOW priority (document only, no bug fix):**
- None identified
```

---

## Template 4: User Presentation (Step 7.3)

**Purpose:** Present issues to user for approval before creating bug fixes
**When to Use:** After prioritizing issues, before creating bug fixes
**Format:** Present directly to user (not in a file)

### Template

```markdown
I found {number} issues during S9.P3 Epic PR Review that require bug fixes:

**ISSUE 1: {Issue Name} ({PRIORITY} priority)**
- **Problem:** {Brief description of the issue}
- **Impact:** {Why it matters}
- **Fix:** {What will be done}
- **Estimated time:** {X-Y hours (bug fix workflow: S2 → 5a → 5b → 5c)}

**ISSUE 2: {Issue Name} ({PRIORITY} priority)**
- **Problem:** {Brief description of the issue}
- **Impact:** {Why it matters}
- **Fix:** {What will be done}
- **Estimated time:** {X-Y hours}

[Repeat for all high/medium priority issues]

After fixing these issues, I'll need to RESTART S9 from the beginning (S9.P1 smoke testing) to ensure the fixes didn't introduce new issues.

Should I proceed with creating these bug fixes?
```

### Example

```markdown
I found 2 issues during S9.P3 Epic PR Review that require bug fixes:

**ISSUE 1: Architectural Inconsistency (HIGH priority)**
- **Problem:** Feature 01 uses Manager class pattern, Feature 02 uses standalone functions
- **Impact:** Architectural inconsistency makes epic hard to maintain
- **Fix:** Refactor Feature 02 to Manager pattern (MatchupManager class)
- **Estimated time:** 2-3 hours (bug fix workflow: S2 → 5a → 5b → 5c)

**ISSUE 2: Performance Regression (HIGH priority)**
- **Problem:** Epic execution time 12.5s (baseline 2.5s, +400% regression)
- **Impact:** Unacceptable performance for user
- **Fix:** Implement batch loading for matchup data in Feature 02
- **Estimated time:** 1-2 hours

After fixing these issues, I'll need to RESTART S9 from the beginning (S9.P1 smoke testing) to ensure the fixes didn't introduce new issues.

Should I proceed with creating these bug fixes?
```

**Wait for user approval before proceeding to Step 7.4.**

---

## Template 5: Bug Fix Folder Structure (Step 7.4)

**Purpose:** Create bug fix folders with proper structure
**When to Use:** Step 7.4 when creating bug fixes for issues
**Location:** `KAI-{N}-{epic_name}/bugfix_{priority}_{name}/`

### Folder Structure

```
bugfix_{priority}_{name}/
├── notes.txt                    (User-provided bug description)
├── README.md                    (Agent Status during bug fix)
├── spec.md                      (Bug fix specification)
├── checklist.md                 (Open questions)
├── implementation_plan.md       (Implementation approach)
├── code_changes.md              (Actual changes made)
└── lessons_learned.md           (Bug fix retrospective)
```

### notes.txt Template

```markdown
# Bug Fix: {Issue Name}

**Issue:** {Brief description of the problem}
**Impact:** {HIGH/MEDIUM/LOW} - {Why it matters}
**Root Cause:** {Why this happened}
**Fix:** {What needs to be done}

**Evidence:**
- {Evidence line 1 - file paths, symptoms, etc.}
- {Evidence line 2}

**Fix Requirements:**
- {Requirement 1}
- {Requirement 2}
- {Requirement 3}
```

### notes.txt Example

```markdown
# Bug Fix: Architectural Inconsistency in Feature 02

**Issue:** Feature 01 uses Manager class pattern, Feature 02 uses standalone functions
**Impact:** HIGH - Architectural inconsistency makes epic hard to maintain
**Root Cause:** Different agents implemented features with different patterns
**Fix:** Refactor Feature 02 to Manager pattern (create MatchupManager class)

**Evidence:**
- Feature 01: ADPManager class (feature_01/adp_manager.py)
- Feature 02: standalone functions get_matchup_difficulty(), load_matchup_data()

**Fix Requirements:**
- Create MatchupManager class
- Move standalone functions to class methods
- Update imports in consuming code
- Update tests
```

---

## Template 6: S9 Restart Documentation (Step 7.5)

**Purpose:** Document S9 restart after bug fixes complete
**When to Use:** After ALL bug fixes complete, when restarting S9
**Location:** Add to `KAI-{N}-{epic_name}/epic_lessons_learned.md`

### Template

```markdown
## S9 Restart Log

**Restart Date:** {YYYY-MM-DD}
**Reason:** {N} bug fixes completed ({list bug fix names})

**Bug Fixes Completed:**
1. {bugfix_name}: {Brief description of fix}
2. {bugfix_name}: {Brief description of fix}
[List all bug fixes]

**Restart Actions:**
- ✅ Re-ran S9.P1: Epic Smoke Testing (all 4 parts) - {PASSED/issues found}
- ✅ Re-ran S9.P2: QC Round 1 (Cross-Feature Integration) - {PASSED/issues found}
- ✅ Re-ran S9.P2: QC Round 2 (Epic Cohesion & Consistency) - {PASSED/issues found}
- ✅ Re-ran S9.P2: QC Round 3 (End-to-End Success Criteria) - {PASSED/issues found}
- ✅ Re-ran S9.P3: Epic PR Review (all 11 categories) - {PASSED/issues found}
- ✅ All unit tests passing ({pass_rate}% - {N} tests)

**Result:** S9 {complete/incomplete} after restart ({no new issues found / N new issues found})
```

### Example

```markdown
## S9 Restart Log

**Restart Date:** 2025-01-02
**Reason:** 2 bug fixes completed (bugfix_high_architecture_inconsistency, bugfix_high_performance_regression)

**Bug Fixes Completed:**
1. bugfix_high_architecture_inconsistency: Refactored Feature 02 to Manager pattern
2. bugfix_high_performance_regression: Implemented batch loading for matchup data

**Restart Actions:**
- ✅ Re-ran S9.P1: Epic Smoke Testing (all 4 parts) - PASSED
- ✅ Re-ran S9.P2: QC Round 1 (Cross-Feature Integration) - PASSED
- ✅ Re-ran S9.P2: QC Round 2 (Epic Cohesion & Consistency) - PASSED
- ✅ Re-ran S9.P2: QC Round 3 (End-to-End Success Criteria) - PASSED
- ✅ Re-ran S9.P3: Epic PR Review (all 11 categories) - PASSED
- ✅ All unit tests passing (100% - 2247 tests)

**Result:** S9 complete after restart (no new issues found)
```

---

## Template 7: Final Verification Checklist (Step 8.1)

**Purpose:** Verify all S9 work complete before marking done
**When to Use:** Step 8.1 (Final Verification)
**Location:** Add to `KAI-{N}-{epic_name}/epic_lessons_learned.md`

### Template

```markdown
## S9.P3 Final Verification

**Date:** {YYYY-MM-DD HH:MM}

**Verification Results:**
- ✅/❌ Epic smoke testing passed (all 4 parts)
- ✅/❌ QC Round 1 passed (no integration issues)
- ✅/❌ QC Round 2 passed (no consistency issues)
- ✅/❌ QC Round 3 passed (success criteria met {percentage}%)
- ✅/❌ Epic PR review passed (all 11 categories)
- ✅/❌ NO pending issues or bug fixes
- ✅/❌ ALL tests passing ({N}/{total} tests, {percentage}% pass rate)

**Result:** S9 verification {PASSED/FAILED} - {Ready/Not ready} to mark complete
```

### Verification Commands

```bash
# 1. Run all tests to confirm 100% pass rate
python tests/run_all_tests.py

# Expected output:
# ============================== 2247 passed in 45.32s ===========================
# Exit code: 0 ✅

# 2. Check EPIC_README.md for pending issues
# Should show: "No pending issues or bug fixes"

# 3. Check epic_lessons_learned.md for unresolved issues
# All issues should have "Status: RESOLVED" or not be listed

# 4. Verify bug fix folders (if any) completed S7
# bugfix_high_*/README.md should show "S7: COMPLETE"
```

### Example

```markdown
## S9.P3 Final Verification

**Date:** 2025-01-02 16:00

**Verification Results:**
- ✅ Epic smoke testing passed (all 4 parts)
- ✅ QC Round 1 passed (no integration issues)
- ✅ QC Round 2 passed (no consistency issues)
- ✅ QC Round 3 passed (success criteria met 100%)
- ✅ Epic PR review passed (all 11 categories)
- ✅ NO pending issues or bug fixes
- ✅ ALL tests passing (2247/2247 tests, 100% pass rate)

**Result:** S9 verification PASSED - Ready to mark complete
```

---

## Template 8: Epic Progress Tracker Update (Step 8.2)

**Purpose:** Update EPIC_README.md to show S9 complete
**When to Use:** Step 8.2 after verification passes
**Location:** Update in `KAI-{N}-{epic_name}/EPIC_README.md`

### Template

```markdown
## Epic Progress Tracker

**S1 - Epic Planning:** ✅ COMPLETE
**S2 - Feature Deep Dives:** ✅ COMPLETE
**S3 - Cross-Feature Sanity Check:** ✅ COMPLETE
**S4 - Epic Testing Strategy:** ✅ COMPLETE
**S5 - Feature Implementation:** ✅ COMPLETE
  - Feature 01: ✅ COMPLETE
  - Feature 02: ✅ COMPLETE
  [List all features]

**S9 - Epic Final QC:** ✅ COMPLETE
- S9.P1 (Epic Smoke Testing): ✅ COMPLETE
- S9.P2 (Epic QC Rounds): ✅ COMPLETE
- S9.P3 (Epic Final Review): ✅ COMPLETE
- Epic smoke testing passed: ✅
- Epic QC rounds passed: ✅ (Rounds {1, 2, 3})
- Epic PR review passed: ✅ ({N} categories)
- End-to-end validation passed: ✅
- Issues found: {N} ({all resolved / N unresolved})
- S9 restarts: {N} ({reason if applicable})
- Date completed: {YYYY-MM-DD}

**S10 - Epic Cleanup:** [ ] PENDING
```

### Example

```markdown
## Epic Progress Tracker

**S1 - Epic Planning:** ✅ COMPLETE
**S2 - Feature Deep Dives:** ✅ COMPLETE
**S3 - Cross-Feature Sanity Check:** ✅ COMPLETE
**S4 - Epic Testing Strategy:** ✅ COMPLETE
**S5 - Feature Implementation:** ✅ COMPLETE
  - Feature 01: ✅ COMPLETE
  - Feature 02: ✅ COMPLETE

**S9 - Epic Final QC:** ✅ COMPLETE
- S9.P1 (Epic Smoke Testing): ✅ COMPLETE
- S9.P2 (Epic QC Rounds): ✅ COMPLETE
- S9.P3 (Epic Final Review): ✅ COMPLETE
- Epic smoke testing passed: ✅
- Epic QC rounds passed: ✅ (Rounds 1, 2, 3)
- Epic PR review passed: ✅ (11 categories)
- End-to-end validation passed: ✅
- Issues found: 2 (both resolved via bug fixes)
- S9 restarts: 1 (after bug fixes)
- Date completed: 2025-01-02

**S10 - Epic Cleanup:** [ ] PENDING
```

---

## Template 9: S9.P3 Lessons Learned (Step 8.3)

**Purpose:** Document insights from S9.P3 for future improvement
**When to Use:** Step 8.3 after S9 complete
**Location:** Add to `KAI-{N}-{epic_name}/epic_lessons_learned.md`

### Template

```markdown
## S9.P3 Lessons Learned (Epic Final Review)

**Date:** {YYYY-MM-DD}

**What Went Well:**
- {Positive observation 1}
- {Positive observation 2}
- {Positive observation 3}

**What Could Be Improved:**
- {Improvement area 1}
- {Improvement area 2}
- {Improvement area 3}

**Issues Found & Resolved:**
1. **{Issue Name}:** {Brief description}
   - Fixed: {What was done}
   - Prevention: {How to prevent in future}
2. **{Issue Name}:** {Brief description}
   - Fixed: {What was done}
   - Prevention: {How to prevent in future}

**Insights for Future Epics:**
- {Actionable insight 1}
- {Actionable insight 2}
- {Actionable insight 3}

**Guide Improvements Needed:**
- {Guide name}: {Specific improvement needed}
- {Guide name}: {Specific improvement needed}

**S9.P3 Statistics:**
- Epic PR Review time: {X minutes}
- Issues found: {N} ({breakdown by priority})
- Bug fixes created: {N}
- Bug fix time: {X hours total}
- S9 restart time: {X hours}
- Total S9 time: {X hours} (including restarts)

**Key Takeaway:** {One-sentence summary of most important lesson}
```

### Example

```markdown
## S9.P3 Lessons Learned (Epic Final Review)

**Date:** 2025-01-02

**What Went Well:**
- Epic PR review systematic (11 categories covered comprehensively)
- Architectural consistency check caught Manager pattern inconsistency
- Performance category identified N+1 query regression early
- Bug fix workflow smooth (S2 → 5a → 5b → 5c)
- S9 restart after bug fixes ensured quality maintained

**What Could Be Improved:**
- Architectural pattern should be enforced in S2 (spec should mandate Manager pattern)
- Performance baseline should be measured in S1 (not assumed)
- Could have caught architectural inconsistency in S8.P1 (cross-feature alignment)

**Issues Found & Resolved:**
1. **Architectural Inconsistency:** Feature 02 used standalone functions instead of Manager pattern
   - Fixed: Refactored to MatchupManager class
   - Prevention: Add "Architecture Pattern" to S2 spec template
2. **Performance Regression:** N+1 queries in Feature 02 (+400% regression)
   - Fixed: Implemented batch loading for matchup data
   - Prevention: Add performance testing to S7 smoke testing

**Insights for Future Epics:**
- Establish architectural patterns early (S2 deep dives)
- Document patterns in EPIC_README.md for all agents to follow
- Measure performance baseline in S1 (include in epic notes)
- Add "Architecture" section to feature spec.md template
- Review architectural consistency after EACH feature (S8.P1)

**Guide Improvements Needed:**
- STAGE_2 guide: Add "Architecture Pattern" section to spec template
- S5.P3 guide: Add performance baseline comparison to smoke testing
- S9 guide: Add architectural pattern consistency check

**S9.P3 Statistics:**
- Epic PR Review time: 45 minutes
- Issues found: 2 (both high priority)
- Bug fixes created: 2
- Bug fix time: 4 hours total
- S9 restart time: 2 hours
- Total S9 time: 8.5 hours (including restarts)

**Key Takeaway:** Epic-level PR review is CRITICAL for catching architectural inconsistencies that feature-level reviews miss. The 11-category checklist provides comprehensive coverage.
```

---

## Template 10: Agent Status Update (Step 8.4)

**Purpose:** Update EPIC_README.md Agent Status to show S9 complete
**When to Use:** Step 8.4 after all documentation complete
**Location:** Update in `KAI-{N}-{epic_name}/EPIC_README.md`

### Template

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Stage:** S9.P3 - Epic Final Review
**Status:** ✅ COMPLETE

**S9 Summary:**
- S9.P1 (Epic Smoke Testing): ✅ {PASSED/issues found}
- S9.P2 (Epic QC Rounds): ✅ {PASSED/issues found} (Rounds {1, 2, 3})
- S9.P3 (Epic Final Review): ✅ {PASSED/issues found}
- Epic PR review: ✅ {PASSED/issues found} ({N} categories)
- Issues found: {N} ({resolution status})
- Bug fixes completed: {N}
- S9 restarts: {N} ({reason if applicable})
- All tests passing: ✅ ({N}/{total} tests)
- Result: Epic ready for {next stage}

**Next Stage:** stages/s10/s7_epic_cleanup.md
**Next Action:** Read stages/s10/s7_epic_cleanup.md to begin final epic cleanup
```

### Example

```markdown
## Agent Status

**Last Updated:** 2025-01-02 16:15
**Current Stage:** S9.P3 - Epic Final Review
**Status:** ✅ COMPLETE

**S9 Summary:**
- S9.P1 (Epic Smoke Testing): ✅ PASSED
- S9.P2 (Epic QC Rounds): ✅ PASSED (Rounds 1, 2, 3)
- S9.P3 (Epic Final Review): ✅ PASSED
- Epic PR review: ✅ PASSED (11 categories)
- Issues found: 2 (both fixed via bug fixes)
- Bug fixes completed: 2
- S9 restarts: 1 (after bug fixes)
- All tests passing: ✅ (2247/2247 tests)
- Result: Epic ready for cleanup and move to done/

**Next Stage:** stages/s10/s7_epic_cleanup.md
**Next Action:** Read stages/s10/s7_epic_cleanup.md to begin final epic cleanup
```

---

## Template Selection Guide

**Use Template 1** when documenting PR review results (Step 6 complete)

**Use Templates 2-6** when issues found during PR review (Step 7):
- Template 2: Document issues in epic_lessons_learned.md
- Template 3: Prioritize issues (which need bug fixes)
- Template 4: Present issues to user for approval
- Template 5: Create bug fix folders with notes.txt
- Template 6: Document S9 restart after bug fixes

**Use Templates 7-10** during final verification (Step 8):
- Template 7: Verify all work complete
- Template 8: Update Epic Progress Tracker
- Template 9: Document S9.P3 lessons learned
- Template 10: Update Agent Status to S9 complete

---

**See Also:**
- Main Guide: `stages/s9/s6_p4_epic_final_review.md`
- PR Review Checklist: `reference/stage_6/epic_pr_review_checklist.md`
- Examples: `reference/stage_6/epic_final_review_examples.md` (will be created)

---

**END OF EPIC FINAL REVIEW TEMPLATES**
