# Stage 5a.5: Hands-On Data Inspection Guide

---

## Quick Start

**What is this guide?**
Hands-On Data Inspection is a critical verification step where you manually inspect actual data files to verify assumptions about data structure, values, and location BEFORE implementing code to prevent catastrophic bugs.

**When do you use this guide?**
- After Stage 5a Round 3 (Implementation planning complete)
- Before Stage 5b (Implementation execution)
- When implementation will load or process data files

**Key Outputs:**
- ✅ All data dependencies identified from implementation_plan.md
- ✅ Data files opened and values inspected in Python REPL
- ✅ Data model assumptions verified against actual data
- ✅ Wrong assumptions corrected in spec.md and implementation_plan.md
- ✅ Ready for Stage 5b (Implementation Execution)

**Time Estimate:**
15-30 minutes (can prevent hours of debugging)

**Exit Condition:**
Hands-On Data Inspection is complete when you have opened actual data files, printed real values, verified assumptions match reality, and corrected any wrong assumptions in spec and implementation plan

---

**Premise:** **NEVER TRUST ASSUMPTIONS - VERIFY WITH ACTUAL DATA**

---

## Why This Stage Exists

**Historical Evidence:** Feature 02 (Accuracy Sim) had a catastrophic bug that survived implementation and testing:

**The Assumption (WRONG):**
```
"Week_N folder contains week N actual points"
```

**The Reality:**
```python
# week_01/qb_data.json
week_01[0]['actual_points'][0]  # 0.0 (week 1 not complete yet)

# week_02/qb_data.json
week_02[0]['actual_points'][0]  # 33.6 (week 1 complete)
```

**The Consequences:**
- Implemented code that loaded week_N for both projected and actual
- All actual_points were 0.0
- MAE calculations were meaningless
- Smoke tests showed "(0 have non-zero actual points)" - marked PASS anyway
- Bug survived 7 stages, caught by user in final review

**The Prevention:**
Opening a Python REPL and running 3 commands would have caught this bug in 30 seconds:
```python
import json
week_01 = json.load(open('simulation/sim_data/2021/weeks/week_01/qb_data.json'))
print(week_01[0]['actual_points'][0])  # 0.0 → Assumption is WRONG
```

**This stage is MANDATORY** to prevent implementing code based on wrong assumptions.

---

## Prerequisites

Before starting Stage 5a.5:

- [x] Stage 5a Round 3 completed (implementation_plan.md and questions.md exist)
- [x] Spec.md identifies data files that will be loaded
- [x] Data files exist in the codebase
- [x] Python environment is available

---

## Core Principle

**YOU CANNOT TRUST ASSUMPTIONS ABOUT DATA**

- Code comments might be outdated
- Variable names might be misleading
- Your mental model might be wrong
- Spec.md might have misinterpreted the data model

**THE ONLY SOURCE OF TRUTH IS THE ACTUAL DATA**

Open the files. Print the values. Verify your assumptions.

---

## The Inspection Process

### Step 1: Identify Data Dependencies

**Action:** List ALL data files that your implementation will read

**From your implementation_plan.md, identify:**
- Which data files will be loaded?
- Which fields/keys will be accessed?
- Which array indices will be used?
- What value ranges are expected?

**Document:**
```markdown
## Data Dependencies Identified

**File 1:** simulation/sim_data/2021/weeks/week_01/qb_data.json
- Fields accessed: projected_points, actual_points
- Array indices: [week_num - 1]
- Expected: projected > 0, actual might be 0 or > 0

**File 2:** simulation/sim_data/2021/weeks/week_02/qb_data.json
- Fields accessed: actual_points
- Array indices: [week_num - 1]
- Expected: actual > 0

[Repeat for each file]
```

---

### Step 2: Open Python REPL

**Action:** Open an interactive Python session in the project directory

**Method:**
```bash
cd /path/to/FantasyFootballHelperScripts
python
```

**Why REPL instead of script?**
- Interactive exploration (try commands, see results immediately)
- No file creation overhead
- Can adjust queries based on findings
- Forces you to think about each command

---

### Step 3: Load REAL Data Files

**Action:** Load the ACTUAL data files your code will use (NOT test fixtures)

