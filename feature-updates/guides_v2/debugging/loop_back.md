# PHASE 5: Loop Back to Testing

**Purpose:** After ALL issues resolved, loop back to testing stage

**When to Use:** ALL issues in ISSUES_CHECKLIST.md are 🟢 FIXED with user confirmation

**Previous Phase:** PHASE 4 (User Verification) - See `debugging/resolution.md`

**Next Phase:** Return to testing stage (Stage 5ca, 5cb, or 6a)

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
```

**If any issue is NOT 🟢 FIXED with ✅ YES:**
- STOP - Cannot proceed to loop-back
- Complete investigation and user verification for that issue first
- Return here when ALL issues are resolved

---

## Step 2: Final Code Review

### 2.1: Review debugging/code_changes.md

**Verify:**
- [ ] All changes documented
- [ ] File paths correct
- [ ] Before/after code snippets accurate
- [ ] Reasoning for each change clear

---

### 2.2: Check for leftover artifacts

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
```

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
```

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

## Step 3: Systematic Root Cause Analysis (MANDATORY)

**Purpose:** Analyze why bugs got through research/implementation and how to prevent them

**When:** After all bugs resolved, BEFORE updating lessons learned

**Time Required:** 30-60 minutes (essential for process improvement)

---

### 3.1: Per-Bug Process Failure Analysis

**For EACH bug in ISSUES_CHECKLIST.md, systematically analyze:**

Create a file: `debugging/process_failure_analysis.md`

```markdown
# Process Failure Analysis - {Feature/Epic Name}

**Purpose:** Systematic analysis of why bugs got through our process and how to prevent them

**Date:** {YYYY-MM-DD}

---

## Issue #1: {name}

### Bug Summary
- **What was the bug:** {brief description}
- **Root Cause:** {technical root cause from investigation}
- **Severity:** {High/Medium/Low}
- **Discovery Stage:** {Smoke Testing / QC Round X / Epic Testing / User Testing}

### Why Did This Bug Get Through?

**Research Phase Analysis (Stage 5a - TODO Creation):**
- [ ] Was this scenario considered during Iterations 1-7 (Round 1)?
  - If NO: Why not? {explanation}
  - If YES: Why wasn't it captured in TODO items? {explanation}

- [ ] Was this covered during Iterations 8-16 (Round 2 - Test Coverage)?
  - If NO: What edge case/scenario was missed? {explanation}
  - If YES: Why didn't the test catch it? {explanation}

- [ ] Was this caught during Iteration 23a (Pre-Implementation Spec Audit)?
  - If NO: What audit question should have caught this? {explanation}
  - If YES: How did it still get through? {explanation}

**Implementation Phase Analysis (Stage 5b):**
- [ ] Did the implementation follow the spec correctly?
  - If NO: Why did implementation deviate? {explanation}
  - If YES: Was the spec incomplete/incorrect? {explanation}

- [ ] Were there mini-QC checkpoints that should have caught this?
  - If NO: Should there have been? {explanation}
  - If YES: Why didn't they catch it? {explanation}

- [ ] Did unit tests exist for this code path?
  - If NO: Why was test coverage inadequate? {explanation}
  - If YES: Why didn't tests catch the bug? {explanation}

**Testing Phase Analysis (Stage 5c):**
- [ ] Should smoke testing (Part 3 E2E) have caught this?
  - If NO: Is this a QC-level issue only? {explanation}
  - If YES: Why didn't Part 3 catch it? {explanation}

- [ ] Which QC round should have caught this?
  - Round 1 (Basic Validation): {yes/no and why}
  - Round 2 (Deep Verification): {yes/no and why}
  - Round 3 (Skeptical Review): {yes/no and why}

### Process Gaps Identified

**Research/Planning Gaps:**
1. {specific gap in Stage 5a process}
2. {specific gap in specification process}

**Implementation Gaps:**
1. {specific gap in Stage 5b process}
2. {specific gap in testing approach}

**Testing Gaps:**
1. {specific gap in smoke testing}
2. {specific gap in QC rounds}

### Prevention Strategies

**How to prevent this specific bug type in future:**

1. **Research Phase Improvements:**
   - Update Round 1/2/3 iterations to include: {specific addition}
   - Add new audit question to Iteration 23a: "{question}"
   - Add to common edge cases checklist: {scenario}

2. **Implementation Phase Improvements:**
   - Add mini-QC checkpoint: {specific checkpoint}
   - Update test coverage requirements: {specific requirement}
   - Add to implementation checklist: {specific item}

3. **Testing Phase Improvements:**
   - Update smoke test Part 3 to include: {specific test}
   - Add QC Round {N} verification: {specific verification}
   - Update test data to cover: {specific scenario}

### Guide Updates Required

