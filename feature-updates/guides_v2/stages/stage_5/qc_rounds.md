# STAGE 5cb: QC Rounds Guide (Post-Implementation - Part 2)

**Purpose:** Comprehensive quality control through 3 validation rounds to ensure feature correctness, data quality, and completeness.

**Stage Flow Context:**
```
Stage 5ca (Smoke Testing) →
→ [YOU ARE HERE: Stage 5cb - QC Rounds] →
→ Stage 5cc (Final Review) → Stage 5d (Cross-Feature Alignment)
```

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting QC Rounds, you MUST:**

1. **Read the QC rounds pattern:** `reference/qc_rounds_pattern.md`
   - Understand universal 3-round QC workflow
   - Review critical rules that apply to ALL QC rounds
   - Study restart protocol and common mistakes

2. **Use the phase transition prompt** from `prompts/stage_5_prompts.md`
   - Find "Starting Stage 5c (Phase 2): QC Rounds" prompt
   - Acknowledge requirements
   - List critical requirements from this guide

3. **Update README Agent Status** with:
   - Current Phase: POST_IMPLEMENTATION_QC_ROUNDS
   - Current Guide: stages/stage_5/qc_rounds.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "3 rounds MANDATORY", "QC restart if ANY issues", "Round 3 = zero issues or restart"
   - Next Action: QC Round 1 - Basic Validation

4. **Verify all prerequisites** (see checklist below)

5. **THEN AND ONLY THEN** begin QC rounds

**This is NOT optional.** Reading both the pattern and this guide ensures comprehensive validation.

---

## Quick Start

**What is this stage?**
Feature-level QC Rounds perform 3 progressively deeper quality checks (Basic Validation, Deep Verification, Final Skeptical Review) with zero tech debt tolerance. See `reference/qc_rounds_pattern.md` for universal workflow.

**When do you use this guide?**
- Stage 5ca complete (Smoke Testing passed all 3 parts)
- Ready for comprehensive quality validation
- Before final review

**Key Outputs:**
- ✅ Round 1 PASSED: Basic Validation (<3 critical issues, 100% requirements met)
- ✅ Round 2 PASSED: Deep Verification (all Round 1 issues resolved, zero new critical)
- ✅ Round 3 PASSED: Final Skeptical Review (ZERO issues found)
- ✅ All issues fixed with zero tech debt
- ✅ Ready for Stage 5cc (Final Review)

**Time Estimate:**
30-60 minutes (all 3 rounds, assuming no major issues)

**Exit Condition:**
QC Rounds are complete when all 3 rounds pass (Round 3 with ZERO issues), no tech debt remains, and you're ready to proceed to Final Review

---

## 🛑 Critical Rules (Feature-Specific)

**📖 See `reference/qc_rounds_pattern.md` for universal critical rules.**

**Feature-specific rules for Stage 5cb:**

```
┌─────────────────────────────────────────────────────────────┐
│ FEATURE-SPECIFIC RULES - Add to README Agent Status         │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ZERO TECH DEBT TOLERANCE (Feature-level is stricter than epic-level)
   - "90% complete" = INCOMPLETE = RESTART
   - "Placeholder values" = INCOMPLETE = RESTART
   - "Will finish later" = INCOMPLETE = RESTART
   - Feature must be 100% production-ready

2. ⚠️ QC RESTART PROTOCOL (Feature-specific)
   - If Round 1: ≥3 critical OR <100% requirements → RESTART from smoke testing
   - If Round 2: Any Round 1 issues unresolved OR new critical → RESTART
   - If Round 3: ANY issues (critical OR minor) → RESTART
   - Restart destination: Stage 5ca (Feature Smoke Testing)

3. ⚠️ Algorithm verification MANDATORY
   - Re-check Algorithm Traceability Matrix from Stage 5a
   - Every algorithm in spec must map to exact code location
   - Code behavior must match spec EXACTLY

4. ⚠️ 100% requirement completion REQUIRED
   - ALL spec requirements implemented
   - ALL checklist items verified
   - NO "we'll add that later" items
```