**CRITICAL RULES:**
- Use PRODUCTION data paths (simulation/sim_data/2021/...)
- Do NOT use test fixture paths (tests/fixtures/...)
- Load MULTIPLE files (to understand patterns)
- Use paths from spec.md (verify spec assumptions)

**Example:**
```python
import json
from pathlib import Path

# Load multiple weeks to understand pattern
week_01_path = Path('simulation/sim_data/2021/weeks/week_01/qb_data.json')
week_02_path = Path('simulation/sim_data/2021/weeks/week_02/qb_data.json')
week_03_path = Path('simulation/sim_data/2021/weeks/week_03/qb_data.json')

with open(week_01_path) as f:
    week_01 = json.load(f)

with open(week_02_path) as f:
    week_02 = json.load(f)

with open(week_03_path) as f:
    week_03 = json.load(f)
```

**Common Mistake:**
```python
# WRONG - only loads one file
week_01 = json.load(open('week_01/qb_data.json'))
# Can't see patterns with one data point
```

**Right:**
```python
# RIGHT - loads multiple files
week_01 = json.load(open('simulation/sim_data/2021/weeks/week_01/qb_data.json'))
week_02 = json.load(open('simulation/sim_data/2021/weeks/week_02/qb_data.json'))
week_03 = json.load(open('simulation/sim_data/2021/weeks/week_03/qb_data.json'))
# Can compare values across files to understand pattern
```

---

### Step 4: Print ACTUAL Values (Not Just "Exists")

**Action:** Print the REAL values from the data (not just check if keys exist)

**CRITICAL RULES:**
- Print ACTUAL numeric values (not True/False for "exists")
- Print values from MULTIPLE array indices
- Print values from MULTIPLE files
- Document EXACT values (not "looks good")

**Example - WRONG:**
```python
# This tells you NOTHING about the actual values
print('actual_points' in week_01[0])  # True
# You now know the key exists, but not what value it contains
```

**Example - RIGHT:**
```python
# This shows you the ACTUAL data
print(f"Week 1 actuals in week_01 folder: {week_01[0]['actual_points'][0]}")  # 0.0
print(f"Week 1 actuals in week_02 folder: {week_02[0]['actual_points'][0]}")  # 33.6
print(f"Week 2 actuals in week_02 folder: {week_02[0]['actual_points'][1]}")  # 0.0
print(f"Week 2 actuals in week_03 folder: {week_03[0]['actual_points'][1]}")  # 22.4

# Now you can see the PATTERN: week_N has 0.0 for week N, week_N+1 has real values
```

---

### Step 5: Test Assumptions Systematically

**Action:** For EACH assumption in your spec or TODO, verify with actual data

**Method:**

For each assumption, create a verification test:

**Assumption Format:**
```markdown
**Assumption:** [What you think is true]
**Verification Command:** [Python code to test it]
**Result:** [What the data actually shows]
**Conclusion:** [Valid or Invalid]
```

**Example:**

**Assumption 1:** "Week_N folder contains week N actual points"
```python
# Verification Command:
week_01 = json.load(open('simulation/sim_data/2021/weeks/week_01/qb_data.json'))
actual_week_1_in_week_01 = week_01[0]['actual_points'][0]
print(f"Week 1 actual in week_01: {actual_week_1_in_week_01}")

# Result:
# Week 1 actual in week_01: 0.0

# Conclusion:
# ❌ INVALID - Week_N folder has 0.0 for week N actuals
```

**Assumption 2:** "Week_N+1 folder contains week N actual points"
```python
# Verification Command:
week_02 = json.load(open('simulation/sim_data/2021/weeks/week_02/qb_data.json'))
actual_week_1_in_week_02 = week_02[0]['actual_points'][0]
print(f"Week 1 actual in week_02: {actual_week_1_in_week_02}")

# Result:
# Week 1 actual in week_02: 33.6

# Conclusion:
# ✅ VALID - Week_N+1 folder has real week N actuals
```

**Assumption 3:** "This pattern applies to all weeks (not just week 17)"
```python
# Verification Command:
week_03 = json.load(open('simulation/sim_data/2021/weeks/week_03/qb_data.json'))
actual_week_2_in_week_03 = week_03[0]['actual_points'][1]
print(f"Week 2 actual in week_03: {actual_week_2_in_week_03}")

# Result:
# Week 2 actual in week_03: 22.4

# Conclusion:
# ✅ VALID - Pattern applies to ALL weeks, not special case
```

