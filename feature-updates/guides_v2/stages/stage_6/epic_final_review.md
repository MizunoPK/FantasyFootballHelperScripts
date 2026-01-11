# STAGE 6c: Epic Final Review Guide

**Part of:** Epic-Driven Development Workflow v2
**Stage:** 6 - Epic-Level Final QC
**Sub-Stage:** 6c - Epic Final Review (Steps 6-8)
**Prerequisites:** STAGE_6b complete (all 3 QC rounds passed)
**Next Stage:** stages/stage_7/epic_cleanup.md

---

## 🚨 MANDATORY READING PROTOCOL

**CRITICAL:** You MUST read this ENTIRE guide before starting Stage 6c work.

**Why this matters:**
- Stage 6c is the FINAL VALIDATION before epic completion
- Missing steps here means shipping incomplete or incorrect epic
- Thoroughness prevents post-completion issues

**Reading Checkpoint:**
Before proceeding, you must have:
- [ ] Read this ENTIRE guide (use Read tool, not memory)
- [ ] Verified STAGE_6b complete (all 3 QC rounds passed)
- [ ] Verified no pending issues or bug fixes
- [ ] Located epic_lessons_learned.md file

**If resuming after session compaction:**
1. Check EPIC_README.md "Agent Status" section for current step
2. Re-read this guide from the beginning
3. Continue from documented checkpoint

---

## Quick Start

### What is this sub-stage?

**STAGE_6c - Epic Final Review** is the final validation phase of Stage 6, where you apply an epic-level PR review checklist, handle any discovered issues through bug fixes, and perform final verification before declaring the epic complete.

**This is NOT feature-level review** - Stage 5c already reviewed individual features. This focuses on:
- Epic-wide architectural consistency
- Cross-feature code quality
- Epic scope and completeness
- Final validation against original request

### When do you use this guide?

**Use this guide when:**
- STAGE_6b is complete (all 3 QC rounds passed)
- Epic smoke testing passed (STAGE_6a)
- Ready for final epic-level PR review and validation
- All features completed Stage 5e

**Do NOT use this guide if:**
- STAGE_6a smoke testing not complete
- STAGE_6b QC rounds not complete
- Any features still in Stage 5b implementation
- Pending bug fixes not yet completed

### What are the key outputs?

1. **Epic PR Review Results** (documented in epic_lessons_learned.md)
   - 11 categories reviewed at epic level
   - All categories must pass (no failures)

2. **Bug Fixes (if issues found)**
   - Bug fix folders created for any issues
   - Stage 6 RESTARTED after bug fixes

3. **Final Verification**
   - All Stage 6 steps confirmed complete
   - epic_lessons_learned.md updated
   - EPIC_README.md marked complete

4. **Stage 6 Completion**
   - Ready to proceed to Stage 7 (Epic Cleanup)

### Time estimate

**60-90 minutes** (if no issues found)
- Epic PR Review: 30-45 minutes
- Final Verification: 15-30 minutes
- Documentation updates: 15 minutes

**+2-4 hours per bug fix** (if issues found, includes Stage 6 restart)

### Workflow overview

```
STAGE_6c Workflow (Steps 6-8)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Prerequisites Met?
  ├─ STAGE_6b complete (3 QC rounds passed)
  ├─ No pending issues
  └─ All tests passing (100%)
         │
         ▼
┌─────────────────────────────────────┐
│ STEP 6: Epic PR Review              │
│ (11 Categories - Epic Scope)        │
└─────────────────────────────────────┘
         │
         ├─ Correctness (epic level)
         ├─ Code Quality (epic level)
         ├─ Comments & Documentation
         ├─ Code Organization
         ├─ Testing (epic level)
         ├─ Security (epic level)
         ├─ Performance (epic level)
         ├─ Error Handling (epic level)
         ├─ Architecture (CRITICAL)
         ├─ Backwards Compatibility
         └─ Scope & Changes
         │
         ▼
    Any Issues Found?
    ├─ YES → STEP 7 (Handle Issues)
    │         │
    │         ├─ Document all issues
    │         ├─ Create bug fixes
    │         └─ RESTART Stage 6
    │
    └─ NO → STEP 8 (Final Verification)
              │
              ├─ Verify all issues resolved
              ├─ Update EPIC_README.md
              ├─ Update epic_lessons_learned.md
              └─ Mark Stage 6 complete
              │
              ▼
        Stage 6 COMPLETE
              │
              ▼
        Ready for Stage 7
```