**Specific guide sections that need updating:**

1. **{guide_name}.md - Section {X}:**
   - Current text: "{quote current text}"
   - Proposed addition/change: "{new text}"
   - Rationale: {why this change prevents bug}

2. **{guide_name}.md - Section {Y}:**
   - Current text: "{quote current text}"
   - Proposed addition/change: "{new text}"
   - Rationale: {why this change prevents bug}

---

## Issue #2: {name}

{Repeat same analysis structure for each bug}

---
```

**Critical Requirements:**

- [ ] Analyze EVERY bug (no exceptions)
- [ ] Be brutally honest about process failures
- [ ] Identify specific guide sections that failed us
- [ ] Propose concrete, actionable guide updates
- [ ] Focus on "why didn't our process catch this?" not "why did bug occur?"

**Anti-Patterns to Avoid:**

❌ "This was just a coding error" - dig deeper into why process didn't prevent it
❌ "We should be more careful" - not actionable, need specific process changes
❌ "Tests should have caught this" - WHY didn't they? What's missing from test strategy?
❌ Generic advice - need SPECIFIC guide sections and SPECIFIC changes

---

### 3.2: Cross-Bug Pattern Analysis

**After analyzing individual bugs, identify patterns:**

Add to `debugging/process_failure_analysis.md`:

```markdown
---

## Cross-Bug Pattern Analysis

### Pattern #1: {Pattern Name}

**Bugs affected:** Issue #{N}, Issue #{M}

**Common process failure:**
{What specific part of the process failed repeatedly}

**Why this pattern exists:**
{Root cause of why our process has this gap}

**Systemic fix required:**
1. {Guide update that prevents this pattern}
2. {Process change that prevents this pattern}
3. {Checklist addition that prevents this pattern}

### Pattern #2: {Pattern Name}

{Repeat for each pattern}

---

## High-Priority Guide Updates

**These guide updates would have prevented multiple bugs:**

### 1. {Guide Name} - {Section}

