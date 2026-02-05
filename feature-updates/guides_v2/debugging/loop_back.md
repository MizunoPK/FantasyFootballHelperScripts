# PHASE 5: Loop Back to Testing

**Purpose:** After ALL issues resolved, loop back to testing stage

**When to Use:** ALL issues in ISSUES_CHECKLIST.md are 🟢 FIXED with user confirmation

**Previous Phase:** PHASE 4 (User Verification) - See `debugging/resolution.md`

**Next Phase:** Return to testing stage (S7.P1, S7.P2, or S9.P1)

---

## Triggered When

ALL issues in ISSUES_CHECKLIST.md meet these criteria:
- Status: 🟢 FIXED
- User Confirmed: ✅ YES
- No issues in 🟡 INVESTIGATING, 🟠 SOLUTION_READY, or 🔴 NOT_STARTED status

---

## Step 1: Verify All Issues Resolved

### Checklist

```markdown
## All Issues Resolution Verification

**Check ISSUES_CHECKLIST.md:**
- [ ] All issues marked 🟢 FIXED
- [ ] All issues have ✅ YES in "User Confirmed?" column
- [ ] No issues in 🟡 INVESTIGATING status
- [ ] No issues in 🟠 SOLUTION_READY status
- [ ] No issues in 🔴 NOT_STARTED status

**Counts:**
- Total Issues: {count}
- Fixed with User Confirmation: {count} ✅
- Outstanding: 0 ✅
```markdown

**If any issue is NOT 🟢 FIXED with ✅ YES:**
- STOP - Cannot proceed to loop-back
- Complete investigation and user verification for that issue first
- Return here when ALL issues are resolved

---

## Step 2: Final Code Review

### 2.1: Check for leftover artifacts

**Search codebase for debug artifacts:**

```bash
# Search for diagnostic logging statements
grep -r "logger.debug.*DEBUG" .
grep -r "print.*DEBUG" .

# Search for TODO comments added during debugging
grep -r "TODO.*debug" .
grep -r "FIXME.*debug" .

# Search for commented-out diagnostic code
grep -r "#.*logger.info.*diagnostic" .
```markdown

**Remove:**
- [ ] Diagnostic logging (unless valuable for production)
- [ ] Debug print statements
- [ ] TODO comments resolved
- [ ] Commented-out diagnostic code
- [ ] Test fixtures used only for debugging

**Keep:**
- Production-valuable logging (errors, warnings, key events)
- Permanent tests (not temporary debugging tests)

---

### 2.3: Run full test suite

```bash
python tests/run_all_tests.py
```markdown

**Requirements:**
- Exit code: 0
- Pass rate: 100%
- No skipped tests (unless intentional)
- No test warnings (unless expected)

**If tests fail:**
- Review failures
- Fix issues
- Re-run tests
- **Do NOT proceed until 100% pass rate**

---

## Step 3: Cross-Bug Pattern Analysis (MANDATORY)

**Purpose:** Identify PATTERNS across bugs and aggregate guide improvements

**When:** After all bugs resolved AND Phase 4b complete for all issues

**Time Required:** 20-40 minutes (focuses on patterns, not individual bugs)

**Note:** Individual bug root cause analysis already done in Phase 4b per issue. This step focuses on PATTERNS across multiple bugs.

---

### 3.1: Review Per-Bug Analyses from Phase 4b

**FIRST: Check if Phase 4b was completed for ALL issues:**

```bash
# Check ISSUES_CHECKLIST.md "Root Cause?" column
# Should show ✅ YES or ⏭️ SKIP for every 🟢 FIXED issue
```markdown

**If any issue missing root cause analysis:**
- STOP - Cannot proceed
- Go back and complete Phase 4b for that issue
- Return here when all issues have root cause analysis

**Read existing analyses:**
- `debugging/guide_update_recommendations.md` (created incrementally in Phase 4b)
- Each `issue_XX_{name}.md` file's "Root Cause Analysis" section

---

### 3.2: Cross-Bug Pattern Analysis

**Goal:** Identify PATTERNS across multiple bugs (not just individual bugs)

**Create or update file:** `debugging/process_failure_analysis.md`