---

### Step 6: Understand Value Ranges and Statistics

**Action:** Verify that data values are in realistic ranges

**Why This Matters:**
- Prevents implementing code that produces all zeros (Feature 02 bug)
- Catches edge cases (negative values, nulls, extremely large values)
- Validates that data makes sense for domain (NFL scoring)

**Method:**
```python
# Get statistical distribution of values
import statistics

# Collect all actual points for week 1 from week_02 folder
week_1_actuals = [player['actual_points'][0] for player in week_02
                  if len(player['actual_points']) > 0]

print(f"Count: {len(week_1_actuals)}")
print(f"Min: {min(week_1_actuals)}")
print(f"Max: {max(week_1_actuals)}")
print(f"Mean: {statistics.mean(week_1_actuals)}")
print(f"Median: {statistics.median(week_1_actuals)}")
print(f"Std Dev: {statistics.stdev(week_1_actuals)}")

# Count zeros
zero_count = sum(1 for val in week_1_actuals if val == 0.0)
zero_percentage = (zero_count / len(week_1_actuals)) * 100
print(f"Zero percentage: {zero_percentage:.1f}%")

# Sample of non-zero values
non_zero = [val for val in week_1_actuals if val > 0][:10]
print(f"Sample non-zero values: {non_zero}")
```

**Document Findings:**
```markdown
## Value Range Analysis

**Week 1 Actuals (from week_02 folder):**
- Count: 250 players
- Min: 0.0, Max: 48.2
- Mean: 8.5, Median: 6.2
- Std Dev: 7.3
- Zero percentage: 35% (reasonable - not all players played)
- Sample values: [33.6, 22.4, 18.9, 15.2, 12.7, ...]

**Conclusion:** Values are realistic for NFL scoring
```

**Red Flags That Should FAIL This Stage:**
- Zero percentage > 90% (almost all zeros)
- Std Dev = 0 (all same value)
- Min = Max (no variance)
- All values are 0.0
- Values outside realistic range (e.g., 10,000 points for QB)

---

### Step 7: Verify Cross-File Consistency

**Action:** Verify that data across multiple files follows expected patterns

**Why This Matters:**
- Catches schema changes mid-season
- Validates that patterns are consistent
- Ensures implementation won't break on certain files

**Method:**
```python
# Check schema consistency across weeks
def check_schema(week_data, week_num):
    """Verify data structure is consistent."""
    sample = week_data[0]

    required_keys = ['id', 'name', 'position', 'team',
                     'projected_points', 'actual_points']

    for key in required_keys:
        if key not in sample:
            print(f"❌ Week {week_num}: Missing key '{key}'")
            return False

    # Verify array lengths
    proj_len = len(sample['projected_points'])
    act_len = len(sample['actual_points'])

    if proj_len != 17:
        print(f"⚠️  Week {week_num}: projected_points has {proj_len} items (expected 17)")

    if act_len != 17:
        print(f"⚠️  Week {week_num}: actual_points has {act_len} items (expected 17)")

    print(f"✅ Week {week_num}: Schema valid")
    return True

# Test multiple weeks
check_schema(week_01, 1)
check_schema(week_02, 2)
check_schema(week_03, 3)
```

**Document Findings:**
```markdown
## Schema Consistency Check

Verified weeks 1-3:
- ✅ All have required keys
- ✅ All have 17-item arrays
- ✅ Data types consistent

Pattern verified across all sampled files.
```

---

### Step 8: Document ALL Findings

**Action:** Create a permanent record of your hands-on inspection

**Required Documentation:**

