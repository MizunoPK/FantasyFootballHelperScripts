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

1. **Use the phase transition prompt** from `prompts_reference_v2.md`
   - Find "Starting Stage 5cb (QC Rounds)" prompt
   - Speak it out loud (acknowledge requirements)
   - List critical requirements from this guide

2. **Update README Agent Status** with:
   - Current Phase: POST_IMPLEMENTATION (QC Rounds)
   - Current Guide: STAGE_5cb_qc_rounds_guide.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "3 rounds MANDATORY", "QC restart if ANY issues", "Round 3 = zero issues or restart"
   - Next Action: QC Round 1 - Basic Validation

3. **Verify all prerequisites** (see checklist below)

4. **THEN AND ONLY THEN** begin QC rounds

**This is NOT optional.** Reading this guide ensures you complete all validation rounds.

---

## Quick Start

**Goal:** Comprehensive validation through 3 progressively deeper QC rounds.

**3 Mandatory Rounds:**
1. **QC Round 1: Basic Validation** - Tests, structure, interfaces
2. **QC Round 2: Deep Verification** - Baseline, logs, data quality, edge cases
3. **QC Round 3: Final Skeptical Review** - Fresh eyes, re-read specs, zero tolerance

**Critical:** Must complete ALL 3 rounds even if first two pass perfectly

**If ANY issues found:** Follow QC Restart Protocol (restart from smoke testing)

**Output artifacts:**
- ✅ Round 1 passed (<3 critical issues, 100% requirements met)
- ✅ Round 2 passed (all Round 1 issues resolved, zero new critical issues)
- ✅ Round 3 passed (ZERO issues found)

---

## 🛑 Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 3 ROUNDS ARE MANDATORY
   - Cannot skip any round
   - Must complete in order (Round 1 → 2 → 3)
   - Each round has DIFFERENT focus

2. ⚠️ QC RESTART PROTOCOL
   - If Round 1: ≥3 critical issues OR <100% requirements met → RESTART
   - If Round 2: Any Round 1 issues unresolved OR new critical issues → RESTART
   - If Round 3: ANY issues found → RESTART
   - Restart = Re-run smoke testing + all 3 QC rounds

3. ⚠️ NO PARTIAL WORK ACCEPTED - ZERO TECH DEBT TOLERANCE
   - "File structure correct but data pending" = INCOMPLETE (not acceptable)
   - "Method exists but returns placeholder values" = INCOMPLETE (not acceptable)
   - "Stat arrays created but filled with zeros" = INCOMPLETE (not acceptable)
   - "90% complete, will finish later" = INCOMPLETE (not acceptable)
   - Rule: If feature cannot achieve 100% of spec requirements, it's INCOMPLETE
   - NO shortcuts, NO "temporary" solutions, NO deferred work
   - Feature must be production-ready with ZERO tech debt

4. ⚠️ EACH ROUND HAS UNIQUE FOCUS
   - Round 1: Basic validation (does it work?)
   - Round 2: Deep verification (does it work correctly?)
   - Round 3: Skeptical review (is it ACTUALLY complete?)
   - Cannot skip rounds - each catches different issues

5. ⚠️ DATA VALUES NOT JUST STRUCTURE
   - Every round must verify data VALUES are correct
   - Example: Don't just check "column exists", verify values make sense
   - Example: Don't just check "logs exist", verify no unexpected WARNINGs

6. ⚠️ RE-READING CHECKPOINTS
   - After Round 1 → re-read "Common Mistakes"
   - After Round 2 → re-read critical rules
   - Before Round 3 → re-read spec with fresh eyes

7. ⚠️ ALGORITHM VERIFICATION
   - Implementation must match spec EXACTLY
   - Re-check Algorithm Traceability Matrix from Stage 5a
   - Every algorithm in spec must map to exact code location
   - Code behavior must match spec behavior

8. ⚠️ 100% REQUIREMENT COMPLETION
   - ALL spec requirements must be implemented
   - ALL checklist items must be verified
   - NO "we'll add that later" items
   - Feature is DONE or NOT DONE (no partial credit)
```

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

```
┌─────────────────────────────────────────────────────────────┐
│                   QC ROUNDS WORKFLOW                        │
└─────────────────────────────────────────────────────────────┘