**Universal rules (from pattern file):**
- All 3 rounds mandatory
- Each round has unique focus
- Verify DATA VALUES (not just structure)
- Re-reading checkpoints mandatory
- See `reference/qc_rounds_pattern.md` for complete list

---

## Prerequisites Checklist

**Verify these BEFORE starting QC Rounds:**

**From Stage 5ca (Smoke Testing):**
- [ ] All 3 smoke test parts passed
- [ ] Part 3 verified OUTPUT DATA VALUES (not just "file exists")
- [ ] Feature executes end-to-end without crashes
- [ ] Output data is correct and reasonable

**Unit Tests:**
- [ ] Run `python tests/run_all_tests.py` → exit code 0
- [ ] All unit tests passing (100% pass rate)

**Documentation:**
- [ ] `code_changes.md` fully updated
- [ ] `implementation_checklist.md` all requirements verified
- [ ] Smoke test results documented in README Agent Status

**If ANY prerequisite not met:** Return to Stage 5ca and complete it first.

---

## Workflow Overview

**📖 See `reference/qc_rounds_pattern.md` for universal workflow details.**

**Feature-specific workflow for Stage 5cb:**

```
┌─────────────────────────────────────────────────────────────┐
│         FEATURE-LEVEL QC ROUNDS (3 Rounds)                  │
└─────────────────────────────────────────────────────────────┘

Round 1: Basic Validation (10-20 min)
   ↓ Unit tests, code structure, output files, interfaces, docs
   ↓ Pass: <3 critical issues, 100% requirements met
   ↓
   If PASS → Round 2
   If FAIL → Fix, RESTART from smoke testing (Stage 5ca)

Round 2: Deep Verification (10-20 min)
   ↓ Baseline comparison, data validation, regression, edge cases
   ↓ Pass: ALL Round 1 issues resolved + zero new critical
   ↓
   If PASS → Round 3
   If FAIL → Fix, RESTART from smoke testing

Round 3: Final Skeptical Review (10-20 min)
   ↓ Re-read spec with fresh eyes, re-check matrices
   ↓ Pass: ZERO issues (critical, medium, OR minor)
   ↓
   If PASS → QC complete, proceed to Stage 5cc
   If FAIL → Fix, RESTART from smoke testing
```

---

## QC Round 1: Basic Validation

**📖 See `reference/qc_rounds_pattern.md` for universal Round 1 patterns.**

**Objective:** Basic validation - does the feature work?

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
- [ ] todo.md (all tasks done)
- [ ] code_changes.md (all changes documented)
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

# Check all expected output files exist
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

**From Stage 5a Algorithm Traceability Matrix, verify each integration point:**

```python
# Example: Feature calls PlayerManager.get_players()
from league_helper.PlayerManager import PlayerManager

pm = PlayerManager()
players = pm.get_players()  # Verify this method exists

# Verify return type matches spec
assert isinstance(players, list), "get_players should return list"
assert len(players) > 0, "get_players returned empty list"

print("✅ PlayerManager interface verified")
```

**Check ALL dependencies identified in Stage 5a:**
- ✅ Methods exist
- ✅ Method signatures match usage
- ✅ Return types correct

---

### Validation 1.5: Documentation Complete

**Check documentation updated:**

- [ ] Code has docstrings (Google style)
- [ ] README.md updated if user-facing changes
- [ ] code_changes.md lists all modified files
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
3. **RESTART from Stage 5ca (smoke testing)**
4. Re-run smoke testing → QC Round 1

**If Round 1 PASSES:**
- Document results in README
- **Re-read "Common Mistakes"** in `reference/qc_rounds_pattern.md`
- Proceed to Round 2

---

## QC Round 2: Deep Verification