```markdown
## Hands-On Data Inspection Results

**Date:** [Current date]
**Feature:** [Feature name]
**Data Inspected:** [List of files]

### Commands Run

\`\`\`python
# Load data files
import json
week_01 = json.load(open('simulation/sim_data/2021/weeks/week_01/qb_data.json'))
week_02 = json.load(open('simulation/sim_data/2021/weeks/week_02/qb_data.json'))

# Print actual values
print(f"Week 1 actuals in week_01: {week_01[0]['actual_points'][0]}")  # 0.0
print(f"Week 1 actuals in week_02: {week_02[0]['actual_points'][0]}")  # 33.6
\`\`\`

### Assumptions Tested

| Assumption | Verification | Result | Valid? |
|------------|--------------|--------|--------|
| Week_N has week N actuals | Printed week_01[0]['actual_points'][0] | 0.0 | ❌ FALSE |
| Week_N+1 has week N actuals | Printed week_02[0]['actual_points'][0] | 33.6 | ✅ TRUE |
| Pattern applies to all weeks | Tested weeks 1, 2, 3 | Consistent | ✅ TRUE |

### Value Range Analysis

**Week 1 Actuals (from week_02):**
- Count: 250, Min: 0.0, Max: 48.2
- Mean: 8.5, Median: 6.2, Std Dev: 7.3
- Zero percentage: 35% (realistic)

### Key Findings

1. **Week_N folder has 0.0 for week N actuals** (verified empirically)
2. **Week_N+1 folder has real week N actuals** (verified empirically)
3. **Pattern is consistent across all weeks** (tested weeks 1-3)
4. **Values are in realistic range for NFL** (verified statistics)

### Implementation Impact

**Spec.md claimed:** "No special handling needed"
**Reality:** MUST load week_N+1 folder for actual points

**Code changes required:**
- Load TWO folders (week_N and week_N+1)
- Create TWO PlayerManager instances
- Get projections from week_N, actuals from week_N+1

---

### Discrepancies with Spec

**Discrepancy 1:** Spec says week_N has week N actuals
- **Spec claim:** "JSON arrays already handle week 17/18"
- **Data shows:** Week_N has 0.0 for week N actuals
- **Impact:** Spec conclusion "no code changes needed" is WRONG

**Recommendation:** STOP - Report to user, update spec.md
```

---

### Step 9: Compare Findings with Spec and Implementation Plan

**Action:** Check if your hands-on findings contradict spec.md or implementation_plan.md

**For EACH finding, ask:**
- Does this contradict anything in spec.md?
- Does this contradict any implementation plan task?
- Does this reveal a wrong assumption?
- Does this require code changes not in implementation plan?

**If ANY contradictions found:**

**🛑 STOP IMMEDIATELY**

Do NOT proceed to Stage 5b (Implementation). Your implementation plan is based on wrong assumptions.

**Report to User:**

Use this template:

```markdown
## ⚠️ DATA INSPECTION FAILED - User Input Required

I completed Stage 5a.5 (Hands-On Data Inspection) and found discrepancies
between the actual data and our spec.md/implementation_plan.md.

### Findings Summary

**Assumption in spec.md:**
> [Quote from spec]

**What actual data shows:**
> [What you found with hands-on inspection]

**Evidence:**
\`\`\`python
# Commands run:
[Python commands you ran]

# Output:
[Actual output showing the contradiction]
\`\`\`

**Impact:**
- [What this means for implementation]
- [Which implementation plan tasks are affected]
- [What needs to change]

### Recommended Actions

**Option A (Recommended):** Fix spec and implementation plan, restart Stage 5a
1. Update spec.md based on actual data findings
2. Restart Stage 5a Round 1 to regenerate implementation_plan.md
3. Re-run Stage 5a.5 to verify new assumptions
4. Proceed to Stage 5b only after zero discrepancies

**Option B:** Fix spec and implementation plan, continue to Stage 5b
1. Update spec.md based on findings
2. Manually update implementation_plan.md tasks
3. Continue to Stage 5b
4. Risk: Implementation plan may still have subtle errors

**Option C:** Discuss findings first
1. Review each discrepancy together
2. Clarify data model
3. Then update spec/implementation plan
4. Re-run Stage 5a.5 to verify

**My Recommendation:** Option A

**Reason:** [Specific reason based on severity]

Please advise how you'd like to proceed.
```

**Wait for User Decision** - Do NOT make this choice autonomously.

---

### Step 10: If Zero Discrepancies, Create Evidence Summary

**Action:** If hands-on inspection validates spec/TODO, create summary for future reference

