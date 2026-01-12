# PHASE 2: Issue Investigation (Per Issue, Repeated Rounds)

**Purpose:** Find root cause through structured investigation rounds

**When to Use:** After PHASE 1 complete, issues exist in ISSUES_CHECKLIST.md

**Previous Phase:** PHASE 1 (Discovery) - See `debugging/discovery.md`

**Next Phase:** PHASE 3 (Solution Design) - See `debugging/resolution.md`

---

## Overview

**This process uses repeated rounds:** Repeat Rounds 1-3 until root cause confirmed (max 5 rounds total)

**Investigation Round Structure:**
- **Round 1:** Code Tracing & Root Cause Analysis (identify 2-3 suspicious areas)
- **Round 2:** Hypothesis Formation (max 3 testable hypotheses, ranked by likelihood)
- **Round 3:** Diagnostic Testing (test hypotheses, confirm root cause with evidence)

**Time Limits:**
- Max 2 hours per round (alert user if exceeded)
- Max 5 total rounds before user escalation

**Goal:** Confirm root cause with concrete evidence

---

## Before Starting Investigation

### Step 1: Update ISSUES_CHECKLIST.md

1. **Change issue status to 🟡 INVESTIGATING:**
   ```markdown
   | 1 | player_scoring_returns_null | 🟡 INVESTIGATING | Round 1 | ❌ NO | Smoke Part 3 | Starting investigation |
   ```

2. **Update "Current Focus" section:**
   ```markdown
   **Active Issue:** #1 (player_scoring_returns_null)
   **Current Phase:** Phase 2 (Investigation - Round 1)
   **Next Action:** Code tracing to identify suspicious areas
   ```

---

### Step 2: Create issue_{number}_{name}.md file

**Filename format:** `issue_01_player_scoring_returns_null.md`

Use template below (populated during investigation).

---

### Step 3: Create/Update investigation_rounds.md

**If first issue being investigated:**
Create `debugging/investigation_rounds.md`:

```markdown
# Investigation Rounds Tracker

**Feature/Epic:** {name}
**Created:** {YYYY-MM-DD HH:MM}

---

## Active Investigations

| Issue # | Issue Name | Current Round | Status |
|---------|------------|---------------|--------|
| 1 | player_scoring_returns_null | Round 1 | Code tracing in progress |

---

## Completed Investigations

{Empty initially - will populate as investigations complete}

---

## Investigation Statistics

**Total Investigations:** 1 active, 0 complete
**Average Rounds per Issue:** N/A
**Total Investigation Time:** {tracking}
```

**If investigation_rounds.md already exists:**
Add new issue to "Active Investigations" table.

---

## Issue File Template: issue_{number}_{name}.md

```markdown
# Issue #1: Player scoring returns None

**Created:** {YYYY-MM-DD HH:MM}
**Status:** INVESTIGATING
**Discovered During:** Smoke Testing Part 3 (E2E Test)
**Current Phase:** Investigation Round 1

---

## Issue Description

**Symptom:**
Player scoring calculation returns None instead of expected float value

**Discovered During:**
S10.P1 Smoke Testing Part 3 - E2E test execution

**Reproduction:**
```python
player = PlayerManager.load_player("Patrick Mahomes")
score = player.calculate_score(week=1)
# Expected: 24.5 (float)
# Actual: None
```

**Impact:**
Blocks feature functionality - cannot calculate player scores

**Test Output:**
```
AssertionError: Expected float, got None
  File: simulation/accuracy/AccuracySimulationManager.py:89
```

---

## Investigation Rounds

{Rounds will be added below as investigation proceeds}

---

## Solution Implementation

{Will be filled after root cause confirmed - see PHASE 3}

---

## User Verification

{Will be filled after solution implemented - see PHASE 4}

---

## Related Issues

{Links to other issues if discovered during investigation}

---

## Code Locations

{Will be populated during investigation}
```

---

## Round 1: Code Tracing & Root Cause Analysis

**Goal:** Trace execution path, identify 2-3 suspicious code areas

**Time Limit:** 2 hours max (alert user if exceeded)

---

### Steps

#### 1. Trace execution path from symptom backwards

**Start where error occurs** (test failure point):
- Review stack trace
- Identify the file and line where error appears
- Note the exact error message

**Follow call stack backwards:**
- What function/method called this?
- What called that function?
- Continue until you reach the entry point