---

## Critical Rules for Stage 6c

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - Stage 6c (Epic Final Review)               │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ Epic-level PR review focuses on CROSS-FEATURE concerns
   - Feature-level review already done in Stage 5c
   - Focus: Architectural consistency, cross-feature impacts
   - Don't repeat feature-level checks

2. ⚠️ ALL 11 categories are MANDATORY
   - Cannot skip categories
   - All categories must PASS (no exceptions)
   - If ANY category fails → create bug fix

3. ⚠️ If issues found, you MUST RESTART Stage 6
   - After bug fixes complete
   - RESTART from STAGE_6a (smoke testing)
   - Cannot partially continue Stage 6

4. ⚠️ Validate against ORIGINAL epic request
   - Not against evolved specs
   - Re-read {epic_name}.txt file
   - Verify user's stated goals achieved

5. ⚠️ Zero tolerance for architectural inconsistencies
   - Design patterns must be consistent across features
   - Code style must be uniform
   - Error handling must be consistent

6. ⚠️ 100% test pass rate required
   - All unit tests must pass
   - No "expected failures"
   - Fix ALL test failures before marking complete

7. ⚠️ Document EVERYTHING in epic_lessons_learned.md
   - PR review results
   - Issues found (if any)
   - Stage 6 insights
   - Improvements for future epics

8. ⚠️ Cannot proceed to Stage 7 without completion
   - All 8 steps of Stage 6 must be complete
   - No pending issues or bug fixes
   - EPIC_README.md must show Stage 6 complete