**Document:**
```markdown
## ✅ Data Inspection Passed

All assumptions validated with actual data.

### Verified Assumptions

| Assumption | Evidence | Status |
|------------|----------|--------|
| [Assumption 1] | [Command + output] | ✅ Valid |
| [Assumption 2] | [Command + output] | ✅ Valid |
| [Assumption 3] | [Command + output] | ✅ Valid |

### Data Characteristics

- File count: [X files inspected]
- Value range: [Min to Max]
- Zero percentage: [X%]
- Schema: [Consistent/Inconsistent]

### Implementation Confidence

**Spec.md claims:** [Summary of spec]
**Data confirms:** [Summary of findings]
**Conclusion:** Safe to proceed to Stage 5b

All TODO items are based on validated assumptions.
```

---

## Pass Criteria

Stage 5a.5 is complete when:

**Scenario 1: Zero Discrepancies**
- [ ] Loaded REAL data files (not test fixtures)
- [ ] Printed ACTUAL values (not just "exists" checks)
- [ ] Tested ALL assumptions from spec.md
- [ ] Verified value ranges are realistic
- [ ] Checked schema consistency across files
- [ ] Documented findings with actual commands and output
- [ ] Compared findings with spec.md and implementation_plan.md
- [ ] Zero contradictions found
- [ ] Created evidence summary
- [ ] **Proceed to Stage 5b**

**Scenario 2: Discrepancies Found**
- [ ] Documented ALL discrepancies with evidence
- [ ] Reported to user with 3 options
- [ ] Waited for user decision
- [ ] Executed user's choice (fix spec, restart 5a, discuss, etc.)
- [ ] Re-ran Stage 5a.5 after fixes
- [ ] Now zero discrepancies
- [ ] **Proceed per user decision**

---

## Common Pitfalls

### ❌ Pitfall 1: Only Checking "Exists"

**Wrong:**
```python
print('actual_points' in week_01[0])  # True
# Conclusion: "Data exists, looks good"
```

**Right:**
```python
print(f"Actual value: {week_01[0]['actual_points'][0]}")  # 0.0
# Conclusion: "Key exists but value is 0.0 - investigate why"
```

### ❌ Pitfall 2: Only Loading One File

**Wrong:**
```python
week_01 = json.load(open('week_01/qb_data.json'))
print(week_01[0]['actual_points'][0])  # 0.0
# Conclusion: "Week 1 actuals are 0.0" (but is this the pattern or special case?)
```

**Right:**
```python
week_01 = json.load(open('week_01/qb_data.json'))
week_02 = json.load(open('week_02/qb_data.json'))
week_03 = json.load(open('week_03/qb_data.json'))
print(f"Week 1 in week_01: {week_01[0]['actual_points'][0]}")  # 0.0
print(f"Week 1 in week_02: {week_02[0]['actual_points'][0]}")  # 33.6
print(f"Week 2 in week_03: {week_03[0]['actual_points'][1]}")  # 22.4
# Conclusion: "Pattern is week_N has 0.0, week_N+1 has real values"
```

### ❌ Pitfall 3: Using Test Fixtures Instead of Real Data

**Wrong:**
```python
# Test fixtures might have simplified/fake data
data = json.load(open('tests/fixtures/sample_week.json'))
```

**Right:**
```python
# Real production data shows actual behavior
data = json.load(open('simulation/sim_data/2021/weeks/week_01/qb_data.json'))
```

### ❌ Pitfall 4: Trusting Variable Names

**Wrong:**
```python
# Variable name suggests it has week 1 actuals
week_1_actual_points = week_01[0]['actual_points'][0]
print(week_1_actual_points)  # 0.0
# Conclusion: "Week 1 actuals are 0.0, maybe no games played?"
```

**Right:**
```python
# Don't trust names - verify the actual values
week_1_actual_in_week_01 = week_01[0]['actual_points'][0]  # 0.0
week_1_actual_in_week_02 = week_02[0]['actual_points'][0]  # 33.6
# Conclusion: "week_01 folder name is misleading - has 0.0, not real actuals"
```

### ❌ Pitfall 5: Silently Fixing Discrepancies