**Document each function/method:**
- Function name
- File location (file:line)
- What data is passed in
- What data is returned

**Note data transformations:**
- Where does data originate?
- How is it transformed at each step?
- Where might it become None/null/incorrect?

---

#### 2. Identify suspicious areas

**Narrow to 2-3 specific code locations:**
- File path and line numbers
- Function/method names
- Why is this location suspicious?

**For each suspicious area, note:**
- What does this code do?
- What data does it expect?
- What data is it actually receiving?
- Could this cause the symptom?

---

#### 3. Document in issue_{number}_{name}.md

**Add Round 1 section:**

```markdown
### Round 1: Code Tracing & Root Cause Analysis ({YYYY-MM-DD HH:MM})

**Execution Path Traced:**
```
AccuracySimulationManager.run()
  → PlayerManager.load_player("Patrick Mahomes")
    → Player.__init__()
      → Player._load_stats()
        → Player._calculate_base_score()  ← Returns None
```

**Findings:**
- Player._calculate_base_score() is returning None
- Method expects self.stats to be populated
- self.stats appears to be empty dict {}
- Suspect: Stats not loading from CSV during __init__

**Suspicious Code Locations:**
1. utils/FantasyPlayer.py:156 - _load_stats() method
   - Responsible for loading player stats from CSV
   - If CSV load fails, self.stats stays empty
2. utils/FantasyPlayer.py:89 - _calculate_base_score() method
   - Returns None if self.stats is empty
   - No error raised, just returns None silently
3. data/player_stats_2024.csv - Data source
   - CSV might be missing or have wrong format
   - Column names might not match expected

**Data Flow:**
- CSV file → pd.read_csv() → filter by player name → self.stats dict
- If any step fails, self.stats = {}
- Empty dict → calculate_base_score() returns None

**Preliminary Hypothesis:**
CSV not loading correctly, leaving self.stats empty

**Next:** Round 2 - Form specific testable hypotheses
```

---

#### 4. Update investigation_rounds.md

```markdown
## Active Investigations

| Issue # | Issue Name | Current Round | Status |
|---------|------------|---------------|--------|
| 1 | player_scoring_returns_null | Round 1 Complete | Identified 3 suspicious areas |
```

---

#### 5. Update ISSUES_CHECKLIST.md

```markdown
| 1 | player_scoring_returns_null | 🟡 INVESTIGATING | Round 1 → Round 2 | ❌ NO | Smoke Part 3 | 3 suspicious areas found |
```

---

## Round 2: Hypothesis Formation

**Goal:** Form 1-3 specific TESTABLE hypotheses

**Time Limit:** 2 hours max

**Max Hypotheses:** 3 (prevents shotgun debugging)

---

### Steps

#### 1. Review Round 1 findings

- Re-read execution path
- Re-read suspicious code locations
- Consider what could cause the symptom

---

#### 2. Form ranked hypotheses

**Each hypothesis must be:**
- **Specific:** Names exact cause (not vague guesses)
- **Testable:** Can be confirmed/rejected with diagnostic logging or tests
- **Explanatory:** Explains how it would cause the symptom

**Rank by likelihood:**
- Hypothesis 1: Most likely (60-80% confidence)
- Hypothesis 2: Possible (20-40% confidence)
- Hypothesis 3: Less likely but worth testing (5-20% confidence)

**For each hypothesis, specify:**
- **Root Cause:** Exact technical cause
- **Why it explains symptom:** How this would lead to observed behavior
- **How to test:** What diagnostic logging or tests will confirm/reject
- **Expected evidence:** What you'd see in logs if this is the cause

---

#### 3. Design diagnostic logging plan

**What data to inspect?**
- Variable values at suspicious code locations
- Data coming from external sources (CSV, API, config)
- Data transformations (before/after)

**Where to add log statements?**
- At each suspicious code location from Round 1
- At data transformation points
- At decision branches

**What test scenarios?**
- Reproduce original bug scenario
- Test with different inputs
- Test with edge cases

---

#### 4. Document in issue_{number}_{name}.md

**Add Round 2 section:**