**📖 See `reference/qc_rounds_pattern.md` for universal Round 2 patterns.**

**Objective:** Deep verification - does it work CORRECTLY?

**Time Estimate:** 10-20 minutes

**Pass Criteria:**
- ALL Round 1 issues resolved (none remaining)
- ZERO new critical issues found in Round 2

---

### Validation 2.1: Baseline Comparison (If Updating Existing Feature)

**If feature modifies existing functionality:**

```python
# Compare old vs new behavior
import pandas as pd

# Load baseline output (before feature)
baseline = pd.read_csv("baseline/output.csv")

# Load new output (after feature)
new_output = pd.read_csv("data/output.csv")

# Verify new output includes everything from baseline
# (unless spec says to remove something)
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

# Check column exists (structure)
assert 'projected_points' in df.columns

# Check values are correct (DEEP validation)
assert df['projected_points'].notna().all(), "Has null values"
assert (df['projected_points'] > 0).all(), "Has zero/negative values"
assert df['projected_points'].between(0, 500).all(), "Values out of expected range"

# Check statistical properties match spec
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
# Run tests for related modules (not just new tests)
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
# Edge case 1: Empty input
result = feature.process([])
assert result == [], "Empty input should return empty output"

# Edge case 2: Single item
result = feature.process([single_item])
assert len(result) == 1, "Single item should return single result"

# Edge case 3: Maximum input
large_input = [item] * 1000
result = feature.process(large_input)
assert len(result) == 1000, "Should handle large input"

# Edge case 4: Invalid input
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
3. **RESTART from Stage 5ca (smoke testing)**
4. Re-run smoke testing → Round 1 → Round 2

**If Round 2 PASSES:**
- Document results in README
- **Re-read "Critical Rules"** in pattern file and this guide
- Proceed to Round 3

---

## QC Round 3: Final Skeptical Review

**📖 See `reference/qc_rounds_pattern.md` for universal Round 3 patterns.**

**Objective:** Final skeptical review with ZERO tolerance

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

**From Stage 5a, re-verify Algorithm Traceability Matrix:**

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

**From Stage 5a, re-verify Integration Gap Check:**

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
3. **RESTART from Stage 5ca (smoke testing)**
4. Re-run smoke testing → Round 1 → Round 2 → Round 3

**If ZERO issues found:**
- ✅ QC Rounds COMPLETE
- ✅ Document completion in README
- ✅ Update Agent Status: "QC Rounds COMPLETE"
- ✅ Proceed to **Stage 5cc: Final Review**

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
# WRONG - creates structure but uses placeholders
for player in players:
    ratings.append({'name': player.name, 'rating': 1.0})  # All 1.0!

# CORRECT - actually calculates values
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

## Re-Reading Checkpoint

**After Round 3:**

1. **Re-read ALL Critical Rules** (pattern file + this guide)
2. **Re-read Restart Protocol** (pattern file)
3. **Verify ZERO issues** (scan one more time)
4. **Update README Agent Status**

---

## Next Steps

**If ALL 3 rounds PASSED:**
- ✅ Document QC results in feature README
- ✅ Update Agent Status: "QC Rounds COMPLETE (3/3 rounds passed, zero issues)"
- ✅ Proceed to **Stage 5cc: Final Review**

**If ANY round FAILED:**
- ❌ Fix ALL issues identified
- ❌ **RESTART from Stage 5ca (smoke testing)**
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
- Restart destination: Stage 5ca (feature smoke testing)

**Critical Success Factors:**
- Zero tech debt tolerance (100% or INCOMPLETE)
- All 3 rounds mandatory (no skipping)
- Restart protocol if ANY round fails
- Fresh-eyes spec review (Round 3)
- ZERO issues tolerance in Round 3

**📖 For universal patterns and detailed validation techniques, see:**
`reference/qc_rounds_pattern.md`

---

**END OF STAGE 5cb GUIDE**