**Wrong:**
```python
# Find discrepancy
print(week_01[0]['actual_points'][0])  # 0.0 (expected > 0)
# Conclusion: "Spec is wrong, I'll fix it and continue"
# [Updates spec.md and implementation_plan.md silently]
# [Proceeds to Stage 5b]
```

**Right:**
```python
# Find discrepancy
print(week_01[0]['actual_points'][0])  # 0.0 (expected > 0)
# Conclusion: "Spec is wrong - STOP and report to user"
# [Documents discrepancy with evidence]
# [Reports to user with 3 options]
# [Waits for user decision]
```

---

## Critical Questions Checklist

Before marking Stage 5a.5 complete, answer ALL questions:

```markdown
## Stage 5a.5 Critical Questions

### Data Loading
- [ ] Did I load REAL data files (not test fixtures)?
- [ ] Did I load MULTIPLE files (to understand patterns)?
- [ ] Did I use paths from spec.md (verify assumptions)?

### Value Inspection
- [ ] Did I print ACTUAL values (not just check "exists")?
- [ ] Did I test values from MULTIPLE array indices?
- [ ] Did I verify value ranges are realistic?
- [ ] Did I check for zeros, nulls, outliers?

### Statistical Validation
- [ ] Did I calculate min, max, mean, median, std dev?
- [ ] Did I check zero percentage?
- [ ] Did I verify variance > 0?
- [ ] Would these values make sense in production?

### Pattern Recognition
- [ ] Did I test with multiple examples (not just one)?
- [ ] Did I distinguish pattern from special case?
- [ ] Did I verify consistency across files?

### Assumption Testing
- [ ] Did I test EVERY assumption from spec.md?
- [ ] Did I document evidence for each test?
- [ ] Did I identify any contradictions?

### Comparison with Spec/Implementation Plan
- [ ] Did I compare findings with spec.md claims?
- [ ] Did I compare with implementation_plan.md tasks?
- [ ] Did I report ALL discrepancies to user?
- [ ] If discrepancies found, did I STOP and wait for user?

### Documentation
- [ ] Did I document actual commands run?
- [ ] Did I document actual output received?
- [ ] Did I create evidence table?
- [ ] Can someone reproduce my findings?
```

All questions must be YES to pass.

---

## Time Estimate

- **Normal case (validates assumptions):** 20-40 minutes
- **Discrepancies found:** 1-2 hours (includes user discussion)

**Note:** This time investment prevents days of implementing wrong solution.

---

## Output Artifacts

After Stage 5a.5:

1. **data_inspection_findings.md** (NEW FILE):
   - Commands run in Python REPL
   - Actual output received
   - Assumptions tested with evidence
   - Value range analysis
   - Schema consistency check
   - Comparison with spec.md/implementation_plan.md
   - Discrepancies (if any)

2. **Updated spec.md** (if discrepancies found and user approved)

3. **Updated implementation_plan.md** (if major discrepancies found)

---

## Example: Feature 02 Should Have Done This

**What Actually Happened (WRONG):**

Stage 5a → Stage 5b (skipped data inspection)
- Assumed week_N folder has week N actuals
- Implemented based on assumption
- All actuals were 0.0
- Bug survived to user final review

**What Should Have Happened (RIGHT):**

Stage 5a → **Stage 5a.5 (Data Inspection)** → Stage 5b

**Stage 5a.5 Process:**
```python
# Step 1: Load actual data
import json
week_01 = json.load(open('simulation/sim_data/2021/weeks/week_01/qb_data.json'))
week_02 = json.load(open('simulation/sim_data/2021/weeks/week_02/qb_data.json'))

# Step 2: Test assumption
print(f"Week 1 actuals in week_01: {week_01[0]['actual_points'][0]}")  # 0.0
print(f"Week 1 actuals in week_02: {week_02[0]['actual_points'][0]}")  # 33.6

# Step 3: Realize assumption is WRONG
# week_01 folder does NOT have week 1 actuals (has 0.0)
# week_02 folder DOES have week 1 actuals (has 33.6)

# Step 4: Report to user
# "Spec.md says 'no code changes needed' but data shows we need week_N+1"

# Step 5: User chooses Option A (fix spec, restart Stage 5a)

# Step 6: Update spec.md with correct data model

# Step 7: Restart Stage 5a with correct understanding

# Step 8: Re-run Stage 5a.5 to verify fixes

# Step 9: Proceed to Stage 5b with validated assumptions
```