```markdown
# Process Failure Analysis - {Feature/Epic Name}

**Purpose:** Identify PATTERNS across multiple bugs and aggregate guide improvements

**Date:** {YYYY-MM-DD}

**Note:** Individual bug root cause analyses completed in Phase 4b (see guide_update_recommendations.md)

---

## Summary of All Issues

**Total Issues Debugged:** {count}
**Issues with Root Cause Analysis:** {count with ✅ YES}
**Issues Skipped (Not Process Issues):** {count with ⏭️ SKIP}

**Issues by Discovery Stage:**
- Smoke Testing (Part 3): {count}
- QC Round 1: {count}
- QC Round 2: {count}
- QC Round 3: {count}
- Epic Testing: {count}
- User Testing: {count}

---

## Cross-Bug Patterns (NEW FOCUS)

**Purpose:** Identify PATTERNS that appear across multiple bugs (not just individual bugs)

**For each pattern, analyze:**

### Pattern #1: {Pattern Name - e.g., "Missing Entity Status Checks"}

**Affected Issues:** Issue #{X}, Issue #{Y}, Issue #{Z}

**Common Root Cause:**
{What's the common process/guide gap across these bugs?}
Example: "All three bugs involved missing checks for entity status fields (injured, active, etc.) because s5_p2_planning_round2.md Iteration 9 (Edge Case Analysis) doesn't explicitly mention status field edge cases"

**Common Prevention Point:**
{Which stage/iteration should have caught all these bugs?}
Example: "S5 Round 2, Iteration 9 (Edge Case Analysis)"

**Pattern-Based Guide Improvement:**
{What ONE guide change prevents ALL these bugs?}
Example: "Add to s5_p2_planning_round2.md Iteration 9 checklist: '[ ] Entity status fields (active, injured, suspended, bye week, etc.)'"

**Impact:**
- Bugs prevented: {count} similar bugs in future epics
- Estimated time saved: {X} hours per epic

**Priority:** {P0/P1/P2/P3 based on severity and frequency}

---

{Repeat for each pattern found}

---

## High-Priority Guide Updates (Cross-Pattern)

**Purpose:** Aggregate all guide updates from patterns into prioritized list

**These are IN ADDITION to individual guide updates from Phase 4b (which are in guide_update_recommendations.md)**

1. **{guide_name}.md - {section}:**
   - Current state: {quote or "Section doesn't exist"}
   - Proposed change: {new text addressing pattern}
   - Prevents: Pattern #{X} (affects {count} bug types)
   - Priority: {P0/P1/P2/P3}

2. **{guide_name}.md - {section}:**
   - {repeat for each cross-pattern improvement}

---

## Systemic Process Gaps

**Purpose:** Identify gaps that affect the ENTIRE workflow, not just specific stages

**Gap #1: {Gap Name}**
- **What's missing:** {description}
- **Impact:** {which stages/iterations affected}
- **Evidence:** {which bugs exposed this gap}
- **Proposed Solution:** {new workflow step, new gate, new template, etc.}
- **Priority:** {P0/P1/P2/P3}

2. **{guide_name}.md - Section {Y}:**
   - Current text: "{quote current text}"
   - Proposed addition/change: "{new text}"
   - Priority: {P0/P1/P2/P3}

---
```markdown

**Critical Requirements:**

- [ ] Review ALL Phase 4b root cause analyses
- [ ] Identify PATTERNS that appear across multiple bugs
- [ ] Focus on "what pattern exists?" not "why did individual bug occur?"
- [ ] Propose PATTERN-BASED guide updates (not just individual fixes)
- [ ] Cross-pattern improvements are IN ADDITION to Phase 4b individual improvements

**Anti-Patterns to Avoid:**