```

---

## Prerequisites

**Before starting Stage 6c, verify ALL of these are true:**

### From STAGE_6b (QC Rounds)
- [ ] QC Round 1 (Cross-Feature Integration): ✅ PASSED
- [ ] QC Round 2 (Epic Cohesion & Consistency): ✅ PASSED
- [ ] QC Round 3 (End-to-End Success Criteria): ✅ PASSED
- [ ] STAGE_6b completion documented in EPIC_README.md

### From STAGE_6a (Smoke Testing)
- [ ] Epic smoke testing Part 1 (Import Tests): ✅ PASSED
- [ ] Epic smoke testing Part 2 (Entry Point Tests): ✅ PASSED
- [ ] Epic smoke testing Part 3 (E2E Execution Tests): ✅ PASSED
- [ ] Epic smoke testing Part 4 (Cross-Feature Integration Tests): ✅ PASSED

### Feature Completion
- [ ] All features completed Stage 5e (Post-Feature Testing Update)
- [ ] No features currently in Stage 5b (Implementation)
- [ ] No pending feature work

### Quality Gates
- [ ] All unit tests passing (100% pass rate)
- [ ] No known bugs or issues
- [ ] All previous bug fixes (if any) completed Stage 5c

### Documentation
- [ ] epic_lessons_learned.md exists and accessible
- [ ] EPIC_README.md shows STAGE_6b complete
- [ ] Original {epic_name}.txt file located

**If ANY prerequisite not met:**
- STOP - Do not proceed with Stage 6c
- Complete missing prerequisites first
- Return to appropriate stage (6a or 6b)

---

## STEP 6: Epic PR Review (Multi-Round with Fresh Eyes)

**🚨 MANDATORY: READ PR REVIEW PROTOCOL**

**Before proceeding, you MUST:**
1. **READ:** `stages/stage_5/pr_review_protocol.md`
2. **Follow the complete hybrid approach:**
   - Round 1: 4 specialized reviews (fresh agent for each)
   - Rounds 2-5: Iterative comprehensive reviews (fresh agent for each)
   - 2 consecutive clean rounds required to pass
   - Maximum 5 rounds total

**Purpose:** Systematic epic-level PR review using fresh agent context to catch issues before final commit.

**Why fresh agents?** New agents avoid context bias and provide "fresh eyes" on epic-wide changes.

---

### Overview

**Objective:** Apply PR review protocol to epic-wide changes with focus on architectural consistency.

**This is NOT feature-level review:**
- Stage 5c already reviewed individual feature correctness
- Stage 6c reviews EPIC-WIDE concerns:
  - Architectural consistency ACROSS features
  - Code duplication BETWEEN features
  - Cross-feature integration quality
  - Epic scope completeness
  - Original epic request validation

**Round Structure:**

**Round 1 (Specialized - 4 Fresh Agents):**
- **Round 1a:** Code Quality (epic level) - Fresh agent
- **Round 1b:** Testing & Performance - Fresh agent
- **Round 1c:** Security & Error Handling - Fresh agent
- **Round 1d:** Documentation & Scope - Fresh agent

**Rounds 2-5 (Comprehensive - Fresh Agent Each):**
- Each round: Fresh agent reviews ALL 11 categories
- 2 consecutive clean rounds required to pass
- Maximum 5 total rounds

---

### Step-by-Step Workflow

**See:** `reference/stage_6/epic_pr_review_checklist.md` for complete 11-category checklist

**Step 6.1: Apply Round 1 (Specialized Reviews)**

1. **Create pr_review_issues.md file:**
   ```
   Location: KAI-{N}-{epic_name}/pr_review_issues.md
   Purpose: Track issues discovered during PR review rounds
   ```

2. **Launch Round 1a (Code Quality - Fresh Agent):**
   - Code Quality (Epic Level)
   - Code Organization & Refactoring (Epic Level)

3. **Launch Round 1b (Testing & Performance - Fresh Agent):**
   - Testing (Epic Level)
   - Performance (Epic Level)

4. **Launch Round 1c (Security & Error Handling - Fresh Agent):**
   - Security (Epic Level)
   - Error Handling (Epic Level)

5. **Launch Round 1d (Documentation & Scope - Fresh Agent):**
   - Comments & Documentation (Epic Level)
   - Scope & Changes (Epic Level)

**Step 6.2: Apply Rounds 2-5 (Comprehensive Reviews)**

**For each round (2-5), launch fresh agent to review ALL 11 categories:**

1. Correctness (Epic Level)
2. Code Quality (Epic Level)
3. Comments & Documentation (Epic Level)
4. Code Organization & Refactoring (Epic Level)
5. Testing (Epic Level)
6. Security (Epic Level)
7. Performance (Epic Level)
8. Error Handling (Epic Level)
9. **Architecture (Epic Level - CRITICAL)**
10. Backwards Compatibility (Epic Level)
11. Scope & Changes (Epic Level)

**Each fresh agent:**
- Reviews ALL 11 categories
- Documents issues in pr_review_issues.md
- Returns comprehensive report

**Passing Criteria:**
- 2 consecutive rounds with ZERO issues = PASS
- If issues found in any round → Fix and continue
- Maximum 5 rounds total

**Step 6.3: Document PR Review Results**

**Update epic_lessons_learned.md with results:**

**See:** `reference/stage_6/epic_final_review_templates.md` Template 1 for PR review results template

**Include:**
- Date, epic name, total rounds
- Final status (PASSED/FAILED)
- Review summary (what was found in each round)
- Total issues found and fixed
- Epic-level concerns addressed

---

## STEP 7: Handle Issues (If Any Discovered)

**When to use:** ANY category failed in Step 6 PR review

**When to SKIP:** All 11 categories passed, no issues discovered

---

### Overview

**Objective:** Create bug fixes for any epic-level integration issues discovered during Step 6.

**Critical Rule:** After bug fixes, you MUST COMPLETELY RESTART Stage 6 from STAGE_6a.

**Why RESTART?** Bug fixes may have affected areas already checked. Cannot assume previous QC results still valid.

---

### Step-by-Step Workflow

**See:** `reference/stage_6/epic_final_review_templates.md` Templates 2-6 for issue handling templates

**Step 7.1: Document ALL Issues**

**See:** Template 2 (Issues Found Documentation)

Document in epic_lessons_learned.md:
- Issue description
- Discovered in (which category)
- Impact (HIGH/MEDIUM/LOW)
- Root cause
- Fix required
- Priority (high/medium/low)

**Step 7.2: Determine Bug Fix Priorities**

**See:** Template 3 (Issue Prioritization)

**Priority Levels:**
- **high:** Breaks functionality, security, architecture, performance >100% regression
- **medium:** Affects quality (consistency, error messages, minor performance)
- **low:** Cosmetic only (comments, variable names) - document only, no bug fix

**Step 7.3: Present Issues to User**

**See:** Template 4 (User Presentation)

Present ALL high/medium priority issues to user for approval before creating bug fixes.

**Step 7.4: Create Bug Fixes Using Bug Fix Workflow**

**See:** Template 5 (Bug Fix Folder Structure)

For EACH issue:
1. Create bug fix folder (bugfix_{priority}_{name}/)
2. Create notes.txt with issue description
3. Run through bug fix workflow: Stage 2 → 5a → 5b → 5c
4. Bug fix stays in epic folder (doesn't move to done/)

**Step 7.5: RESTART Stage 6 After Bug Fixes**

**See:** Template 6 (Stage 6 Restart Documentation)

**CRITICAL:** You MUST COMPLETELY RESTART Stage 6 after ALL bug fixes complete.

**Restart Protocol:**
1. Mark all Stage 6 steps as "incomplete" in EPIC_README.md
2. Re-run STAGE_6a (Epic Smoke Testing - all 4 parts)
3. Re-run STAGE_6b (Epic QC Rounds 1, 2, 3)
4. Re-run STAGE_6c (Epic PR Review - all 11 categories)
5. Document restart in epic_lessons_learned.md

---

## STEP 8: Final Verification & README Update

**When to use:** Step 6 passed (all 11 categories) AND Step 7 complete OR skipped (no issues)

---

### Overview

**Objective:** Verify Stage 6c complete, all issues resolved, update epic documentation.

---

### Step-by-Step Workflow

**See:** `reference/stage_6/epic_final_review_templates.md` Templates 7-10 for verification templates

**Step 8.1: Verify All Issues Resolved**

**See:** Template 7 (Final Verification Checklist)

**Verification Checklist:**
- [ ] Epic smoke testing passed (all 4 parts)
- [ ] QC Round 1 passed (no integration issues)
- [ ] QC Round 2 passed (no consistency issues)
- [ ] QC Round 3 passed (success criteria met)
- [ ] Epic PR review passed (all 11 categories)
- [ ] NO pending issues or bug fixes
- [ ] ALL tests passing (100% pass rate)

**Run all tests to confirm:**
```bash
python tests/run_all_tests.py
# Expected: 100% pass rate, exit code 0
```

**If ANY item unchecked:** STOP - Address remaining issues, re-run affected steps

**Step 8.2: Update EPIC_README.md Epic Progress Tracker**

**See:** Template 8 (Epic Progress Tracker Update)

Mark Stage 6 complete, including:
- STAGE_6a, 6b, 6c completion status
- Issues found and resolved
- Bug fixes completed
- Stage 6 restarts (if any)
- Date completed

**Step 8.3: Update epic_lessons_learned.md**

**See:** Template 9 (Stage 6c Lessons Learned)

Add Stage 6c insights:
- What went well
- What could be improved
- Issues found & resolved
- Insights for future epics
- Guide improvements needed
- Statistics (time, issues, bug fixes)
- Key takeaway

**Step 8.4: Update EPIC_README.md Agent Status**

**See:** Template 10 (Agent Status Update)

Mark Stage 6c complete and prepare for Stage 7:
- Current stage: Stage 6c
- Status: COMPLETE
- Stage 6 summary (all parts, results)
- Next stage: stages/stage_7/epic_cleanup.md
- Next action: Read epic cleanup guide

**Step 8.5: Completion Indicator**

**Stage 6c is COMPLETE when ALL of these are true:**
- ✅ All 3 steps finished (6, 7, 8)
- ✅ Epic PR review passed (all 11 categories)
- ✅ All issues resolved (bug fixes complete OR no issues found)
- ✅ No pending issues or bug fixes
- ✅ EPIC_README.md Epic Progress Tracker updated
- ✅ epic_lessons_learned.md updated with Stage 6c insights
- ✅ EPIC_README.md Agent Status shows Stage 6c complete
- ✅ All tests passing (100% pass rate)
- ✅ Ready to proceed to Stage 7

**If ANY item not complete:** STOP - Complete missing items, re-verify

---

## Re-Reading Checkpoints

**You MUST re-read this guide when:**

### 1. After Session Compaction
- Conversation compacted while in Stage 6c
- Re-read to restore context
- Check EPIC_README.md Agent Status to see which step you're on
- Continue from documented checkpoint

### 2. After Creating Bug Fixes
- Bug fixes created during Step 7
- Re-read "STEP 7: Handle Issues" section
- Remember: MUST RESTART Stage 6 after bug fixes (from STAGE_6a)
- Re-read STAGE_6a and STAGE_6b guides for restart

### 3. After Extended Break (>24 hours)
- Returning to epic after break
- Re-read guide to refresh requirements
- Verify prerequisites still met (tests passing, no new issues)

### 4. When Encountering Confusion
- Unsure about next step
- Re-read workflow overview and current step
- Check EPIC_README.md for current status

### 5. Before Starting Epic PR Review (Step 6)
- Re-read all 11 category descriptions
- Refresh focus areas for each category
- Ensure thorough coverage (don't rush)

**Re-Reading Protocol:**
1. Use Read tool to load ENTIRE guide
2. Find current step in EPIC_README.md Agent Status
3. Read "Workflow Overview" section
4. Read current step's detailed workflow
5. Proceed with renewed understanding

---

## Completion Criteria

**Stage 6c is COMPLETE when ALL of the following are true:**

### Epic PR Review (Step 6)
- [ ] All 11 categories reviewed: ✅ PASSED
  - [ ] 1. Correctness (Epic Level): ✅ PASS
  - [ ] 2. Code Quality (Epic Level): ✅ PASS
  - [ ] 3. Comments & Documentation (Epic Level): ✅ PASS
  - [ ] 4. Code Organization & Refactoring (Epic Level): ✅ PASS
  - [ ] 5. Testing (Epic Level): ✅ PASS
  - [ ] 6. Security (Epic Level): ✅ PASS
  - [ ] 7. Performance (Epic Level): ✅ PASS
  - [ ] 8. Error Handling (Epic Level): ✅ PASS
  - [ ] 9. Architecture (Epic Level - CRITICAL): ✅ PASS
  - [ ] 10. Backwards Compatibility (Epic Level): ✅ PASS
  - [ ] 11. Scope & Changes (Epic Level): ✅ PASS
- [ ] PR review results documented in epic_lessons_learned.md

### Handle Issues (Step 7 - if applicable)
- [ ] All issues documented (if any found)
- [ ] Bug fixes created for all high/medium priority issues (if any)
- [ ] Bug fixes completed Stage 5c (if any created)
- [ ] Stage 6 RESTARTED after bug fixes (if any created)
- [ ] All steps re-run and passed after restart

### Final Verification (Step 8)
- [ ] All issues resolved (no pending issues or bug fixes)
- [ ] All unit tests passing (100% pass rate)
- [ ] EPIC_README.md Epic Progress Tracker updated (Stage 6 marked complete)
- [ ] epic_lessons_learned.md updated with Stage 6c insights
- [ ] EPIC_README.md Agent Status shows Stage 6c complete

### Overall Stage 6 Completion
- [ ] STAGE_6a complete (Epic Smoke Testing passed)
- [ ] STAGE_6b complete (QC Rounds 1, 2, 3 passed)
- [ ] STAGE_6c complete (Epic PR Review passed, issues resolved)
- [ ] Original epic goals validated and achieved (from STAGE_6b QC Round 3)
- [ ] Ready to proceed to Stage 7

**DO NOT proceed to Stage 7 until ALL completion criteria are met.**

---

## Reference Files

**For detailed information, see these reference files:**

**Epic PR Review Checklist:**
- `reference/stage_6/epic_pr_review_checklist.md`
- Complete 11-category checklist with validation steps
- Use during Step 6 (Epic PR Review)

**Templates:**
- `reference/stage_6/epic_final_review_templates.md`
- Templates for documenting results (Steps 6-8)
- Issue documentation, bug fix structure, verification checklists

**Examples & Best Practices:**
- `reference/stage_6/epic_final_review_examples.md`
- Common mistakes to avoid (7 anti-patterns)
- Real-world example walkthrough
- Best practices summary

---

## Prerequisites for Next Stage

**Before proceeding to Stage 7 (Epic Cleanup), verify:**

### Stage 6c Completion
- [ ] STEP 6 (Epic PR Review) complete: All 11 categories PASSED
- [ ] STEP 7 (Handle Issues) complete OR skipped (no issues)
- [ ] STEP 8 (Final Verification) complete: All verification items checked

### Overall Stage 6 Completion
- [ ] STAGE_6a complete (Epic Smoke Testing passed)
- [ ] STAGE_6b complete (QC Rounds 1, 2, 3 passed)
- [ ] STAGE_6c complete (Epic PR Review passed, issues resolved)
- [ ] No pending issues or bug fixes
- [ ] All bug fix folders (if any) show Stage 5c complete

### Documentation Complete
- [ ] epic_lessons_learned.md updated with Stage 6c insights
- [ ] EPIC_README.md Epic Progress Tracker shows Stage 6 complete
- [ ] EPIC_README.md Agent Status shows Stage 6c complete
- [ ] PR review results documented

### Quality Gates Passed
- [ ] All unit tests passing (100% pass rate)
- [ ] Original epic goals validated (from STAGE_6b QC Round 3)
- [ ] Epic success criteria met
- [ ] End-to-end workflows validated

**Only proceed to Stage 7 when ALL items are checked.**

**Next stage:** stages/stage_7/epic_cleanup.md
**Next action:** Read stages/stage_7/epic_cleanup.md to begin epic cleanup

---

## Summary

**Stage 6c - Epic Final Review is the final validation before epic completion:**

**Key Activities:**
1. **Epic PR Review (Step 6):** Apply 11-category checklist to epic-wide changes
   - Focus: Architectural consistency, cross-feature impacts, epic scope
   - Critical category: Architecture (Step 6.9)
   - Document results in epic_lessons_learned.md

2. **Handle Issues (Step 7):** Create bug fixes for any discovered issues
   - Document all issues comprehensively
   - Create bug fixes using bug fix workflow
   - RESTART Stage 6 from STAGE_6a after fixes

3. **Final Verification (Step 8):** Confirm Stage 6 complete
   - Verify all issues resolved
   - Update EPIC_README.md (Epic Progress Tracker, Agent Status)
   - Update epic_lessons_learned.md with insights

**Critical Distinctions:**
- **Feature-level PR review (Stage 5c):** Reviews individual features in isolation
- **Epic-level PR review (Stage 6c):** Reviews cross-feature consistency, architectural cohesion, epic scope

**Success Criteria:**
- Epic PR review passed (all 11 categories)
- All issues resolved (bug fixes complete OR no issues)
- No pending issues or bug fixes
- All tests passing (100%)
- Original epic goals achieved
- Ready to proceed to Stage 7

**Common Pitfalls:**
- Repeating feature-level review instead of epic-level
- Fixing issues inline instead of using bug fix workflow
- Skipping Architecture category review (most important)
- Comparing to specs instead of original epic request
- Accepting issues instead of creating bug fixes
- Not documenting PR review results
- Proceeding to Stage 7 with pending issues

**See:** `reference/stage_6/epic_final_review_examples.md` for detailed examples of each mistake and best practices

**Next Stage:** stages/stage_7/epic_cleanup.md - Final commits, PR creation, user review, move epic to done/

**Remember:** Stage 6c is the LAST CHANCE to catch epic-level issues before shipping. Thoroughness here prevents post-completion rework and ensures epic delivers on user's vision.

---

**END OF STAGE 6c GUIDE**