```markdown
### Round 2: Hypothesis Formation ({YYYY-MM-DD HH:MM})

**Hypotheses (ranked by likelihood):**

**HYPOTHESIS 1: CSV Column Name Mismatch** (Confidence: 70%)
- **Root Cause:** _load_stats() expects column 'stat_value' but CSV has 'StatValue'
- **Why it explains symptom:** Column mismatch → pd filtering fails → stats dict stays empty → calculate returns None
- **How to test:** Add logging to show CSV columns and parsed dict contents
- **Expected evidence:** Log shows column names don't match expected, parsed dict is empty

**HYPOTHESIS 2: Player Name Mismatch** (Confidence: 20%)
- **Root Cause:** CSV uses "P. Mahomes" but we're looking up "Patrick Mahomes"
- **Why it explains symptom:** Name mismatch → no rows match filter → empty dict → None
- **How to test:** Add logging to show player name in CSV vs lookup name
- **Expected evidence:** Log shows name format mismatch between CSV and lookup

**HYPOTHESIS 3: File Path Wrong** (Confidence: 10%)
- **Root Cause:** _load_stats() looking in wrong directory for CSV
- **Why it explains symptom:** File not found → empty DataFrame → empty dict → None
- **How to test:** Add logging to show full file path being accessed
- **Expected evidence:** Log shows FileNotFoundError or wrong path

**Diagnostic Logging Plan:**
```python
# Add to utils/FantasyPlayer.py:156 (_load_stats method)
logger.info(f"Loading stats from: {csv_path}")
logger.info(f"CSV columns: {df.columns.tolist()}")
logger.info(f"CSV shape: {df.shape}")
logger.info(f"Looking for player: {self.name}")
logger.info(f"Players in CSV: {df['PlayerName'].unique()[:5]}")  # First 5
logger.info(f"Stats after filter: {player_stats.shape}")
logger.info(f"Parsed stats dict: {self.stats}")
```

**Test Scenarios:**
1. Load "Patrick Mahomes" (current failing case)
2. Load different player to see if pattern repeats
3. Check if CSV file exists and is readable
4. Inspect CSV manually to verify format

**Next:** Round 3 - Add logging and test hypotheses
```

---

#### 5. Update investigation_rounds.md and ISSUES_CHECKLIST.md

```markdown
## Active Investigations

| Issue # | Issue Name | Current Round | Status |
|---------|------------|---------------|--------|
| 1 | player_scoring_returns_null | Round 2 Complete | 3 hypotheses formed |
```

```markdown
| 1 | player_scoring_returns_null | 🟡 INVESTIGATING | Round 2 → Round 3 | ❌ NO | Smoke Part 3 | 3 hypotheses ready to test |
```

---

## Round 3: Diagnostic Testing

**Goal:** Test hypotheses, confirm root cause with evidence

**Time Limit:** 2 hours max

---

### Steps

#### 1. Add diagnostic logging

Implement the diagnostic logging plan from Round 2:
- Add log statements at suspicious code locations
- Log variable values, data inputs/outputs, decision paths
- Use INFO level (not DEBUG) so logs appear by default

---

#### 2. Run test scenarios

Execute the test scenarios from Round 2:
- Reproduce the original bug
- Test with variations
- Collect log output

---

#### 3. Collect and save log output

```bash
# Save to debugging/diagnostic_logs/
cp output.log debugging/diagnostic_logs/issue_01_round3.log

# Or capture programmatically
python run_simulation.py --mode accuracy 2>&1 | tee debugging/diagnostic_logs/issue_01_round3.log
```

---

#### 4. Analyze results

**For each hypothesis:**
- Review log output
- Does evidence CONFIRM or REJECT hypothesis?
- What was unexpected?
- Which hypothesis has strongest evidence?

**Root cause confirmation criteria:**
- Hypothesis explains ALL symptoms
- Evidence is concrete (not circumstantial)
- Fix for this cause would resolve issue

---

#### 5. Document in issue_{number}_{name}.md

**Add Round 3 section:**