**Current State:**
- {What the guide currently says or doesn't say}

**Proposed Update:**
```
{Exact text to add/change in guide}
```

**Bugs This Would Prevent:**
- Issue #{N}: {how it would prevent}
- Issue #{M}: {how it would prevent}

**Priority:** {High/Medium/Low}

### 2. {Guide Name} - {Section}

{Repeat for each high-priority update}

---
```

---

### 3.3: Guide Update Recommendations

**After completing process failure analysis, create:**

File: `debugging/guide_update_recommendations.md`

```markdown
# Guide Update Recommendations

**Feature/Epic:** {name}
**Date:** {YYYY-MM-DD}
**Bugs Analyzed:** {count}
**Patterns Identified:** {count}

---

## Critical Updates (Implement Immediately)

### Update #1: {guide_name}.md

**Section to Update:** {section name or "New section"}

**Current Text:**
```
{exact current text, or "Section doesn't exist"}
```

**Proposed New Text:**
```
{exact proposed text with markdown formatting}
```

**Rationale:**
- Prevents bugs: Issue #{N}, Issue #{M}
- Addresses pattern: {pattern name}
- Process gap filled: {specific gap}

**Implementation Steps:**
1. Update {guide_name}.md lines {X-Y}
2. Add to {checklist/template} if needed
3. Update prompts_reference_v2.md if affects phase transitions

---

### Update #2: {guide_name}.md

{Repeat for each critical update}

---

## Moderate Priority Updates (Implement Soon)

{Same structure as critical updates}

---

## Low Priority Updates (Consider for Future)

{Same structure as critical updates}

---

## New Sections Needed

### New Section: {section_name}

**Guide:** {guide_name}.md
**Location:** {where in guide it should go}
**Purpose:** {what gap this fills}

**Proposed Content:**
```markdown
{full proposed section content}
```

**Rationale:** {why this section is needed based on bugs discovered}

---

## Template/Checklist Updates

### {template_name}

**Current template missing:**
- {item that should be in template}
- {item that should be in template}

**Proposed additions:**
```markdown
{exact text to add to template}
```

---

## Summary for Guide Maintainers

**Total recommended updates:** {count}
- Critical: {count}
- Moderate: {count}
- Low: {count}
- New sections: {count}

**Most impactful update:**
{Which single update would prevent most bugs in future}

**Estimated time to implement all critical updates:** {hours}

---
```

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
**Testing Stage:** {Stage 5ca Smoke Testing / Stage 5cb QC / Stage 6 Epic Testing / Stage 7 User Testing}
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
```

**Recommended Solution:**
```python
# Example of fix pattern
{code snippet}
```

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
- `debugging/code_changes.md` - All code modifications
- `debugging/investigation_rounds.md` - Investigation meta-tracker

**Feature/Epic Documentation:**
- `spec.md` - Feature specification
- `todo.md` - Implementation task list
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
```

---

## Step 5: Loop Back to Testing

**Determine loop-back destination based on where issues were discovered:**

### Feature-Level Loop-Back

**If issues discovered during Stage 5ca (Smoke Testing):**

Loop back to: **Stage 5ca Part 1** (Import Test)

**Why start at Part 1, not Part 3 where issues were found?**
- Fixes might affect earlier parts (imports, entry points)
- Comprehensive re-validation required
- Ensures no new issues introduced by fixes

**Actions:**
1. Update README Agent Status
2. Return to smoke testing guide
3. Run ALL 3 parts of smoke testing
4. If new issues found → back to debugging
5. If zero issues → proceed to Stage 5cb (QC Rounds)

**README Agent Status update:**

```markdown
**Debugging Protocol Complete**

All issues in debugging/ISSUES_CHECKLIST.md are now 🟢 FIXED with user confirmation.

**Next Action:** Loop back to Stage 5ca (Smoke Testing) Part 1

**Reason:** Must re-run complete smoke testing after fixes to ensure:
1. Original issues are resolved
2. No new issues were introduced by fixes
3. All 3 smoke test parts pass

**Update README Agent Status:**
- Current Phase: POST_IMPLEMENTATION_SMOKE_TESTING
- Current Guide: stages/stage_5/smoke_testing.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Returning From: Debugging Protocol
- Issues Resolved: {count}
- Next Action: Run Smoke Test Part 1 (Import Test)

Looping back to smoke testing...
```

---

**If issues discovered during Stage 5cb (QC Rounds):**

Loop back to: **Stage 5ca Part 1** (NOT back to QC Round directly)

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
6. If zero issues → proceed to Stage 5cc (Final Review)

---

### Epic-Level Loop-Back

**If issues discovered during Stage 6a (Epic Smoke Testing):**

Loop back to: **Stage 6a Step 1** (Epic Smoke Testing start)

**Actions:**
1. Update EPIC_README Agent Status
2. Return to epic smoke testing guide
3. Run all epic smoke test steps
4. If new issues found → back to epic debugging
5. If zero issues → proceed to Stage 6b (Epic QC Rounds)

**EPIC_README Agent Status update:**

```markdown
**Debugging Protocol Complete**

All issues in epic_name/debugging/ISSUES_CHECKLIST.md are now 🟢 FIXED with user confirmation.

**Next Action:** Loop back to Stage 6a (Epic Smoke Testing) Step 1

**Reason:** Must re-run complete epic testing after fixes to ensure:
1. Original issues are resolved
2. No integration conflicts introduced
3. All epic smoke tests pass

**Update EPIC_README Agent Status:**
- Current Phase: EPIC_FINAL_QC_SMOKE_TESTING
- Current Guide: stages/stage_6/epic_smoke_testing.md
- Guide Last Read: {YYYY-MM-DD HH:MM}
- Returning From: Debugging Protocol
- Issues Resolved: {count}
- Next Action: Run Epic Smoke Test Step 1

Looping back to epic smoke testing...
```

---

**If issues discovered during Stage 6b (Epic QC Rounds):**

Loop back to: **Stage 6a Step 1** (Epic Smoke Testing)

**Why?** Same reason as feature-level: restart from smoke testing, not QC.

---

**If issues discovered during Stage 7 (User Testing):**

Loop back to: **Stage 6a Step 1** (Epic Smoke Testing)

**Why Stage 6a, not Stage 7?**
- User-reported bugs might affect epic-level integration
- Must re-validate entire epic before returning to user
- Stage 7 is user-driven, can't "loop back" to it
- User will test again after Stage 6 passes

**Actions:**
1. Update EPIC_README Agent Status
2. Inform user: "Fixing bugs, will return to Stage 6 for re-validation"
3. Return to Stage 6a (Epic Smoke Testing)
4. Run epic smoke testing and QC rounds
5. If passes: Inform user fixes are ready, request new user testing session
6. If fails: Back to debugging

**Message to user:**

```markdown
I've resolved all {count} bug(s) you reported during user testing.

**Next Steps:**
1. I'm returning to Stage 6a (Epic Smoke Testing) to re-validate the epic
2. This ensures the bug fixes don't introduce integration issues
3. After epic testing passes, I'll let you know it's ready for another user testing session

**Bugs Fixed:**
{List of issues with brief descriptions}

Re-running epic testing now...
```

---

## Step 6: Re-run Testing

### Feature-Level Re-Testing

**Stage 5ca: Smoke Testing**

1. **Run all 3 parts:**
   - Part 1: Import Test
   - Part 2: Entry Point Test
   - Part 3: E2E Execution Test

2. **Outcome possibilities:**

   **✅ All parts pass, zero issues:**
   - Smoke testing complete
   - Proceed to Stage 5cb (QC Rounds)

   **❌ New issues found:**
   - Add to debugging/ISSUES_CHECKLIST.md
   - Enter debugging protocol again
   - Resolve all issues
   - Loop back to Part 1 again
   - Repeat until zero issues

**Stage 5cb: QC Rounds**

1. **Run all 3 rounds:**
   - Round 1: Basic Validation
   - Round 2: Deep Verification
   - Round 3: Skeptical Review

2. **Outcome possibilities:**

   **✅ All rounds pass, zero issues:**
   - QC complete
   - Proceed to Stage 5cc (Final Review)

   **❌ Issues found:**
   - Add to debugging/ISSUES_CHECKLIST.md
   - Enter debugging protocol
   - Resolve all issues
   - Loop back to Stage 5ca Part 1 (smoke testing)
   - Repeat until zero issues

---

### Epic-Level Re-Testing

**Stage 6a: Epic Smoke Testing**

1. **Run all steps**

2. **Outcome possibilities:**

   **✅ All steps pass, zero issues:**
   - Epic smoke testing complete
   - Proceed to Stage 6b (Epic QC Rounds)

   **❌ New issues found:**
   - Add to epic_name/debugging/ISSUES_CHECKLIST.md
   - Enter debugging protocol
   - Resolve all issues
   - Loop back to Stage 6a Step 1 again
   - Repeat until zero issues

**Stage 6b: Epic QC Rounds**

1. **Run all 3 rounds**

2. **Outcome possibilities:**

   **✅ All rounds pass, zero issues:**
   - Epic QC complete
   - Proceed to Stage 6c (Epic Final Review)

   **❌ Issues found:**
   - Add to epic_name/debugging/ISSUES_CHECKLIST.md
   - Enter debugging protocol
   - Resolve all issues
   - Loop back to Stage 6a Step 1 (epic smoke testing)
   - Repeat until zero issues

---

## Integration with Testing Stages

### Stage 5ca: Smoke Testing Integration

**Add to smoke_testing.md at end of Part 3:**

```markdown
### Part 3 Result Handling

**If Part 3 PASSES:**
- Proceed to Stage 5cb (QC Rounds)

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
**Testing Stage Paused:** Stage 5ca Smoke Part 3
**Issues Found:** {count}
**Next Action:** Begin debugging protocol (read debugging/discovery.md)
```
```

---

### Stage 5cb: QC Rounds Integration

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
```

---

### Stage 6: Epic Testing Integration

**Add to epic_smoke_testing.md and epic_qc_rounds.md:**

```markdown
## Epic Issue Handling

**If epic testing finds issues:**

1. **Create epic_name/debugging/ folder** (if doesn't exist)

2. **Create/update debugging/ISSUES_CHECKLIST.md:**
   - Epic-level issues tracked here
   - Separate from feature-level debugging/

3. **User Testing Integration:**
   - User reports bugs during Stage 7 testing
   - Add to epic_name/debugging/ISSUES_CHECKLIST.md
   - Enter debugging protocol
   - Loop back to Stage 6a (epic smoke testing)

4. **Loop Back:**
   - After all epic issues resolved
   - Re-run epic smoke testing from beginning
   - Repeat until zero issues
```

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

**Testing Stage Paused:** {Stage 5ca / Stage 5cb / Stage 6a / Stage 6b}
**Loop Back To:** {Stage 5ca Part 1 / Stage 6a Step 1}

**Next Action:** Loop back to testing (Phase 5 complete)

**Files to Check:**
- debugging/ISSUES_CHECKLIST.md - Verify all 🟢 FIXED with ✅ YES
- debugging/lessons_learned.md - Updated with all issues
- debugging/code_changes.md - All changes documented
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
5. ✅ Determine loop-back destination (Stage 5ca Part 1 / Stage 6a Step 1)
6. ✅ Update README/EPIC_README Agent Status
7. ✅ Return to testing guide
8. ✅ Re-run testing from beginning
9. ✅ If new issues → repeat debugging
10. ✅ If zero issues → proceed to next stage

**Loop-Back Destinations:**
- **Feature Smoke Testing (Stage 5ca)** → Loop back to Part 1
- **Feature QC Rounds (Stage 5cb)** → Loop back to Stage 5ca Part 1
- **Epic Smoke Testing (Stage 6a)** → Loop back to Step 1
- **Epic QC Rounds (Stage 6b)** → Loop back to Stage 6a Step 1
- **User Testing (Stage 7)** → Loop back to Stage 6a Step 1

**Key Principle:** Always loop back to START of testing stage (not to where issues were found)

---

**END OF PHASE 5 GUIDE**