**Result:** Bug caught before writing any code.

---

## Integration with Other Stages

**Stage 5a Round 3 (Implementation Planning):**
- Creates implementation_plan.md based on spec.md assumptions
- Does NOT verify assumptions with actual data

**Stage 5a.5 (Hands-On Data Inspection) - THIS STAGE:**
- Verifies spec.md assumptions with REAL data
- Catches wrong assumptions BEFORE implementing
- Reports discrepancies to user
- May trigger restart of Stage 5a if spec is wrong

**Stage 5b (Implementation Execution):**
- Implements based on implementation_plan.md
- Assumes implementation plan is correct (validated by 5a.5)
- If 5a.5 skipped, may implement wrong solution

---

## Why 30 Seconds of Data Inspection Saves Days

**Time to catch bug in Stage 5a.5:** 30 seconds
```python
import json
week_01 = json.load(open('simulation/sim_data/2021/weeks/week_01/qb_data.json'))
print(week_01[0]['actual_points'][0])  # 0.0 → "Wait, this should be > 0!"
```

**Time to fix bug caught in Stage 5a.5:** 30 minutes
- Update spec.md with correct data model
- Restart Stage 5a to regenerate implementation_plan.md
- Proceed to 5b with correct plan

**Time to fix bug caught in Stage 6 (Epic QC):** 4+ hours
- Debug why MAE is wrong
- Trace through implementation
- Realize data loading is wrong
- Fix code
- Re-run all tests
- Re-run smoke tests
- Re-run QC rounds

**Time to fix bug caught by user:** 8+ hours + trust lost
- User reports issue
- Investigation to find root cause
- Realize spec was wrong from start
- Fix spec + code + tests
- Re-validate entire feature
- User re-tests
- Damage to user trust in process

**MORAL: Spend 30 seconds in Stage 5a.5 to save hours (or days) later.**

---

## Remember

**Core Principle:** NEVER TRUST ASSUMPTIONS - VERIFY WITH ACTUAL DATA

- Your mental model might be wrong
- Spec.md might be wrong
- Code comments might be wrong
- Variable names might be misleading

**THE ONLY SOURCE OF TRUTH IS THE ACTUAL DATA**

Open the files. Print the values. Verify every assumption.

30 seconds of hands-on inspection beats days of debugging wrong assumptions.

---

## Completion Criteria

**Stage 5a.5 is complete when ALL of these are true:**

□ **Data Dependencies Identified:**
  - All data files listed from implementation_plan.md and spec.md
  - File paths verified (files exist)
  - Data format identified (JSON, CSV, etc.)

□ **Python REPL Inspection Complete:**
  - Each data file opened in Python REPL
  - Actual data values printed and inspected
  - Data structure verified (keys, fields, nesting)

□ **Assumptions Verified:**
  - Every data assumption from spec.md tested against real data
  - Data location verified (which folder/file contains what data)
  - Data offset verified (week_N contains week N or week N-1?)
  - Data completeness verified (are expected values present or null/zero?)

□ **Discrepancies Documented:**
  - Wrong assumptions identified and documented
  - Correct behavior documented with examples
  - Evidence collected (actual data values, file paths)

□ **Specs Updated (if needed):**
  - spec.md updated with correct data model
  - implementation_plan.md updated with correct data loading logic
  - questions.md updated if clarification needed

□ **Confidence Verified:**
  - Confident about data structure
  - Confident about data location
  - Confident about data values
  - Ready to implement with correct assumptions

**Exit Condition:** Stage 5a.5 is complete when you have opened actual data files in Python REPL, printed real values, verified all data assumptions against reality, corrected any wrong assumptions in spec/implementation plan, and are confident the implementation will load correct data.

---

## Next Stage

**If Zero Discrepancies:**
- Proceed to Stage 5b (Implementation Execution)

**If Discrepancies Found:**
- Follow user's decision (restart 5a / fix and continue / discuss)

---

*This stage was created after Feature 02's catastrophic failure. Opening a Python REPL for 30 seconds would have prevented a bug that survived 7 stages.*
