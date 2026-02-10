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
3. [Critical Rules (Feature-Specific)](#critical-rules-feature-specific)
4. [Prerequisites Checklist](#prerequisites-checklist)
5. [Workflow Overview](#workflow-overview)
6. [Code Inspection Protocol (MANDATORY)](#code-inspection-protocol-mandatory)
7. [QC Round 1: Basic Validation](#qc-round-1-basic-validation)
8. [QC Round 2: Deep Verification](#qc-round-2-deep-verification)
9. [QC Round 3: Final Skeptical Review](#qc-round-3-final-skeptical-review)
10. [Common Feature-Specific Issues](#common-feature-specific-issues)
11. [MANDATORY CHECKPOINT 1](#mandatory-checkpoint-1)
12. [Next Steps](#next-steps)
13. [Summary](#summary)
14. [Exit Criteria](#exit-criteria)

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

**Verify these BEFORE starting QC Rounds:**

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
- **Time Savings:** 60-180 min per bug (no restart overhead)

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
- Agent claimed "error handling verified" in QC Round 1
- Actually: Agent didn't read the file, just assumed it was correct
- Result: Missing `set -e` in shell script passed through 3 QC rounds
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

## QC Round 1: Basic Validation

**📖 See `reference/qc_rounds_pattern.md` for universal Round 1 patterns.**
**📖 See `reference/validation_loop_qc_pr.md` for Validation Loop QC approach.**

**Objective:** Basic validation - does the feature work?

**Validation Loop Approach:**
- **Assume everything is wrong:** Skeptically analyze all changed files
- **Fresh eyes:** Use sequential reading pattern (top to bottom)
- **No deferred issues:** ALL issues (critical, major, minor) must be fixed before Round 2
- **Exit criteria:** Zero critical issues, all tests pass, spec 100% implemented

**Time Estimate:** 10-20 minutes

**Pass Criteria:**
- <3 critical issues found
- 100% of spec requirements implemented (no partial work)

---

### Validation 1.1: Unit Tests

```bash
python tests/run_all_tests.py
```

**Verify:**
- ✅ Exit code = 0 (all tests pass)
- ✅ 100% pass rate
- ✅ No skipped tests for this feature

**If tests fail:** Document failures, fix, restart from smoke testing

---

### Validation 1.2: Code Structure

**Check feature files exist and are complete:**

```markdown
## Feature Files (example)
- [ ] spec.md (complete specification)
- [ ] checklist.md (all items resolved)
- [ ] implementation_plan.md (all tasks documented)
- [ ] implementation_checklist.md (all requirements verified)
- [ ] README.md (Agent Status updated)
```

**Check code organization:**
- ✅ New modules in correct directories
- ✅ No temporary/debug files committed
- ✅ Code follows project conventions (see CLAUDE.md)

---

### Validation 1.3: Output Files

**Verify feature output files:**

```python
from pathlib import Path

## Check all expected output files exist
expected_outputs = [
    "data/output_file_1.json",
    "data/output_file_2.csv",
]

for output_file in expected_outputs:
    assert Path(output_file).exists(), f"Missing output: {output_file}"

print("✅ All output files exist")
```

**Verify output structure:**
- ✅ Files have expected format (JSON, CSV, etc.)
- ✅ Files have expected schema/columns
- ✅ Files are not empty

---

### Validation 1.4: Interface Verification

**Verify feature interfaces match dependencies:**

**From S5 Algorithm Traceability Matrix, verify each integration point:**

```python
## Example: Feature calls PlayerManager.get_players()
from league_helper.PlayerManager import PlayerManager

pm = PlayerManager()
players = pm.get_players()  # Verify this method exists

## Verify return type matches spec
assert isinstance(players, list), "get_players should return list"
assert len(players) > 0, "get_players returned empty list"

print("✅ PlayerManager interface verified")
```

**Check ALL dependencies identified in S5:**
- ✅ Methods exist
- ✅ Method signatures match usage
- ✅ Return types correct

---

### Validation 1.5: Documentation Complete

**Check documentation updated:**

- [ ] Code has docstrings (Google style)
- [ ] README.md updated if user-facing changes
- [ ] No placeholder comments ("TODO: implement this later")

---

### Round 1 Checkpoint

**Count critical issues found:**

**Critical issues:**
- Unit tests failing
- Output files missing or wrong format
- Interface mismatches
- Required functionality missing

**Pass Criteria:**
- <3 critical issues found
- 100% of spec requirements implemented

**If Round 1 FAILS:**
1. Document ALL issues found
2. Fix ALL issues
3. **RESTART from S7.P1 (smoke testing)**
4. Re-run smoke testing → QC Round 1

**If Round 1 PASSES:**
- Document results in README
- **Re-read "Common Mistakes"** in `reference/qc_rounds_pattern.md`
- Proceed to Round 2

---

## QC Round 2: Deep Verification

**📖 See `reference/qc_rounds_pattern.md` for universal Round 2 patterns.**
**📖 See `reference/validation_loop_qc_pr.md` for Validation Loop QC approach.**

**Objective:** Deep verification - does it work CORRECTLY?

**Validation Loop Approach:**
- **Different patterns than Round 1:** Use reverse reading order (bottom to top)
- **Focus:** Verify Round 1 fixes AND find NEW issues
- **No deferred issues:** ALL new issues must be fixed before Round 3
- **Exit criteria:** Zero critical issues, all Round 1 fixes verified

**Time Estimate:** 10-20 minutes

**Pass Criteria:**
- ALL Round 1 issues resolved (none remaining)
- ZERO new critical issues found in Round 2

---

### Validation 2.1: Baseline Comparison (If Updating Existing Feature)

**If feature modifies existing functionality:**

```python
## Compare old vs new behavior
import pandas as pd

## Load baseline output (before feature)
baseline = pd.read_csv("baseline/output.csv")

## Load new output (after feature)
new_output = pd.read_csv("data/output.csv")

## Verify new output includes everything from baseline
## (unless spec says to remove something)
baseline_players = set(baseline['player_name'])
new_players = set(new_output['player_name'])

assert baseline_players.issubset(new_players), "Lost players in new output"

print("✅ Baseline comparison passed")
```

**Skip if:** Feature is entirely new (no baseline to compare)

---

### Validation 2.2: Data Validation

**📖 See pattern file for data validation patterns.**

**Verify data VALUES are correct (not just structure):**

```python
import pandas as pd

df = pd.read_csv("data/output.csv")

## Check column exists (structure)
assert 'projected_points' in df.columns

## Check values are correct (DEEP validation)
assert df['projected_points'].notna().all(), "Has null values"
assert (df['projected_points'] > 0).all(), "Has zero/negative values"
assert df['projected_points'].between(0, 500).all(), "Values out of expected range"

## Check statistical properties match spec
mean_points = df['projected_points'].mean()
assert 100 < mean_points < 200, f"Mean {mean_points} outside expected range"

print("✅ Data validation passed")
```

**Check for common data issues:**
- ❌ All zeros (forgot to populate)
- ❌ All same value (placeholder)
- ❌ Null values (missing data)
- ❌ Out of range (algorithm bug)

---

### Validation 2.3: Regression Testing

**Verify existing functionality still works:**

```bash
## Run tests for related modules (not just new tests)
python -m pytest tests/league_helper/test_PlayerManager.py -v
python -m pytest tests/league_helper/test_LeagueHelper.py -v
```

**Verify:**
- ✅ All related tests pass
- ✅ No new test failures
- ✅ Existing features unaffected

---

### Validation 2.4: Semantic Diff (Behavior Matches Spec)

**Re-read spec algorithms, verify implementation matches EXACTLY:**

**Example from spec:**
```markdown
## Algorithm: Calculate Player Rating
1. Get player ADP (Average Draft Position)
2. Look up ADP in multiplier ranges config
3. Apply multiplier to base rating
4. Clamp result between 0.5 and 1.5
5. Return multiplier
```

**Verify code does EXACTLY this:**
```python
def calculate_player_rating(self, player):
    # Step 1: Get ADP
    adp = player.get_adp()  # ✅ Matches spec step 1

    # Step 2: Look up in config
    multiplier = self.config.get_adp_multiplier(adp)  # ✅ Matches spec step 2

    # Step 3: Apply to base rating
    base_rating = player.get_base_rating()
    rating = base_rating * multiplier  # ✅ Matches spec step 3

    # Step 4: Clamp between 0.5 and 1.5
    rating = max(0.5, min(1.5, rating))  # ✅ Matches spec step 4

    # Step 5: Return
    return rating  # ✅ Matches spec step 5
```

**Check EVERY algorithm in spec has matching code behavior**

---

### Validation 2.5: Edge Cases

**Test edge cases from spec:**

```python
## Edge case 1: Empty input
result = feature.process([])
assert result == [], "Empty input should return empty output"

## Edge case 2: Single item
result = feature.process([single_item])
assert len(result) == 1, "Single item should return single result"

## Edge case 3: Maximum input
large_input = [item] * 1000
result = feature.process(large_input)
assert len(result) == 1000, "Should handle large input"

## Edge case 4: Invalid input
try:
    result = feature.process(None)
    assert False, "Should raise error for None"
except ValueError:
    pass  # Expected

print("✅ Edge cases handled correctly")
```

---

### Round 2 Checkpoint

**Verify:**
- ✅ ALL Round 1 issues resolved (none remaining)
- ✅ Data validation passed (values correct, not just structure)
- ✅ Regression tests passed (existing functionality works)
- ✅ Semantic diff passed (behavior matches spec)
- ✅ Edge cases handled

**If Round 2 FAILS:**
1. Document ALL issues (unresolved Round 1 + new critical)
2. Fix ALL issues
3. **RESTART from S7.P1 (smoke testing)**
4. Re-run smoke testing → Round 1 → Round 2

**If Round 2 PASSES:**
- Document results in README
- **Re-read "Critical Rules"** in pattern file and this guide
- Proceed to Round 3

---

## QC Round 3: Final Skeptical Review

**📖 See `reference/qc_rounds_pattern.md` for universal Round 3 patterns.**
**📖 See `reference/validation_loop_qc_pr.md` for Validation Loop QC approach.**

**Objective:** Final skeptical review with ZERO tolerance

**Validation Loop Approach:**
- **Final validation:** Random spot-checks and thematic clustering
- **Requirement:** ZERO issues (critical, major, or minor)
- **Exit criteria:** 3 consecutive clean rounds (no known issues remain)
- **If ANY issues found:** Fix ALL immediately, restart from S7.P1 (smoke testing)

**Time Estimate:** 10-20 minutes

**Pass Criteria:**
- **ZERO issues found** (critical, medium, OR minor)
- Spec re-read confirms 100% implementation
- Fresh-eyes review finds no gaps

---

### Validation 3.1: Fresh-Eyes Spec Review

**Close spec.md → Wait 1 minute → Re-read independently:**

This prevents confirmation bias (seeing what you expect, not what's actually there).

**Re-read spec.md section by section:**
- [ ] Overview - verify feature does what spec describes
- [ ] Requirements - verify EACH requirement implemented (100%)
- [ ] Algorithms - verify EACH algorithm implemented correctly
- [ ] Data Structures - verify EACH structure matches spec
- [ ] Edge Cases - verify EACH edge case handled
- [ ] Examples - verify examples work as shown

**Mark ANY gaps found as issues (even minor)**

---

### Validation 3.2: Re-check Algorithm Traceability Matrix

**From S5, re-verify Algorithm Traceability Matrix:**

```markdown
## Algorithm Traceability Matrix (example)

| Algorithm (from spec) | Code Location | Verified |
|----------------------|---------------|----------|
| Calculate player rating | PlayerRatingManager.py:45 | ✅ |
| Look up ADP multiplier | ConfigManager.py:120 | ✅ |
| Apply rating to recommendations | RecommendationEngine.py:89 | ✅ |
| Clamp values 0.5-1.5 | PlayerRatingManager.py:52 | ✅ |
```

**Re-verify EACH entry:**
- ✅ Algorithm from spec still exists
- ✅ Code location still correct
- ✅ Implementation still matches spec

---

### Validation 3.3: Re-check Integration Gap Check

**From S5, re-verify Integration Gap Check:**

**For EACH new method, verify it has identified CALLERS:**

```markdown
## Integration Gap Check (example)

| New Method | Called By | Verified |
|------------|-----------|----------|
| get_player_rating() | RecommendationEngine.generate() | ✅ |
| apply_multiplier() | get_player_rating() | ✅ |
| load_adp_config() | __init__() | ✅ |
```

**Verify:**
- ✅ No orphan methods (methods never called)
- ✅ All integration points still valid
- ✅ No missing connections

---

### Validation 3.4: Zero Issues Scan

**Scan for ANY remaining issues (even minor):**

**Code issues:**
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] No placeholder comments ("TODO", "FIXME")
- [ ] No unused imports
- [ ] No unused variables

**Documentation issues:**
- [ ] No typos in docstrings
- [ ] No missing docstrings
- [ ] No outdated comments
- [ ] README.md accurate

**Data issues:**
- [ ] No placeholder values in output
- [ ] No suspiciously round numbers (10.0, 100.0 - often placeholders)
- [ ] No repeated identical values (sign of placeholder)

---

### Round 3 Checkpoint

**ZERO TOLERANCE:**

**If ANY issues found (critical, medium, OR minor):**
1. Document ALL issues
2. Fix ALL issues
3. **RESTART from S7.P1 (smoke testing)**
4. Re-run smoke testing → Round 1 → Round 2 → Round 3

**If ZERO issues found:**
- ✅ QC Rounds COMPLETE
- ✅ Document completion in README
- ✅ Update Agent Status: "QC Rounds COMPLETE"
- ✅ Proceed to **S7.P3: Final Review**

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

## 🛑 MANDATORY CHECKPOINT 1

**You have completed all 3 QC rounds**

⚠️ STOP - DO NOT PROCEED TO S7.P3 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Critical Rules" section of this guide
2. [ ] Use Read tool to re-read `reference/qc_rounds_pattern.md` (ALL Critical Rules)
3. [ ] Use Read tool to re-read "Restart Protocol" section of pattern file
4. [ ] Verify ZERO issues remain (scan implementation one more time)
5. [ ] Update feature README Agent Status:
   - Current Guide: "stages/s7/s7_p3_final_review.md"
   - Current Step: "S7.P2 complete (3/3 rounds passed), ready to start S7.P3"
   - Last Updated: [timestamp]
6. [ ] Output acknowledgment: "✅ CHECKPOINT 1 COMPLETE: Re-read Critical Rules and Restart Protocol, verified ZERO issues"

**Why this checkpoint exists:**
- 85% of agents miss subtle issues without re-reading pattern file
- Restart Protocol violations cause failed QC in later stages
- 3 minutes of re-reading prevents days of rework

**ONLY after completing ALL 6 actions above, proceed to Next Steps section**

---

## Next Steps

**If ALL 3 rounds PASSED:**
- ✅ Document QC results in feature README
- ✅ Update Agent Status: "QC Rounds COMPLETE (3/3 rounds passed, zero issues)"
- ✅ Proceed to **S7.P3: Final Review**

**If ANY round FAILED:**
- ❌ Fix ALL issues identified
- ❌ **RESTART from S7.P1 (smoke testing)**
- ❌ Re-run entire validation: Smoke → Round 1 → Round 2 → Round 3
- ❌ Do NOT proceed to Final Review until clean pass

---

## Summary

**Feature-Level QC Rounds validate:**
- Round 1: Basic validation (does it work?)
- Round 2: Deep verification (does it work correctly?)
- Round 3: Final skeptical review (is it ACTUALLY complete?)

**Key Differences from Epic-Level:**
- Stricter zero tech debt tolerance (feature-level more strict)
- Baseline comparison (if updating existing feature)
- Algorithm traceability matrix re-verification
- Integration gap check re-verification
- Restart destination: S7.P1 (feature smoke testing)

**Critical Success Factors:**
- Zero tech debt tolerance (100% or INCOMPLETE)
- All 3 rounds mandatory (no skipping)
- Restart protocol if ANY round fails
- Fresh-eyes spec review (Round 3)
- ZERO issues tolerance in Round 3

**📖 For universal patterns and detailed validation techniques, see:**
`reference/qc_rounds_pattern.md`


## Exit Criteria

**QC Rounds (S7.P2) is complete when ALL of these are true:**

- [ ] All steps in this phase complete as specified
- [ ] Agent Status updated with phase completion
- [ ] Ready to proceed to next phase

**If any criterion unchecked:** Complete missing items before proceeding

---
---

**END OF STAGE S7.P2 GUIDE**