❌ Repeating individual bug analysis (that's Phase 4b's job)
❌ Generic patterns like "we should test more" (not actionable)
❌ Patterns with only 1 bug (that's already in Phase 4b analysis)
❌ Ignoring existing Phase 4b work (build on it, don't replace it)

---

### 3.3: Update guide_update_recommendations.md with Patterns

**Note:** guide_update_recommendations.md already exists (created incrementally in Phase 4b with individual bug improvements)

**Action:** ADD cross-pattern recommendations to existing file

**Append to existing file** (created in Phase 4b, now add cross-pattern recommendations):

```markdown
---

## CROSS-PATTERN RECOMMENDATIONS (Added from Phase 5 Step 3)

**Purpose:** Pattern-based guide improvements (IN ADDITION to per-issue recommendations above)

**Patterns Analyzed:** {count}
**Date Added:** {YYYY-MM-DD}

---

## Pattern-Based Recommendation #{next_number}: {Pattern Name}

**Source Pattern:** Cross-bug pattern affecting Issue #{X}, #{Y}, #{Z}
**Affected Guide:** `{guide_path}`
**Section:** {section}
**Priority:** {P0/P1/P2/P3}

### Pattern Description

{Description of pattern found across multiple bugs}

### Root Cause (Pattern-Level)

{What process/guide gap allows this pattern to recur}

### Current State (BEFORE)

```markdown
{Current text from guide, OR "Section doesn't exist"}
```bash

### Proposed Change (AFTER)

```markdown
{Proposed new text with **BOLD** for additions/changes}
```markdown

### Rationale

{Why this prevents the PATTERN (affects multiple bug types)}

### Impact Assessment

**Bugs this pattern affected:**
- Issue #{X}: {brief description}
- Issue #{Y}: {brief description}
- Issue #{Z}: {brief description}

**Estimated bugs prevented per epic:** {count} similar bugs
**Estimated debugging time saved:** {X} hours per epic

---

{Repeat for each pattern-based recommendation}
```markdown

---

## Step 4: Update Lessons Learned

### Create/update debugging/lessons_learned.md

**This is DIFFERENT from process_failure_analysis.md:**
- process_failure_analysis.md = Process improvement focus (WHY bugs got through)
- lessons_learned.md = Technical/investigation focus (WHAT bugs were and HOW we found them)

**Format matches feature lessons_learned.md but with debugging focus**

**Template:**

```markdown
# Debugging Lessons Learned - {Feature/Epic Name}

**Feature/Epic:** {name}
**Testing Stage:** {S7.P1 Smoke Testing / S7.P2 QC / S9 Epic Testing / S10 User Testing}
**Date Range:** {start date} - {end date}
**Total Issues:** {count}
**Total Investigation Time:** {hours}

---

## Purpose

This document captures technical lessons from debugging. For process improvement analysis (why bugs got through our workflow), see:
- `debugging/process_failure_analysis.md` - Process gap analysis
- `debugging/guide_update_recommendations.md` - Concrete guide updates

---

## Debugging Phase Lessons

### What Went Well

1. **Issue discovery and tracking**
   - {Positive observation about ISSUES_CHECKLIST.md usage}
   - {Positive observation about issue tracking}

2. **Investigation approach**
   - {What investigation techniques worked well}
   - {What diagnostic approaches were effective}

3. **User collaboration**
   - {Positive observation about user verification}
   - {Positive observation about communication}

### What Didn't Go Well

1. **{Issue or challenge encountered}**
   - Description: {What happened}
   - Impact: {How it affected debugging}
   - Resolution: {How it was resolved}

2. **{Another issue or challenge}**
   - Description: {Details}
   - Impact: {Impact}
   - Resolution: {Resolution}

### Recommendations

- {Recommendation 1 for future debugging sessions}
- {Recommendation 2}
- {Recommendation 3}

---

## Issues Resolved - Technical Summary

### Issue #1: {name}

**Root Cause:**
- {Technical description of what caused the bug}
- {Specific code/logic/data issue}

**Investigation Rounds:** {count}

**Investigation Approach:**
- Round 1: {What was done - code tracing}
- Round 2: {What was done - hypothesis formation}
- Round 3: {What was done - diagnostic testing}
{Continue if more rounds needed}

**Solution Implemented:**
- {Description of fix}
- Files modified: {list}
- Tests added/updated: {count}

**Key Learning:**
- {Technical insight from this bug}
- {What we learned about the codebase}

**Prevention (Technical):**
- Code changes: {Specific code-level prevention}
- Test additions: {Specific tests added}
- Architecture changes: {If any}

**Time Impact:**
- Investigation: {hours}
- Implementation: {hours}
- Verification: {hours}
- Total: {hours}

---

### Issue #2: {name}

**Root Cause:**
{Details...}

**Investigation Rounds:** {count}

**Investigation Approach:**
{Details...}

**Solution Implemented:**
{Details...}

**Key Learning:**
{Details...}

**Prevention (Technical):**
{Details...}

**Time Impact:**
{Details...}

---

{Repeat for each issue}

---

## Technical Patterns Identified

### Pattern #1: {Pattern Name}

**Issues Affected:** Issue #{N}, Issue #{M}

**Common Technical Root Cause:**
- {What technical issue was common across these bugs}

**Common Code Pattern:**
```python
# Example of problematic pattern
{code snippet}
```markdown

**Recommended Solution:**
```python
# Example of fix pattern
{code snippet}
```markdown

---

### Pattern #2: {Pattern Name}

{Repeat structure}

---

## Investigation Techniques

### Techniques That Worked Well

1. **{Technique name}**
   - Description: {What technique was used}
   - Issues where used: Issue #{N}, Issue #{M}
   - Why effective: {Explanation}
   - Recommendation: {When to use this technique}

2. **{Another technique}**
   - {Details...}

### Techniques That Didn't Work

1. **{Technique that failed}**
   - Why attempted: {Reasoning}
   - Why it failed: {Explanation}
   - Alternative used: {What worked instead}
   - Learning: {What we learned}

---

## Testing Insights

### Test Coverage Gaps Discovered

**Gap #1: {description}**
- Discovered during: Issue #{N}
- Why tests missed it: {Explanation}
- Tests added: {Description of new tests}

**Gap #2: {description}**
{Details...}

### Testing Improvements Made

1. **{Improvement 1}**
   - What: {Description}
   - Why: {Rationale}
   - Impact: {How this prevents future bugs}

2. **{Improvement 2}**
   {Details...}

### Recommendations for Future Testing

- {Testing recommendation 1}
- {Testing recommendation 2}
- {Testing recommendation 3}

---

## Code Quality Insights

### Code Issues Discovered

1. **{Code quality issue}**
   - Where found: {Location}
   - Why it's an issue: {Explanation}
   - Fix applied: {Description}

2. **{Another code quality issue}**
   {Details...}

### Architecture Insights

**Insight #1:**
- {What we learned about the architecture}
- {How it affected debugging}
- {Recommendations for future}

**Insight #2:**
{Details...}

---

## Guide Updates Applied

**Note:** For detailed guide update analysis, see `debugging/guide_update_recommendations.md`

### Updates Applied to Guides

**{guide_name}.md (v2.{X}):**
- Section updated: {section name}
- What was added/changed: {brief description}
- Why: {rationale from bug analysis}
- Date applied: {YYYY-MM-DD}

**{another_guide_name}.md:**
{Details...}

### Updates Pending User Review

**{guide_name}.md:**
- Proposed update: {brief description}
- Priority: {High/Medium/Low}
- See: debugging/guide_update_recommendations.md for full proposal

---

## Recommendations for Similar Issues

### If you encounter {symptom type 1}:

1. **First steps:**
   - {Recommendation}
   - {Recommendation}

2. **Investigation approach:**
   - {Recommendation}
   - {Recommendation}

3. **Common causes to check:**
   - {Common cause 1}
   - {Common cause 2}

### If you encounter {symptom type 2}:

{Repeat structure}

---

## Summary

### Key Takeaways

1. **{Takeaway 1}**
   - {Explanation}
   - {Application}

2. **{Takeaway 2}**
   {Details...}

3. **{Takeaway 3}**
   {Details...}

### Time Impact Analysis

**Total debugging time:** {hours}

**Breakdown:**
- Issue discovery: {hours}
- Investigation: {hours}
- Implementation: {hours}
- User verification: {hours}
- Process analysis: {hours}
- Documentation: {hours}

**If bugs found in production:**
- Estimated time: {hours} (without context, reproduction, etc.)
- Regression risk: {High/Medium/Low}

**Time saved by catching in {testing stage}:** {hours}

### Recommendations for Future Features

**Do These Things:**
1. {Practice to continue}
2. {Practice to continue}
3. {Practice to continue}

**Avoid These Things:**
1. {Anti-pattern to avoid}
2. {Anti-pattern to avoid}
3. {Anti-pattern to avoid}

**When Debugging Similar Issues:**
1. {Debugging-specific recommendation}
2. {Debugging-specific recommendation}

---

## Cross-References

**Related Documentation:**
- `debugging/ISSUES_CHECKLIST.md` - Issue tracking master list
- `debugging/process_failure_analysis.md` - Why bugs got through process
- `debugging/guide_update_recommendations.md` - Proposed guide updates
- `debugging/investigation_rounds.md` - Investigation meta-tracker

**Feature/Epic Documentation:**
- `spec.md` - Feature specification
- `implementation_plan.md` - Implementation build guide
- `lessons_learned.md` (main) - Overall feature lessons
- `epic_lessons_learned.md` - Epic-level lessons

---

## Final Metrics

**Debugging Stats:**
- Total issues discovered: {count}
- Issues resolved: {count}
- Investigation rounds used: {total across all issues}
- Average rounds per issue: {average}
- User verification sessions: {count}
- Test coverage before: {percentage}%
- Test coverage after: {percentage}%
- Test pass rate: {percentage}% ({X}/{Y} tests)

**Code Impact:**
- Files modified: {count}
- Lines changed: ~{count}
- Tests added: {count}
- Tests modified: {count}

**Process Improvements:**
- Guide updates proposed: {count} (see guide_update_recommendations.md)
- Process gaps identified: {count} (see process_failure_analysis.md)
- Cross-bug patterns found: {count}

---

*End of debugging/lessons_learned.md*
```bash

---

## Step 5: Loop Back to Testing

**Determine loop-back destination based on where issues were discovered:**

### Feature-Level Loop-Back

**If issues discovered during S7.P1:**

Loop back to: **S7.P1 Step 1** (Import Test)

**Why start at Part 1, not Part 3 where issues were found?**
- Fixes might affect earlier parts (imports, entry points)
- Comprehensive re-validation required
- Ensures no new issues introduced by fixes

**Actions:**
1. Update README Agent Status
2. Return to smoke testing guide
3. Run ALL 3 parts of smoke testing
4. If new issues found → back to debugging
5. If zero issues → proceed to S7.P2

**README Agent Status update:**

```markdown
**Debugging Protocol Complete**

All issues in debugging/ISSUES_CHECKLIST.md are now 🟢 FIXED with user confirmation.

**Next Action:** Loop back to S7.P1 Part 1

**Reason:** Must re-run complete smoke testing after fixes to ensure:
1. Original issues are resolved
2. No new issues were introduced by fixes
3. All 3 smoke test parts pass

**Update README Agent Status:**
- Current Phase: POST_IMPLEMENTATION_SMOKE_TESTING
- Current Guide: stages/s7/s7_p1_smoke_testing.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Returning From: Debugging Protocol
- Issues Resolved: {count}
- Next Action: Run Smoke Test Part 1 (Import Test)

Looping back to smoke testing...
```markdown

---

**If issues discovered during S7.P2:**

Loop back to: **S7.P1 Step 1** (NOT back to QC Round directly)

**Why loop back to smoke testing instead of QC?**
- QC restart protocol: Always restart from smoke testing after fixes
- Ensures foundational smoke tests still pass
- Comprehensive validation before QC rounds

**Actions:**
1. Update README Agent Status
2. Return to smoke testing guide
3. Run all 3 parts of smoke testing
4. Then run all QC rounds (1, 2, 3) again
5. If issues found → back to debugging
6. If zero issues → proceed to S7.P3

---

### Epic-Level Loop-Back

**If issues discovered during S9.P1 (Epic Smoke Testing):**

Loop back to: **S9.P1 Step 1** (Epic Smoke Testing start)

**Actions:**
1. Update EPIC_README Agent Status
2. Return to epic smoke testing guide
3. Run all epic smoke test steps
4. If new issues found → back to epic debugging
5. If zero issues → proceed to S9.P2 (Epic QC Rounds)

**EPIC_README Agent Status update:**

```markdown
**Debugging Protocol Complete**

All issues in epic_name/debugging/ISSUES_CHECKLIST.md are now 🟢 FIXED with user confirmation.

**Next Action:** Loop back to S9.P1 (Epic Smoke Testing) Step 1

**Reason:** Must re-run complete epic testing after fixes to ensure:
1. Original issues are resolved
2. No integration conflicts introduced
3. All epic smoke tests pass

**Update EPIC_README Agent Status:**
- Current Phase: EPIC_FINAL_QC_SMOKE_TESTING
- Current Guide: stages/s9/s9_p1_epic_smoke_testing.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Returning From: Debugging Protocol
- Issues Resolved: {count}
- Next Action: Run Epic Smoke Test Step 1

Looping back to epic smoke testing...
```markdown

---

**If issues discovered during S9.P2 (Epic QC Rounds):**

Loop back to: **S9.P1 Step 1** (Epic Smoke Testing)

**Why?** Same reason as feature-level: restart from smoke testing, not QC.

---

**If issues discovered during S10 (User Testing):**

Loop back to: **S9.P1 Step 1** (Epic Smoke Testing)

**Why S9.P1, not S10?**
- User-reported bugs might affect epic-level integration
- Must re-validate entire epic before returning to user
- S10 is user-driven, can't "loop back" to it
- User will test again after S9 passes

**Actions:**
1. Update EPIC_README Agent Status
2. Inform user: "Fixing bugs, will return to S9 for re-validation"
3. Return to S9.P1 (Epic Smoke Testing)
4. Run epic smoke testing and QC rounds
5. If passes: Inform user fixes are ready, request new user testing session
6. If fails: Back to debugging

**Message to user:**

```markdown
I've resolved all {count} bug(s) you reported during user testing.

**Next Steps:**
1. I'm returning to S9.P1 (Epic Smoke Testing) to re-validate the epic
2. This ensures the bug fixes don't introduce integration issues
3. After epic testing passes, I'll let you know it's ready for another user testing session

**Bugs Fixed:**
{List of issues with brief descriptions}

Re-running epic testing now...
```markdown

---

## Step 6: Re-run Testing

### Feature-Level Re-Testing

**S7.P1: Smoke Testing**

1. **Run all 3 parts:**
   - Part 1: Import Test
   - Part 2: Entry Point Test
   - Part 3: E2E Execution Test

2. **Outcome possibilities:**

   **✅ All parts pass, zero issues:**
   - Smoke testing complete
   - Proceed to S7.P2

   **❌ New issues found:**
   - Add to debugging/ISSUES_CHECKLIST.md
   - Enter debugging protocol again
   - Resolve all issues
   - Loop back to Part 1 again
   - Repeat until zero issues

**S7.P2: QC Rounds**

1. **Run all 3 rounds:**
   - Round 1: Basic Validation
   - Round 2: Deep Verification
   - Round 3: Skeptical Review

2. **Outcome possibilities:**

   **✅ All rounds pass, zero issues:**
   - QC complete
   - Proceed to S7.P3

   **❌ Issues found:**
   - Add to debugging/ISSUES_CHECKLIST.md
   - Enter debugging protocol
   - Resolve all issues
   - Loop back to S7.P1 Step 1 (smoke testing)
   - Repeat until zero issues

---

### Epic-Level Re-Testing

**S9.P1: Epic Smoke Testing**

1. **Run all steps**

2. **Outcome possibilities:**

   **✅ All steps pass, zero issues:**
   - Epic smoke testing complete
   - Proceed to S9.P2 (Epic QC Rounds)

   **❌ New issues found:**
   - Add to epic_name/debugging/ISSUES_CHECKLIST.md
   - Enter debugging protocol
   - Resolve all issues
   - Loop back to S9.P1 Step 1 again
   - Repeat until zero issues

**S9.P2: Epic QC Rounds**

1. **Run all 3 rounds**

2. **Outcome possibilities:**

   **✅ All rounds pass, zero issues:**
   - Epic QC complete
   - Proceed to S9.P3 (Epic Final Review)

   **❌ Issues found:**
   - Add to epic_name/debugging/ISSUES_CHECKLIST.md
   - Enter debugging protocol
   - Resolve all issues
   - Loop back to S9.P1 Step 1 (epic smoke testing)
   - Repeat until zero issues

---

## Integration with Testing Stages

### S7.P1: Smoke Testing Integration

**Add to smoke_testing.md at end of Part 3:**

```markdown
### Part 3 Result Handling

**If Part 3 PASSES:**
- Proceed to S7.P2

**If Part 3 FAILS (issues found):**

1. **Create debugging/ folder** (if doesn't exist)

2. **Create/update debugging/ISSUES_CHECKLIST.md:**
   - Add each discovered issue
   - Set status to 🔴 NOT_STARTED
   - Record "Discovered During: Smoke Part 3"

3. **Enter Debugging Protocol:**
   - Read `debugging/discovery.md`
   - Work through ISSUES_CHECKLIST.md systematically
   - Resolve all issues with user confirmation

4. **Loop back to Smoke Testing Part 1:**
   - After all issues resolved (Phase 5)
   - Re-run all 3 parts
   - Repeat if new issues found

**Update README Agent Status:**
```markdown
**Current Phase:** DEBUGGING_PROTOCOL
**Testing Stage Paused:** S7.P1 Smoke Part 3
**Issues Found:** {count}
**Next Action:** Begin debugging protocol (read debugging/discovery.md)
```text
```markdown

---

### S7.P2: QC Rounds Integration

**Add to qc_rounds.md after each round:**

```markdown
### Round {N} Result Handling

**If Round {N} PASSES:**
- Proceed to Round {N+1} / Final Review

**If Round {N} FAILS (issues found):**

1. **Add issues to debugging/ISSUES_CHECKLIST.md**

2. **Enter Debugging Protocol:**
   - Read `debugging/discovery.md`
   - Resolve all issues

3. **Loop back to Smoke Testing Part 1:**
   - NOT back to QC Round {N}
   - Must re-run smoke tests after fixes
   - Then re-run all QC rounds from Round 1

**Critical:** QC restart protocol applies - always loop back to smoke testing after fixes
```markdown

---

### S9: Epic Testing Integration

**Add to epic_smoke_testing.md and epic_qc_rounds.md:**

```markdown
## Epic Issue Handling

**If epic testing finds issues:**

1. **Create epic_name/debugging/ folder** (if doesn't exist)

2. **Create/update debugging/ISSUES_CHECKLIST.md:**
   - Epic-level issues tracked here
   - Separate from feature-level debugging/

3. **User Testing Integration:**
   - User reports bugs during S10 testing
   - Add to epic_name/debugging/ISSUES_CHECKLIST.md
   - Enter debugging protocol
   - Loop back to S9.P1 (epic smoke testing)

4. **Loop Back:**
   - After all epic issues resolved
   - Re-run epic smoke testing from beginning
   - Repeat until zero issues
```markdown

---

## Resumability After Session Compaction

**To ensure agents can resume debugging protocol seamlessly:**

### README Agent Status Format

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}

**Current Phase:** DEBUGGING_PROTOCOL
**Current Guide:** debugging/loop_back.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Critical Rules from Guide:**
- Verify all issues resolved before loop-back
- Final code review (remove debug artifacts)
- Run full test suite (100% pass required)
- Update lessons learned
- Loop back to START of testing stage

**Debugging Status:**
- Total Issues: {count}
- Fixed (User Confirmed): {count} ✅
- In Progress: 0
- Not Started: 0

**Testing Stage Paused:** {S7.P1 / S7.P2 / S9.P1 / S9.P2}
**Loop Back To:** {S7.P1 Step 1 / S9.P1 Step 1}

**Next Action:** Loop back to testing (Phase 5 complete)

**Files to Check:**
- debugging/ISSUES_CHECKLIST.md - Verify all 🟢 FIXED with ✅ YES
- debugging/lessons_learned.md - Updated with all issues
```

---

## Summary

**Loop-Back Process:**

1. ✅ Verify all issues in ISSUES_CHECKLIST.md are 🟢 FIXED with ✅ YES
2. ✅ Final code review (remove debug artifacts, 100% test pass)
3. ✅ Systematic root cause analysis (MANDATORY)
   - Per-bug process failure analysis
   - Cross-bug pattern analysis
   - Guide update recommendations
4. ✅ Update lessons learned (technical focus)
5. ✅ Determine loop-back destination (S7.P1 Step 1 / S9.P1 Step 1)
6. ✅ Update README/EPIC_README Agent Status
7. ✅ Return to testing guide
8. ✅ Re-run testing from beginning
9. ✅ If new issues → repeat debugging
10. ✅ If zero issues → proceed to next stage

**Loop-Back Destinations:**
- **Feature Smoke Testing (S7.P1)** → Loop back to Part 1
- **Feature QC Rounds (S7.P2)** → Loop back to S7.P1 Step 1
- **Epic Smoke Testing (S9.P1)** → Loop back to Step 1
- **Epic QC Rounds (S9.P2)** → Loop back to S9.P1 Step 1
- **User Testing (S10)** → Loop back to S9.P1 Step 1

**Key Principle:** Always loop back to START of testing stage (not to where issues were found)

---

**END OF PHASE 5 GUIDE**