```markdown
### Round 3: Diagnostic Testing ({YYYY-MM-DD HH:MM})

**Changes Made:**
- Added diagnostic logging to utils/FantasyPlayer.py:156-162

**Test Run Output:**
```
INFO: Loading stats from: data/player_stats_2024.csv
INFO: CSV columns: ['Week', 'PlayerName', 'StatValue', 'Position']
INFO: CSV shape: (544, 4)
INFO: Looking for player: Patrick Mahomes
INFO: Players in CSV: ['P.Mahomes', 'J.Allen', 'L.Jackson', 'J.Herbert', 'D.Prescott']
INFO: Stats after filter: (0, 4)
INFO: Parsed stats dict: {}
```

**Analysis:**

**Hypothesis 1 (Column Mismatch):** ❌ REJECTED
- Evidence: CSV columns match expected (['PlayerName', 'StatValue'] exist)
- No column mismatch

**Hypothesis 2 (Player Name Mismatch):** ✅ CONFIRMED
- Evidence: CSV has 'P.Mahomes' but we're looking up 'Patrick Mahomes'
- Filtered DataFrame has 0 rows (no match)
- This explains why stats dict is empty
- Empty dict → calculate_base_score() returns None
- **This is the root cause**

**Hypothesis 3 (File Path):** ❌ REJECTED
- Evidence: CSV loads successfully (has 544 rows)
- File path is correct

---

**ROOT CAUSE CONFIRMED:**

**Problem:** Player name format mismatch
- Code uses: "Patrick Mahomes"
- CSV has: "P.Mahomes"
- Lookup fails → empty stats dict → calculate_base_score() returns None

**Location:** utils/FantasyPlayer.py:156 (_load_stats method)

**Evidence:** Diagnostic logs (saved to debugging/diagnostic_logs/issue_01_round3.log)

**Status:** Ready for Phase 3 (Solution Design & Implementation)

**Investigation Summary:**
- Rounds: 3
- Time: ~90 minutes
- Root cause confirmed with concrete evidence
```

---

#### 6. Update ISSUES_CHECKLIST.md

```markdown
| 1 | player_scoring_returns_null | 🟡 INVESTIGATING | Phase 2 → Phase 3 | ❌ NO | Smoke Part 3 | Root cause confirmed |
```

---

## Round Limits & Escalation

### If root cause NOT found after Round 3

**Assess:**
- Are there new hypotheses to test? → Back to Round 2
- Do you need to expand the search area? → Back to Round 1
- **Max 5 total rounds** before user escalation

---

### After 5 rounds without confirming root cause

**Escalate to user:**

```markdown
I've completed 5 investigation rounds for Issue #{number} without confirming the root cause.

## Investigation Summary

**Issue:** {name}
**Rounds:** 5
**Time:** {total time}

**What I've Tried:**

**Round 1:** Code tracing
- Identified suspicious areas: {list}

**Round 2:** Hypothesis formation
- Hypothesis 1: {summary} - Result: {rejected/inconclusive}
- Hypothesis 2: {summary} - Result: {rejected/inconclusive}

**Round 3:** Diagnostic testing
- {summary of tests}
- Evidence: {what was found}

**Round 4:** {approach}
- Result: {what happened}

**Round 5:** {approach}
- Result: {what happened}

---

## Current Understanding

**Known facts:**
- {what we know for sure}

**Still unclear:**
- {what we don't understand}

**Suspicious areas:**
- {code locations that might be involved}

**Hypotheses not yet tested:**
- {if any}

---

## Recommended Next Steps

1. **Continue investigating (Round 6+):** {new approach to try}
2. **Get user input:** {specific questions for user}
3. **Alternative approach:** {different debugging strategy}

What would you like me to do?
```

**Wait for user guidance before proceeding.**

---

## Common Investigation Patterns

### Pattern 1: Data Format Mismatch

**Symptoms:**
- Data loads but values are wrong
- Empty results when data exists
- Type mismatches

**Investigation approach:**
- Log data formats at boundaries (CSV, API, config)
- Compare expected vs actual formats
- Check column names, data types, encoding

---

### Pattern 2: Null/None Propagation

**Symptoms:**
- Null/None appearing where not expected
- Silent failures (no errors raised)

**Investigation approach:**
- Trace data flow backwards from None value
- Find where None originates
- Check why validation didn't catch it

---

### Pattern 3: Integration Mismatch

**Symptoms:**
- Works in isolation, fails when integrated
- Data lost between components

**Investigation approach:**
- Log data at integration boundaries
- Verify interfaces match (caller sends what callee expects)
- Check for version mismatches in shared data structures

---

## Next Steps

**After confirming root cause (Round 3 complete):**

✅ Root cause identified with concrete evidence
✅ Diagnostic logs saved
✅ Issue file updated with investigation results
✅ ISSUES_CHECKLIST.md updated

**Next:** Read `debugging/resolution.md` for PHASE 3 (Solution Design & Implementation)

---

**END OF PHASE 2 GUIDE**
