# S7.P2: Feature QC (Validation Loop)

**File:** `s7_p2_qc_rounds.md`

**Purpose:** Comprehensive quality control through validation loop to ensure feature correctness, integration, and completeness.

**Version:** 2.0 (Updated to use validation loop approach)
**Last Updated:** 2026-02-10

**Stage Flow Context:**
```text
S7.P1 (Smoke Testing) →
→ [YOU ARE HERE: S7.P2 - Feature QC Validation Loop] →
→ S7.P3 (Final Review) → S8 (Post-Feature Alignment)
```

---

## Table of Contents

1. [MANDATORY READING PROTOCOL](#mandatory-reading-protocol)
2. [Overview](#overview)
3. [Critical Rules](#critical-rules)
4. [Prerequisites Checklist](#prerequisites-checklist)
5. [Workflow Overview](#workflow-overview)
6. [Detailed Validation Process](#detailed-validation-process)
7. [Code Inspection Protocol (MANDATORY)](#code-inspection-protocol-mandatory)
8. [Common Feature-Specific Issues](#common-feature-specific-issues)
9. [MANDATORY CHECKPOINT 1](#mandatory-checkpoint-1)
10. [Next Steps](#next-steps)
11. [Summary](#summary)
12. [Exit Criteria](#exit-criteria)

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Feature QC, you MUST:**

1. **Read the validation loop guide:** `reference/validation_loop_s7_feature_qc.md`
   - Understand 12 dimensions (7 master + 5 S7 QC-specific)
   - Review fresh eyes patterns per round
   - Understand 3 consecutive clean rounds exit criteria
   - Study master protocol: `reference/validation_loop_master_protocol.md`

2. **Use the phase transition prompt** from `prompts_reference_v2.md`
   - Find "Starting S7.P2: Feature QC Validation Loop" prompt
   - Acknowledge requirements
   - List critical requirements from validation loop guide

3. **Update README Agent Status** with:
   - Current Phase: S7.P2 (Feature QC Validation Loop)
   - Current Guide: reference/validation_loop_s7_feature_qc.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "12 dimensions checked every round", "3 consecutive clean rounds required", "Fix issues immediately (no restart)", "100% tests passing"
   - Next Action: Validation Round 1 - Sequential Review + Test Verification

4. **Verify all prerequisites** (see checklist below)

5. **THEN AND ONLY THEN** begin validation loop

**This is NOT optional.** Reading the validation loop guide ensures you check all 12 dimensions systematically.

---

## Overview

**What is this guide?**
Feature QC validates implemented features through systematic validation loop checking 12 dimensions (7 master + 5 S7-specific) every round until 3 consecutive clean rounds achieved.

**When do you use this guide?**
- S7.P1 complete (Smoke Testing passed all 3 parts)
- S6 execution complete (all implementation done)
- Ready for comprehensive quality validation
- Before S7.P3 (Final Review)

**Key Outputs:**
- ✅ All 12 dimensions validated every round
- ✅ 3 consecutive clean rounds achieved (zero issues found)
- ✅ 100% tests passing (verified every round)
- ✅ All spec requirements implemented (100% coverage)
- ✅ All integration points verified and working
- ✅ Zero tech debt (no TODOs, no partial implementations)
- ✅ Ready for S7.P3 (Final Review)

**Time Estimate:**
4-5 hours (typically 6-8 validation rounds)

**Exit Condition:**
Feature QC is complete when 3 consecutive validation rounds find ZERO issues across all 12 dimensions, all tests passing (100%), and feature is production-ready

---

## 🛑 Critical Rules

**📖 See `reference/validation_loop_master_protocol.md` for universal validation loop principles.**

**S7.P2 Feature QC rules:**

```text
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - Copy to README Agent Status                │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 12 DIMENSIONS CHECKED EVERY ROUND
   - 7 master dimensions (universal)
   - 5 S7 QC dimensions (feature-specific)
   - Cannot skip any dimension
   - Re-read entire codebase each round (no working from memory)

2. ⚠️ 3 CONSECUTIVE CLEAN ROUNDS REQUIRED
   - Clean = ZERO issues found across all 12 dimensions
   - Counter resets if ANY issue found
   - Cannot exit early (must achieve 3 consecutive)
   - Typical: 6-8 rounds total to achieve 3 consecutive clean

3. ⚠️ FIX ISSUES IMMEDIATELY (NO RESTART PROTOCOL)
   - If issues found → Fix ALL immediately
   - Re-run tests after fixes (must pass 100%)
   - Continue validation from current round (no restart needed)
   - New approach: Fix and continue vs old: Fix and restart from beginning

4. ⚠️ 100% TESTS PASSING MANDATORY
   - Run ALL tests EVERY validation round
   - Must achieve 100% pass rate
   - Any test failure = issue (must fix before next round)
   - Verify tests still pass after code changes

5. ⚠️ ZERO TECH DEBT TOLERANCE
   - "90% complete" = INCOMPLETE (must finish)
   - "Placeholder values" = INCOMPLETE (must replace)
   - "Will finish later" = NOT ACCEPTABLE (finish now)
   - NO TODOs, NO temporary solutions, NO deferred features

6. ⚠️ FRESH EYES EVERY ROUND
   - Take 2-5 minute break between rounds
   - Re-read ENTIRE codebase using Read tool
   - Use different reading patterns each round
   - Assume everything is wrong (skeptical fresh perspective)
```

**Validation Loop Principles (from master protocol):**
- Assume everything is wrong (start each round skeptical)
- Fresh eyes required (break + re-read between rounds)
- Zero deferred issues (fix ALL before next round)
- Exit only after 3 consecutive clean rounds
- See `reference/validation_loop_master_protocol.md` for complete principles

---

## Prerequisites Checklist

**Verify these BEFORE starting Validation Loop:**

**From S7.P1:**
- [ ] All 3 smoke test parts passed
- [ ] Part 3 verified OUTPUT DATA VALUES (not just "file exists")
- [ ] Feature executes end-to-end without crashes
- [ ] Output data is correct and reasonable

**Unit Tests:**
- [ ] Run `python tests/run_all_tests.py` → exit code 0
- [ ] All unit tests passing (100% pass rate)

**Documentation:**
- [ ] `implementation_checklist.md` all requirements verified
- [ ] Smoke test results documented in README Agent Status

**If ANY prerequisite not met:** Return to S7.P1 and complete it first.

---

## Workflow Overview

**📖 See `reference/validation_loop_s7_feature_qc.md` for complete validation loop protocol.**

**S7.P2 Validation Loop Process:**

```text
┌─────────────────────────────────────────────────────────────┐
│     S7.P2 FEATURE QC VALIDATION LOOP (Until 3 Clean)       │
└─────────────────────────────────────────────────────────────┘

PREPARATION
   ↓ Read validation_loop_s7_feature_qc.md
   ↓ Create VALIDATION_LOOP_LOG.md
   ↓ Run ALL tests (must pass 100%)

ROUND 1: Sequential Review + Test Verification
   ↓ Check ALL 12 dimensions (7 master + 5 S7 QC)
   ↓ Run tests, read code sequentially, verify requirements
   ↓
   If issues found → Fix ALL immediately → Re-run tests → Round 2
   If clean → Round 2 (count = 1)

ROUND 2: Reverse Review + Integration Focus
   ↓ Check ALL 12 dimensions again (fresh eyes)
   ↓ Run tests, read code in reverse, focus on integration
   ↓
   If issues found → Fix ALL immediately → Re-run tests → Round 3
   If clean → Round 3 (count = 2 or 1 depending on previous)

ROUND 3+: Continue Until 3 Consecutive Clean
   ↓ Check ALL 12 dimensions (different reading patterns)
   ↓ Run tests, spot-checks, E2E verification
   ↓
   Continue until 3 consecutive rounds with ZERO issues
   ↓
VALIDATION COMPLETE → Proceed to S7.P3 (Final Review)
```

**Key Difference from Old Approach:**
- **Old:** 3 sequential rounds checking different concerns → Any issue → Restart from S7.P1
- **New:** N rounds checking ALL concerns → Fix issues immediately → Continue until 3 consecutive clean

**VALIDATION_LOOP_LOG.md:** Create this file at the start of S7.P2 in the feature folder. Log each round's findings, issues fixed, and clean round counter. Format:
```markdown
## Validation Loop Log - {feature_name}

## Round 1 (Sequential Review)
- Issues Found: [list or "None"]
- Fixes Applied: [list or "N/A"]
- Clean Count: 0 (or 1 if no issues)

## Round 2 (Reverse Review)
...
```

**Time Savings:** 60-180 min per bug (no restart overhead)

---

## Detailed Validation Process

**🚨 FOLLOW THE COMPLETE VALIDATION LOOP GUIDE:**

**Primary guide:** `reference/validation_loop_s7_feature_qc.md`

This guide contains:
- Complete 12-dimension checklist (7 master + 5 S7 QC)
- Fresh eyes patterns for each round
- Common issues with examples
- Exit criteria details
- Example validation round sequence

**Do NOT attempt to run S7.P2 without reading the validation loop guide.**

**Quick Summary of What to Check:**

**Master Dimensions (7):**
1. Empirical Verification - All interfaces verified from source
2. Completeness - All requirements implemented
3. Internal Consistency - No contradictions
4. Traceability - All code traces to requirements
5. Clarity & Specificity - Clear naming, specific errors
6. Upstream Alignment - Matches spec and implementation plan
7. Standards Compliance - Follows project standards

**S7 QC Dimensions (5):**
8. Cross-Feature Integration - Integration points work
9. Error Handling Completeness - All errors handled gracefully
10. End-to-End Functionality - Complete user flow works
11. Test Coverage Quality - 100% tests passing, adequate coverage
12. Requirements Completion - 100% complete, zero tech debt

**See validation_loop_s7_feature_qc.md for detailed checklists for each dimension.**
```

---

## 🚨 Code Inspection Protocol (MANDATORY)

**CRITICAL:** QC rounds require ACTUAL code inspection, not checkbox validation.

**Historical Context (KAI-1 Feature 01):**
- Agent claimed "error handling verified" in Validation Round 1
- Actually: Agent didn't read the file, just assumed it was correct
- Result: Missing `set -e` in shell script passed through multiple validation rounds
- Caught only when user asked "did you actually review the code?"
- **This protocol prevents that anti-pattern**

---

### For EVERY file modified/created in this feature:

**Step 1: OPEN THE FILE**
- Use Read tool to load the actual file contents
- Do NOT rely on memory or assumptions
- Do NOT skip this step even if you "know what's in the file"

**Step 2: READ EVERY LINE**
- Not just skim - actually read each line
- Check for commented code, debug statements, TODOs
- Verify code matches implementation plan

**Step 3: VERIFY AGAINST CHECKLIST**
- Line-by-line comparison against QC checklist items
- Provide specific evidence (line numbers, actual code)
- Never say "verified ✅" without showing the evidence

---

### Example - Correct Code Inspection:

❌ **WRONG APPROACH:**
```text
Validation 1.2: Code Structure
- Error handling: ✅ Present
- File structure: ✅ Correct
- Code conventions: ✅ Followed
```

✅ **CORRECT APPROACH:**
```text
Validation 1.2: Code Structure

Opening file: league_helper/PlayerManager.py

Line 45-52: load_adp_data() method
- Error handling present: ✅
  - Line 48: try/except FileNotFoundError
  - Line 50: error logged with context
  - Line 51: returns empty list (graceful degradation)
- Return type matches spec: ✅
  - Returns List[Tuple[str, str, int]]
  - Line 52: return adp_data
- Docstring complete: ✅
  - Lines 45-51: Google style docstring with Args, Returns, Raises

File structure verified: All imports at top (lines 1-8), methods organized by feature
Code conventions verified: Follows CODING_STANDARDS.md (type hints, error context, logging)
```

**Notice the difference:**
- ❌ Wrong: Claims verification without evidence
- ✅ Correct: Shows actual lines inspected, quotes code, provides proof

---

### Why This Matters:

**Without Code Inspection Protocol:**
- Agents claim to verify without reading files
- Issues slip through to PR review or user testing
- QC rounds become meaningless checkbox exercise
- User intervention required (should be caught by agent)

**With Code Inspection Protocol:**
- Agents read actual code before claiming verification
- Issues caught during QC (as designed)
- Evidence-based validation (line numbers, quotes)
- User can trust QC results

---

### Red Flags - Signs You're NOT Inspecting Code:

- ❌ "Verified all requirements ✅" without file reads
- ❌ No line numbers in your validation report
- ❌ No code quotes or examples
- ❌ Generic statements like "looks good"
- ❌ Validating 10+ files in 5 minutes
- ❌ Round 1, 2, and 3 all have identical results

**If you see these patterns, STOP and actually read the code.**

---

## Validation Round Execution

**For complete validation round instructions, see:**
- `reference/validation_loop_s7_feature_qc.md` - Complete 12-dimension checklist
- `reference/validation_loop_master_protocol.md` - Core validation loop principles

**Each validation round:**
1. Check ALL 12 dimensions (7 master + 5 S7 QC-specific)
2. Run all tests (must pass 100%)
3. Fix ANY issues found immediately
4. Take 2-5 minute break before next round
5. Continue until 3 consecutive clean rounds achieved

**Key difference from old approach:**
- **Old (v1.0):** 3 sequential rounds checking different concerns, restart from S7.P1 on any issue
- **New (v2.0):** N rounds checking ALL concerns, fix immediately and continue (no restart needed)

---

## Common Feature-Specific Issues

### Issue 1: Partial Implementation

**Symptom:** Feature "mostly works" but some requirements incomplete

**Example:**
```markdown
Spec requirement: "Update 6 position files (QB, RB, WR, TE, K, DST)"
Implementation: Only updated 4 files (QB, RB, WR, TE)
Agent thought: "80% is good enough, I'll finish the rest later"
```

**Fix:** This is INCOMPLETE. Either implement ALL 6 or get user approval to reduce scope.

### Issue 2: Structure Without Data

**Symptom:** Output files exist with correct structure but wrong values

**Example:**
```python
## WRONG - creates structure but uses placeholders
for player in players:
    ratings.append({'name': player.name, 'rating': 1.0})  # All 1.0!

## CORRECT - actually calculates values
for player in players:
    rating = calculate_rating(player)  # Real calculation
    ratings.append({'name': player.name, 'rating': rating})
```

**Fix:** Verify algorithms ACTUALLY execute (not just create placeholders)

### Issue 3: Spec Drift

**Symptom:** Implementation doesn't match spec because spec was misremembered

**Example:**
```markdown
Spec says: "Clamp rating between 0.5 and 1.5"
Code does: rating = max(0, min(2.0, rating))  # Wrong range!
```

**Fix:** Round 3 fresh-eyes spec review catches this. ALWAYS re-read spec with fresh eyes.

---

## MANDATORY CHECKPOINT 1

**You have achieved 3 consecutive clean validation rounds**

STOP - DO NOT PROCEED TO S7.P3 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Critical Rules" section of this guide
2. [ ] Use Read tool to re-read `reference/validation_loop_s7_feature_qc.md` (12 dimensions)
3. [ ] Verify 3 consecutive clean rounds documented in VALIDATION_LOOP_LOG.md
4. [ ] Verify ZERO issues remain (scan implementation one more time)
5. [ ] Update feature README Agent Status:
   - Current Guide: "stages/s7/s7_p3_final_review.md"
   - Current Step: "S7.P2 complete (3 consecutive clean rounds), ready to start S7.P3"
   - Last Updated: [timestamp]
6. [ ] Output acknowledgment: "CHECKPOINT 1 COMPLETE: Re-read Critical Rules, verified 3 consecutive clean rounds, ZERO issues"

**Why this checkpoint exists:**
- Ensures validation loop was properly executed
- Confirms all 12 dimensions checked every round
- 3 minutes of verification prevents hours of rework

**ONLY after completing ALL 6 actions above, proceed to Next Steps section**

---

## Next Steps

**If 3 consecutive clean rounds achieved:**
- Document QC results in feature README
- Update Agent Status: "S7.P2 COMPLETE (3 consecutive clean rounds, zero issues)"
- Proceed to **S7.P3: Final Review**

**If still finding issues:**
- Fix ALL issues immediately (no deferring)
- Re-run tests (must pass 100%)
- Continue validation loop until 3 consecutive clean rounds
- Do NOT proceed to Final Review until clean pass

---

## Summary

**Feature QC Validation Loop validates:**
- ALL 12 dimensions checked EVERY round (7 master + 5 S7 QC-specific)
- Continue until 3 consecutive clean rounds achieved
- Fix issues immediately (no restart protocol needed)

**12 Dimensions Checked:**
1. Empirical Verification (master)
2. Completeness (master)
3. Internal Consistency (master)
4. Traceability (master)
5. Clarity & Specificity (master)
6. Upstream Alignment (master)
7. Standards Compliance (master)
8. Cross-Feature Integration (S7 QC)
9. Error Handling Completeness (S7 QC)
10. End-to-End Functionality (S7 QC)
11. Test Coverage Quality (S7 QC)
12. Requirements Completion (S7 QC)

**Critical Success Factors:**
- Zero tech debt tolerance (100% or INCOMPLETE)
- 3 consecutive clean rounds required (exit criteria)
- Fix issues immediately and continue (no restart)
- Fresh eyes through breaks + re-reading
- 100% tests passing every round

**For complete validation loop protocol, see:**
`reference/validation_loop_s7_feature_qc.md`


## Exit Criteria

**Validation Loop (S7.P2) is complete when ALL of these are true:**

- [ ] All steps in this phase complete as specified
- [ ] Agent Status updated with phase completion
- [ ] Ready to proceed to next phase

**If any criterion unchecked:** Complete missing items before proceeding

---
---

**END OF STAGE S7.P2 GUIDE**