QC Round 1: Basic Validation
   ├─ Unit tests pass (100%)
   ├─ Code matches spec structurally
   ├─ Tests use real objects (not excessive mocking)
   ├─ Output files validate CONTENT (not just existence)
   ├─ Interfaces verified against actual classes
   ↓
   Pass criteria: <3 critical issues, 100% requirements met
   If PASS → Round 2
   If FAIL → QC Restart Protocol

Re-Reading Checkpoint #1
   ↓ Re-read "Common Mistakes"

QC Round 2: Deep Verification
   ├─ Baseline comparison (if similar feature exists)
   ├─ Output validation (values in range, no zeros/nulls)
   ├─ No regressions (new feature doesn't break existing)
   ├─ Log quality (no unexpected WARNING/ERROR)
   ├─ Semantic diff check (intentional vs accidental changes)
   ├─ Edge cases handled
   ↓
   Pass criteria: ALL Round 1 issues resolved + zero new critical issues
   If PASS → Round 3
   If FAIL → QC Restart Protocol

Re-Reading Checkpoint #2
   ↓ Re-read Critical Rules

QC Round 3: Final Skeptical Review
   ├─ Re-read spec.md with fresh eyes
   ├─ Re-check Algorithm Traceability Matrix
   ├─ Re-run smoke test final time
   ├─ Final question: "Is feature ACTUALLY complete?"
   ↓
   Pass criteria: ZERO issues found
   If PASS → Proceed to Stage 5cc
   If FAIL (ANY issues) → QC Restart Protocol

QC Restart Protocol (if triggered)
   ↓ Fix ALL issues
   ↓ Re-run smoke testing (all 3 parts)
   ↓ Re-run QC Round 1, 2, 3 (fresh validation)
   ↓ Continue until all rounds pass
```

---

## QC Round 1: Basic Validation

**Purpose:** Verify fundamental correctness (tests, structure, interfaces)

**Pass Criteria:** <3 critical issues, 100% of requirements met

---

### Round 1 Checklist

Work through each section systematically. Check ALL boxes.

---

#### 1. Unit Tests Validation

- [ ] Run `python tests/run_all_tests.py` → exit code 0
- [ ] All new tests pass (100% pass rate)
- [ ] Tests use REAL objects (not excessive mocking)
  - ✅ Good: Mock file I/O, external APIs
  - ❌ Bad: Mock internal classes that should be tested
- [ ] Tests verify behavior (not just "method was called")

**Real-World Example - Excessive Mocking:**
```python
# ❌ BAD - Mocking everything, not testing real behavior
def test_calculate_score(mock_config, mock_player, mock_multiplier):
    mock_multiplier.return_value = 1.5
    mock_player.projected_points = 100
    result = calculate_score(mock_player, mock_config)
    assert result == 150  # This just tests your mock, not real code

# ✅ GOOD - Use real objects, mock only external dependencies
def test_calculate_score(real_config, real_player):
    # real_player is actual FantasyPlayer object
    # real_config is actual ConfigManager object
    result = calculate_score(real_player, real_config)
    assert result > real_player.projected_points  # Tests real calculation
```

---

#### 2. Code Structure Validation

- [ ] Code matches spec.md structure
- [ ] All spec requirements have corresponding code
- [ ] Algorithm Traceability Matrix still valid (from Stage 5a iteration 4)
  - Every algorithm in spec maps to exact code location
  - Code behavior matches spec behavior
- [ ] No placeholder implementations (e.g., `pass`, `return None`)

**Verification:**
```markdown
## Algorithm Traceability Matrix Verification

Algorithm from spec: "Calculate ADP multiplier based on rank"
Implementation location: PlayerManager._calculate_adp_multiplier() (line 234)
Behavior verified: ✅ Matches spec (multiplier = 1.0 + (500-rank)/500 * 0.5)
```

---

#### 3. Output File Validation

- [ ] All expected output files created
- [ ] **Output files contain CORRECT DATA** (not just structure)
  - ❌ "File has 1000 rows" - not sufficient
  - ✅ "File has 1000 rows, avg value 245.3, no zeros" - good
- [ ] File formats match spec (CSV columns, JSON structure, etc.)
- [ ] No empty files where data expected

**Example:**
```python
# Verify output file quality
df = pd.read_csv("data/output.csv")

# Structure checks
assert len(df) == 1000, f"Expected 1000 rows, got {len(df)}"
assert 'player_name' in df.columns, "Missing player_name column"

# Data quality checks (not just structure)
assert df['projected_points'].mean() > 200, "Average points too low"
assert df['projected_points'].max() < 500, "Max points unreasonably high"
assert not df['player_name'].isnull().any(), "Some player names are null"
```

---

#### 4. Interface Verification

- [ ] All external interfaces verified against actual classes (not assumptions)
- [ ] Method signatures match actual source code
- [ ] Return types match actual implementations
- [ ] No broken imports or missing dependencies

**Verification:**
```markdown
## Interface Verification

Dependency: ConfigManager.get_adp_multiplier()

Assumed signature: get_adp_multiplier(adp: int) -> float
Actual signature (ConfigManager.py:234): get_adp_multiplier(adp: int) -> Tuple[float, int]

⚠️ MISMATCH FOUND - Code expects float, actual returns tuple
Fix: Updated code to handle tuple return (multiplier, rating)
```

---

#### 5. Runner Script Validation

- [ ] Entry point scripts tested with `--help`
- [ ] **Entry point scripts tested with E2E execution** (not just --help)
- [ ] Error messages are helpful (not stack traces for user errors)
- [ ] Script handles invalid inputs gracefully

---

#### 6. Documentation Validation

- [ ] code_changes.md accurately reflects all changes
- [ ] implementation_checklist.md all items verified
- [ ] No TODOs or FIXMEs in committed code
- [ ] Comments explain "why" not "what"

---

### Round 1 Execution

1. **Work through checklist systematically** (don't skip items)

2. **Document any issues found:**
   ```markdown
   ## QC Round 1 Issues

   ### Critical Issues
   1. Output file contains all zeros for projected_points column
      - Location: data/players_projected.csv
      - Expected: Real projection values (100-400 range)
      - Root cause: Mock data used instead of real API call
      - Impact: Feature doesn't work (primary use case fails)

   2. Interface mismatch - ConfigManager.get_adp_multiplier()
      - Expected return: float
      - Actual return: Tuple[float, int]
      - Impact: Code crashes when calling this method

   ### Minor Issues
   1. Missing docstring on calculate_adp_multiplier()
      - Location: league_helper/util/PlayerRatingManager.py:45
      - Impact: Low (documentation quality)
   ```

3. **Evaluate pass criteria:**
   - Critical issues: {count}
   - Requirements met: {percentage}%
   - **Pass if:** <3 critical issues AND 100% requirements met
   - **Fail if:** ≥3 critical issues OR <100% requirements met

4. **Decision:**
   - **If PASS:** Document results, proceed to Round 2
   - **If FAIL:** Follow QC Restart Protocol (see below)

**Example - Round 1 Results:**
```markdown
## QC Round 1 Results

**Issues Found:**
- Critical issues: 2
- Minor issues: 1

**Requirements Met:** 92% (23/25 requirements verified)

**Pass Criteria Evaluation:**
- Critical issues: 2 (<3) ✅
- Requirements met: 92% (>80%) ✅

**DECISION: PASS**

**Next Action:** Proceed to QC Round 2 (Deep Verification)

**Issues to address in Round 2:**
- Verify critical issues are actually fixed (not just "looks fixed")
- Verify no new issues introduced by fixes
```

---

## 🔄 Re-Reading Checkpoint #1

**STOP - Before proceeding to Round 2:**

1. **Re-read "Common Mistakes to Avoid" section below**
2. **Verify you didn't fall into any anti-patterns**
3. **Confirm Round 1 actually passed** (not just "close enough")
4. **Update README Agent Status:**
   ```markdown
   Guide Last Re-Read: {timestamp}
   Checkpoint: QC Round 1 complete, starting QC Round 2
   Round 1 Result: PASS (2 critical issues, 1 minor issue, 92% requirements met)
   ```

---

## QC Round 2: Deep Verification

**Purpose:** Deep dive into data quality, integration, and edge cases

**Pass Criteria:** ALL issues from Round 1 resolved + zero new critical issues

---

### Round 2 Checklist

Work through each section systematically. Check ALL boxes.

---

#### 1. Baseline Comparison (if similar feature exists)

- [ ] Identify similar feature in codebase (if any)
- [ ] Compare file structure (new feature follows same patterns?)
- [ ] Compare data format (consistent with existing features?)
- [ ] Compare integration patterns (uses same interfaces?)
- [ ] Document INTENTIONAL differences (and why they're needed)
- [ ] Verify new feature matches codebase conventions

**Example:**
```markdown
## Baseline Comparison: ADP Integration vs Player Rating Integration

Similar feature: Player Rating Integration (feature_03)

File structure: ✅ CONSISTENT
- Both use {feature}_Manager.py pattern
- Both store data in data/player_data/

Data format: ✅ CONSISTENT
- Both use CSV with standard columns
- Both use float for multiplier values

Integration: ⚠️ DIFFERENT (intentional)
- Player Rating uses ConfigManager.get_rating_multiplier()
- ADP uses NEW method ConfigManager.get_adp_multiplier()
- Reason: ADP requires different curve (exponential vs linear)
- Documented in: code_changes.md section 3

Conclusion: Differences are intentional and justified
```

---

#### 2. Output Data Validation (Values, not just structure)

- [ ] Open actual output files (CSV, JSON, etc.)
- [ ] Verify data values are in expected range
  - Example: Projected points between 0-500 (not -999 or 10000000)
- [ ] Verify no zeros where real data expected
- [ ] Verify no nulls where values required
- [ ] Verify no placeholder text ("TODO", "N/A", "test")
- [ ] Verify calculations are correct (spot-check a few rows manually)

**Real-World Example:**
```markdown
## Round 2 - Data Quality Check

File: data/player_data/qb_data_with_adp.csv

Verification:
✅ Row count: 128 (expected ~120-130 QBs)
✅ Column 'projected_points': Range 150.2-385.7 (reasonable for QBs)
✅ Column 'adp_multiplier': Range 0.87-1.48 (matches config ranges)
❌ Column 'adp_rank': 12 players have rank 0 (invalid)

Issue found: 12 players missing from ADP data source
Root cause: ADP data only covers top 300 players
Fix: Changed default from rank 0 to NaN for unranked players
Re-verification: ✅ All ranks now valid (1-287) or NaN
```

---

#### 3. Regression Testing

- [ ] Run ALL unit tests (not just new ones)
- [ ] Verify existing features still work
- [ ] Check that new feature didn't break existing functionality
- [ ] Review changed files (git diff) for unintended modifications

**Verification:**
```bash
# Run full test suite
python tests/run_all_tests.py

# Result: 2,247 tests passed, 0 failed ✅

# Verify no regression in existing modes
python run_league_helper.py --mode draft --dry-run  # ✅ Works
python run_league_helper.py --mode starter --dry-run  # ✅ Works
python run_league_helper.py --mode trade --dry-run  # ✅ Works
```

---

#### 4. Log Quality Verification

- [ ] Run feature and capture logs
- [ ] **No unexpected WARNING messages** (review each one)
- [ ] **No ERROR messages** (unless testing error paths)
- [ ] Log messages are helpful for debugging (not cryptic)
- [ ] No excessive logging (log spam)
- [ ] No sensitive data logged (passwords, API keys, PII)

**Example - Log Quality Issues:**
```markdown
## Log Quality Check

Total log messages: 1,247
- DEBUG: 1,189
- INFO: 52
- WARNING: 6
- ERROR: 0

WARNING messages review:
1. "Player 'J.Smith' missing ADP data, using default multiplier 1.0" (×5)
   - Status: Expected (not all players in ADP data)
   - Action: No change needed

2. "ADP data file timestamp is 7 days old"
   - Status: Expected (data refreshed weekly)
   - Action: No change needed

Conclusion: ✅ No unexpected WARNINGs, log quality is good
```

---

#### 5. Semantic Diff Check

- [ ] Review `git diff` for all changed files
- [ ] Categorize changes:
  - **Intentional:** Expected from feature implementation
  - **Accidental:** Formatting, whitespace, unrelated code
- [ ] Flag accidental changes for cleanup

**Example:**
```bash
# Review non-whitespace changes
git diff --ignore-all-space

# Find accidental formatting changes
git diff --word-diff
```

```markdown
## Semantic Diff Analysis

Files changed: 8

Intentional changes (feature-related):
- league_helper/util/PlayerManager.py: Added load_adp_data() method ✅
- league_helper/util/FantasyPlayer.py: Added adp_multiplier field ✅
- league_helper/util/ConfigManager.py: Added get_adp_multiplier() ✅

Accidental changes (not feature-related):
- league_helper/util/ConfigManager.py: Lines 45-67 re-indented
  - Not related to feature
  - Action: Revert whitespace changes
- utils/csv_utils.py: Added blank line at EOF
  - Not related to feature
  - Action: Revert formatting change
```

---

#### 6. Edge Case Validation

- [ ] Review spec.md "Edge Cases" section
- [ ] Verify each edge case handled in code
- [ ] Test edge cases manually (if not covered by unit tests):
  - Empty inputs
  - Maximum/minimum values
  - Null/undefined values
  - Concurrent access (if applicable)

---

#### 7. Error Handling Verification

- [ ] Try to trigger error conditions (invalid input, missing files, etc.)
- [ ] Verify error messages are helpful
- [ ] Verify errors don't crash the application
- [ ] Verify errors are logged appropriately
- [ ] Verify error recovery works (if applicable)

**Example:**
```markdown
## Error Handling Verification

Test 1: Missing ADP data file
- Command: rm data/adp_rankings.csv && python run_league_helper.py --mode draft
- Expected: Error logged, feature continues with default multipliers
- Actual: ✅ "ADP file not found, using default multipliers" logged, no crash

Test 2: Malformed ADP CSV
- Setup: Corrupted CSV (missing column headers)
- Expected: Error logged, feature continues with default multipliers
- Actual: ✅ "Invalid ADP file format" logged, no crash

Test 3: Invalid ADP value in CSV
- Setup: ADP rank = -5 (invalid)
- Expected: Warning logged, player gets default multiplier
- Actual: ✅ "Invalid ADP rank -5 for player X, using default" logged

Conclusion: ✅ All error scenarios handled gracefully
```

---

### Round 2 Execution

1. **Work through checklist systematically**

2. **Document findings:**
   ```markdown
   ## QC Round 2 Deep Verification

   ### Round 1 Issues Resolution
   ✅ Issue #1 (zeros in output): RESOLVED - Real API data now used
   ✅ Issue #2 (interface mismatch): RESOLVED - Code updated to handle tuple

   ### New Findings
   1. Data Quality: 12 players have invalid rank 0
      - Root cause: Not all players in ADP data source
      - Severity: Minor (affects 9% of players)
      - Fix: Changed default from 0 to NaN
      - Status: FIXED and re-verified

   2. Log Quality: No issues found ✅

   3. Semantic Diff: 2 accidental whitespace changes
      - Files: ConfigManager.py, csv_utils.py
      - Impact: None (cosmetic only)
      - Action: Reverted whitespace changes

   4. Baseline Comparison: Consistent with existing patterns ✅
   ```

3. **Evaluate pass criteria:**
   - Round 1 issues resolved: {yes/no}
   - New critical issues: {count}
   - **Pass if:** ALL Round 1 issues resolved AND zero new critical issues
   - **Fail if:** Any Round 1 issues unresolved OR new critical issues found

4. **Decision:**
   - **If PASS:** Proceed to Round 3
   - **If FAIL:** Follow QC Restart Protocol

**Example - Round 2 Results:**
```markdown
## QC Round 2 Results

**Round 1 Issues:**
- Issue #1 (zeros in output): ✅ RESOLVED
- Issue #2 (interface mismatch): ✅ RESOLVED

**New Findings:**
- Critical issues: 0
- Minor issues: 2 (invalid ranks, whitespace changes)
- Both minor issues: FIXED

**Pass Criteria Evaluation:**
- All Round 1 issues resolved: ✅
- New critical issues: 0 ✅

**DECISION: PASS**

**Next Action:** Proceed to QC Round 3 (Final Skeptical Review)
```

---

## 🔄 Re-Reading Checkpoint #2

**STOP - Before proceeding to Round 3:**

1. **Re-read "Critical Rules" section at top of this guide**
2. **Verify Round 1 AND Round 2 both passed**
3. **Confirm you actually verified data VALUES** (not just structure)
4. **Update README Agent Status:**
   ```markdown
   Guide Last Re-Read: {timestamp}
   Checkpoint: QC Round 2 complete, starting QC Round 3
   Round 2 Result: PASS (all Round 1 issues resolved, 0 new critical issues)
   ```

---

## QC Round 3: Final Skeptical Review

**Purpose:** Fresh-eyes review to catch anything missed in previous rounds

**Pass Criteria:** ZERO issues found (if issues found → QC Restart Protocol)

**Mindset:** Approach this as if you're reviewing someone else's code for the first time. Be skeptical.

---

### Round 3 Checklist

Work through each section with fresh perspective. Be ruthlessly skeptical.

---

#### 1. Re-read Spec with Fresh Eyes

- [ ] Open spec.md
- [ ] Read each requirement as if seeing it for first time
- [ ] For each requirement, verify implementation actually achieves it:
  - Not just "code exists for this"
  - But "code correctly implements this"
- [ ] Check for subtle misinterpretations

**Real-World Example:**
```markdown
## Spec Re-Reading Results

Spec requirement: "Add ADP multiplier to draft recommendations"

Round 1/2 verified:
✅ ADP multiplier calculation exists
✅ ADP multiplier stored in player object
✅ ADP multiplier displayed in output

Round 3 catches:
❌ ADP multiplier calculated but NOT applied to final score

Issue: Code calculates multiplier but forgets to multiply final_score by it
Location: FantasyPlayer.calculate_total_score() line 245
Fix: Added `final_score *= self.adp_multiplier`

This would have been caught by re-reading spec with fresh eyes.
```

---

#### 2. Re-check Algorithm Traceability Matrix

- [ ] Open Algorithm Traceability Matrix (from Stage 5a iteration 4)
- [ ] For each algorithm:
  - Find the code location listed in matrix
  - Read the actual code
  - Verify code behavior matches spec algorithm
- [ ] Check for algorithm drift (implementation slightly different from spec)

**Verification:**
```markdown
## Algorithm Traceability Re-Check

Matrix Entry #3:
Algorithm: "Calculate ADP multiplier using exponential curve"
Spec formula: multiplier = 1.0 + (500 - rank) / 500 * 0.5
Code location: PlayerManager._calculate_adp_multiplier() line 234

Code inspection:
```python
def _calculate_adp_multiplier(self, adp_rank):
    if adp_rank is None or adp_rank <= 0:
        return 1.0
    return 1.0 + (500 - adp_rank) / 500 * 0.5
```

Verification: ✅ Code matches spec exactly
```

---

#### 3. Re-check Integration Points

- [ ] Review Integration Gap Check (from Stage 5a iterations 7, 14, 23)
- [ ] Verify every new method has a caller
- [ ] Verify no orphan code (written but never used)
- [ ] Trace data flow end-to-end:
  - Input → Processing → Output
  - Verify each step actually happens

**Verification:**
```markdown
## Integration Points Re-Check

New method: PlayerManager.load_adp_data()
Caller: PlayerManager.load_players() line 180 ✅
Verified: Method is actually called ✅

Data flow trace:
1. load_adp_data() reads CSV ✅
2. _match_player_to_adp() assigns ranks ✅
3. _calculate_adp_multiplier() computes multiplier ✅
4. calculate_total_score() applies multiplier ✅ (FIXED in this round!)

No orphan code found ✅
```

---

#### 4. Re-run Smoke Test (Final Time)

- [ ] Re-run all 3 smoke test parts (Import, Entry Point, E2E)
- [ ] Even if they passed before, run again (fixes can introduce regressions)
- [ ] Verify output data VALUES still correct
- [ ] Compare output to expected output from spec test plan section

**Why re-run:** Fixes in Rounds 1 & 2 might have introduced new bugs

---

#### 5. Review Question Answers

- [ ] Open questions.md (if it exists)
- [ ] Re-read user's answers to your questions
- [ ] Verify implementation actually follows user's answers
- [ ] Check for misinterpretations of user's intent

---

#### 6. Final Skeptical Questions

Ask yourself these questions honestly:

- [ ] **"Does this feature actually work?"**
  - Not "tests pass" but "does it DO what user wants?"

- [ ] **"Would I ship this to production?"**
  - If hesitation: What's making you hesitant?

- [ ] **"Is the feature COMPLETE or just FUNCTIONAL?"**
  - FUNCTIONAL: It works in happy path
  - COMPLETE: It works in all cases, handles errors, has good UX

- [ ] **"What happens if..."**
  - ...file doesn't exist?
  - ...user provides invalid input?
  - ...data is missing/corrupted?
  - ...multiple features interact?

- [ ] **"Did I verify data VALUES or just structure?"**
  - Be honest: Did you actually open output files and check data?

- [ ] **"Is this actually better than before?"**
  - Does feature improve the system?
  - Or does it add complexity without clear benefit?

---

#### 7. Compare to Test Plan

- [ ] Open spec.md "Test Plan" or "Validation" section
- [ ] For each test scenario listed:
  - Run that scenario manually
  - Verify actual output matches expected output from spec
- [ ] If spec doesn't have test plan: Create one now (and update spec)

---

### Round 3 Execution

1. **Work through checklist with skeptical mindset**

2. **Document findings:**
   ```markdown
   ## QC Round 3 Final Review

   ### Issues Found
   1. ADP multiplier calculated but not applied to final score
      - Severity: CRITICAL (feature doesn't work)
      - Location: FantasyPlayer.calculate_total_score()
      - Fix: Added multiplication step
      - This triggers QC Restart Protocol

   {If ZERO issues: State "Zero issues found - feature is complete"}

   ### Skeptical Review Results
   - Feature actually works: {yes/no after fix}
   - Would ship to production: {yes/no}
   - Feature is COMPLETE (not just functional): {yes/no}
   - Data values verified (not just structure): yes
   - Better than before: yes

   ### Final Verification
   - Smoke tests re-run: {pass/fail}
   - Algorithm Traceability Matrix: verified
   - Integration points: verified
   - Test plan scenarios: all passed
   ```

3. **Evaluate pass criteria:**
   - Issues found: {count}
   - **Pass if:** ZERO issues found
   - **Fail if:** ANY issues found

4. **Decision:**
   - **If PASS (zero issues):** Proceed to Stage 5cc
   - **If FAIL (any issues):** Follow QC Restart Protocol

---

## 🚨 QC RESTART PROTOCOL

**This protocol is CRITICAL. If ANY issues found in QC rounds, you MUST follow this protocol.**

---

### When to Trigger QC Restart

**Trigger immediately if:**
- QC Round 1 finds ≥3 critical issues OR <100% requirements met
- QC Round 2 finds any Round 1 issues unresolved OR new critical issues
- QC Round 3 finds ANY issues (zero tolerance in Round 3)

**Do NOT trigger for:**
- Minor documentation issues (missing docstrings)
- Style issues (formatting, naming)
- Non-critical refactoring opportunities

**When in doubt:** If the issue affects CORRECTNESS or COMPLETENESS → Restart

---

### QC Restart Steps

**1. STOP all work immediately**
- Do not proceed to next QC round
- Do not "just fix this one thing"
- Do not rationalize "it's not that bad"

**2. Document the issues requiring restart:**
```markdown
## QC Restart Triggered

Trigger point: QC Round 3
Date: {YYYY-MM-DD}

Critical issues found:
1. ADP multiplier calculated but not applied to final score
   - Impact: Feature doesn't actually work (primary use case fails)
   - Root cause: Forgot to add multiplication step in calculate_total_score()
   - Location: FantasyPlayer.calculate_total_score() line 245

Restart required because: Round 3 found critical issue (zero tolerance)
```

**3. Fix ALL issues:**
- Don't just fix the ones you found
- Look for related issues (if one bug exists, are there others?)
- Fix root causes (not just symptoms)
- Update tests to catch these issues

**4. COMPLETELY RESTART Post-Implementation:**

**YOU MUST RE-RUN EVERYTHING:**

- [ ] **Re-run Smoke Testing** (Stage 5ca)
  - Part 1: Import Test
  - Part 2: Entry Point Test
  - Part 3: E2E Execution Test (verify DATA VALUES)

- [ ] **Re-run QC Round 1**
  - Don't assume it still passes
  - Fixes can introduce new issues
  - Fresh validation required

- [ ] **Re-run QC Round 2**
  - All checks from scratch
  - Baseline comparison again
  - Log quality verification again

- [ ] **Re-run QC Round 3**
  - Fresh-eyes skeptical review
  - Re-check Algorithm Traceability Matrix
  - Re-run final smoke test

**5. Document restart results:**
```markdown
## QC Restart Results

Issues fixed:
✅ Issue #1: Added `final_score *= self.adp_multiplier` at line 245

Post-restart validation:
✅ Smoke testing: ALL 3 PARTS PASSED
✅ QC Round 1: PASSED (<3 critical, 100% requirements)
✅ QC Round 2: PASSED (all resolved, no new issues)
✅ QC Round 3: PASSED (ZERO issues found)

Ready to proceed to Stage 5cc (Final Review).
```

---

### Why Complete Restart is Required

**Real-World Example:**

```
Initial QC Round 1: Found critical issue with output data (all zeros)
Developer fixed: Updated data calculation logic
Developer thought: "I'll just continue to QC Round 2"

PROBLEM: The fix introduced new bug (now some data is negative, which is impossible)

If developer had re-run Smoke Test Part 3 after fix:
→ Would have caught negative values immediately
→ Would have fixed before proceeding

Instead, negative values discovered in QC Round 3:
→ Had to restart entire Post-Implementation
→ Total time wasted: 4 hours
→ If had restarted properly after first fix: 30 minutes
```

**The rule:** Fixes can introduce new bugs. ALWAYS re-validate everything after fixes.

---

## Completion Criteria

**Stage 5cb is complete when ALL of the following are true:**

- [x] QC Round 1 passed (<3 critical issues, 100% requirements met)
- [x] QC Round 2 passed (all Round 1 issues resolved, zero new critical issues)
- [x] QC Round 3 passed (ZERO issues found in skeptical review)
- [x] All re-reading checkpoints completed
- [x] README Agent Status updated after each round
- [x] If QC restart was triggered, fully completed (smoke + all 3 rounds)

**If ALL criteria met:** Proceed to Stage 5cc (Final Review)

**If ANY criteria not met:** Do NOT proceed until all are met

---

## Common Mistakes to Avoid

### Anti-Pattern 1: Skipping QC Rounds

**❌ Mistake:**
"QC Round 1 passed, Round 2 looks similar, I'll skip to Round 3"

**Why wrong:** Each round has DIFFERENT focus:
- Round 1: Basic validation (structure, tests)
- Round 2: Deep verification (data quality, logs, baseline)
- Round 3: Fresh-eyes skeptical review

**Round 2 catches issues Round 1 misses** (data quality, log spam, semantic diff)

**✅ Correct:** Complete ALL 3 rounds, every time, no exceptions

---

### Anti-Pattern 2: "Fix and Continue" (Not Restarting)

**❌ Mistake:**
```
QC Round 1 finds critical issue
Developer fixes issue
Developer continues to QC Round 2 (doesn't restart)
```

**Why wrong:** Fix might introduce new bugs. Must re-validate everything.

**✅ Correct:** Follow QC Restart Protocol (re-run smoke testing, Round 1, 2, 3)

---

### Anti-Pattern 3: Superficial QC Round 3

**❌ Mistake:**
"Already did Round 1 and 2, Round 3 is just a formality, I'll skim it"

**Why wrong:** Round 3 catches subtle issues that previous rounds missed

**Real example:** Round 3 re-reading spec caught "ADP multiplier calculated but not applied"

**✅ Correct:** Round 3 = Fresh eyes, skeptical mindset, actually re-read everything

---

### Anti-Pattern 4: Batch Fixes Without Re-Validation

**❌ Mistake:**
```
QC finds 5 issues
Fix all 5 issues in one batch
Continue to next round (don't re-test)
```

**Why wrong:** Fixes can conflict with each other, introduce new bugs

**✅ Correct:** Follow QC Restart Protocol (re-validate after fixes)

---

## Prerequisites for Next Stage

**Before transitioning to Stage 5cc (Final Review), verify:**

**QC Rounds Complete:**
- [ ] QC Round 1: PASSED
- [ ] QC Round 2: PASSED
- [ ] QC Round 3: PASSED (zero issues)

**Documentation:**
- [ ] All issues documented (even if resolved)
- [ ] README Agent Status updated after each round
- [ ] If restart occurred, restart results documented

**Verification:**
- [ ] Feature is COMPLETE (not just functional)
- [ ] Would ship to production with confidence
- [ ] Data values verified (not just structure)
- [ ] All spec requirements met (100%)

**If ALL verified:** Ready for Stage 5cc (Final Review)

**If ANY unverified:** Complete Stage 5cb first

---

## Next Stage

**After completing QC Rounds:**

📖 **READ:** `STAGE_5cc_final_review_guide.md`
🎯 **GOAL:** Production readiness through PR review, lessons learned, final verification
⏱️ **ESTIMATE:** 45-60 minutes

**Stage 5cc will:**
- PR Review Checklist (11 categories)
- Lessons Learned Capture (update guides immediately)
- Final Verification
- Completion check before Stage 5d

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting Stage 5cc.

---

*End of STAGE_5cb_qc_rounds_guide.md*
