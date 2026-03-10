# S5.5: Hands-On Data Inspection Guide

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Why This Stage Exists](#why-this-stage-exists)
3. [Prerequisites](#prerequisites)
4. [Core Principle](#core-principle)
5. [The Inspection Process](#the-inspection-process)
6. [Pass Criteria](#pass-criteria)
7. [Common Pitfalls](#common-pitfalls)
8. [Critical Questions Checklist](#critical-questions-checklist)
9. [Time Estimate](#time-estimate)
10. [Output Artifacts](#output-artifacts)
11. [Example: What Should Have Happened](#example-what-should-have-happened)
12. [Integration with Other Stages](#integration-with-other-stages)
13. [Why 30 Seconds of Data Inspection Saves Days](#why-30-seconds-of-data-inspection-saves-days)
14. [Remember](#remember)
15. [Completion Criteria](#completion-criteria)
16. [Next Stage](#next-stage)

---

## Quick Start

**What is this guide?**
Hands-On Data Inspection is a critical verification step where you manually inspect actual data files to verify assumptions about data structure, values, and location BEFORE implementing code to prevent catastrophic bugs.

**When do you use this guide?**
- After S5 Round 3 (Implementation planning complete)
- Before S6 (Implementation execution)
- When implementation will load or process data files

**Key Outputs:**
- ✅ All data dependencies identified from implementation_plan.md
- ✅ Data files opened and values inspected in Python REPL
- ✅ Data model assumptions verified against actual data
- ✅ Wrong assumptions corrected in spec.md and implementation_plan.md
- ✅ Ready for S6 (Implementation Execution)

**Time Estimate:**
15-30 minutes (can prevent hours of debugging)

**Exit Condition:**
Hands-On Data Inspection is complete when you have opened actual data files, printed real values, verified assumptions match reality, and corrected any wrong assumptions in spec and implementation plan

---

**Premise:** **NEVER TRUST ASSUMPTIONS - VERIFY WITH ACTUAL DATA**

---

## Why This Stage Exists

**Historical Evidence:** A feature in a previous project had a catastrophic bug that survived implementation and testing:

**The Assumption (WRONG):**
```text
"period_N folder contains period N actual values"
```

**The Reality:**
```python
# period_01/records.json
period_01[0]['actual_value'][0]  # 0.0 (period 1 not complete yet)

# period_02/records.json
period_02[0]['actual_value'][0]  # 33.6 (period 1 now complete)
```

**The Consequences:**
- Implemented code that loaded period_N for both projected and actual values
- All actual_values were 0.0
- Error calculations were meaningless
- Smoke tests showed "(0 have non-zero actual values)" - marked PASS anyway
- Bug survived 7 stages, caught by user in final review

**The Prevention:**
Opening a Python REPL and running 3 commands would have caught this bug in 30 seconds:
```python
import json
period_01 = json.load(open('{data_dir}/period_01/records.json'))
print(period_01[0]['actual_value'][0])  # 0.0 → Assumption is WRONG
```

**This stage is MANDATORY** to prevent implementing code based on wrong assumptions.

---

## Prerequisites

Before starting S5.5:

- [x] S5 Round 3 completed (implementation_plan.md and questions.md exist)
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

**File 1:** {data_dir}/period_01/records.json
- Fields accessed: {projected_field}, {actual_field}
- Array indices: [period_num - 1]
- Expected: projected > 0, actual might be 0 or > 0

**File 2:** {data_dir}/period_02/records.json
- Fields accessed: {actual_field}
- Array indices: [period_num - 1]
- Expected: actual > 0

[Repeat for each file]
```

---

### Step 2: Open Python REPL

**Action:** Open an interactive Python session in the project directory

**Method:**
```bash
cd /path/to/[project name]
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
- Use PRODUCTION data paths (e.g., `data/periods/...`)
- Do NOT use test fixture paths (e.g., `tests/fixtures/...`)
- Load MULTIPLE files (to understand patterns)
- Use paths from spec.md (verify spec assumptions)

**Example:**
```python
import json
from pathlib import Path

# Load multiple periods to understand pattern
period_01_path = Path('{data_dir}/period_01/records.json')
period_02_path = Path('{data_dir}/period_02/records.json')
period_03_path = Path('{data_dir}/period_03/records.json')

with open(period_01_path) as f:
    period_01 = json.load(f)

with open(period_02_path) as f:
    period_02 = json.load(f)

with open(period_03_path) as f:
    period_03 = json.load(f)
```

**Common Mistake:**
```python
# WRONG - only loads one file
period_01 = json.load(open('period_01/records.json'))
# Can't see patterns with one data point
```

**Right:**
```python
# RIGHT - loads multiple files
period_01 = json.load(open('{data_dir}/period_01/records.json'))
period_02 = json.load(open('{data_dir}/period_02/records.json'))
period_03 = json.load(open('{data_dir}/period_03/records.json'))
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
print('actual_value' in period_01[0])  # True
# You now know the key exists, but not what value it contains
```

**Example - RIGHT:**
```python
# This shows you the ACTUAL data
print(f"Period 1 actuals in period_01 folder: {period_01[0]['actual_value'][0]}")  # 0.0
print(f"Period 1 actuals in period_02 folder: {period_02[0]['actual_value'][0]}")  # 33.6
print(f"Period 2 actuals in period_02 folder: {period_02[0]['actual_value'][1]}")  # 0.0
print(f"Period 2 actuals in period_03 folder: {period_03[0]['actual_value'][1]}")  # 22.4

# Now you can see the PATTERN: period_N has 0.0 for period N, period_N+1 has real values
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

**Assumption 1:** "period_N folder contains period N actual values"
```python
# Verification Command:
period_01 = json.load(open('{data_dir}/period_01/records.json'))
actual_period_1_in_period_01 = period_01[0]['actual_value'][0]
print(f"Period 1 actual in period_01: {actual_period_1_in_period_01}")

# Result:
# Period 1 actual in period_01: 0.0

# Conclusion:
# ❌ INVALID - period_N folder has 0.0 for period N actuals
```

**Assumption 2:** "period_N+1 folder contains period N actual values"
```python
# Verification Command:
period_02 = json.load(open('{data_dir}/period_02/records.json'))
actual_period_1_in_period_02 = period_02[0]['actual_value'][0]
print(f"Period 1 actual in period_02: {actual_period_1_in_period_02}")

# Result:
# Period 1 actual in period_02: 33.6

# Conclusion:
# ✅ VALID - period_N+1 folder has real period N actuals
```

**Assumption 3:** "This pattern applies to all periods (not just a special case)"
```python
# Verification Command:
period_03 = json.load(open('{data_dir}/period_03/records.json'))
actual_period_2_in_period_03 = period_03[0]['actual_value'][1]
print(f"Period 2 actual in period_03: {actual_period_2_in_period_03}")

# Result:
# Period 2 actual in period_03: 22.4

# Conclusion:
# ✅ VALID - Pattern applies to ALL periods, not special case
```

---

### Step 6: Understand Value Ranges and Statistics

**Action:** Verify that data values are in realistic ranges

**Why This Matters:**
- Prevents implementing code that produces all zeros (historical bug above)
- Catches edge cases (negative values, nulls, extremely large values)
- Validates that data makes sense for your domain

**Method:**
```python
# Get statistical distribution of values
import statistics

# Collect all actual values for period 1 from period_02 folder
period_1_actuals = [record['actual_value'][0] for record in period_02
                    if len(record['actual_value']) > 0]

print(f"Count: {len(period_1_actuals)}")
print(f"Min: {min(period_1_actuals)}")
print(f"Max: {max(period_1_actuals)}")
print(f"Mean: {statistics.mean(period_1_actuals)}")
print(f"Median: {statistics.median(period_1_actuals)}")
print(f"Std Dev: {statistics.stdev(period_1_actuals)}")

# Count zeros
zero_count = sum(1 for val in period_1_actuals if val == 0.0)
zero_percentage = (zero_count / len(period_1_actuals)) * 100
print(f"Zero percentage: {zero_percentage:.1f}%")

# Sample of non-zero values
non_zero = [val for val in period_1_actuals if val > 0][:10]
print(f"Sample non-zero values: {non_zero}")
```

**Document Findings:**
```markdown
## Value Range Analysis

**Period 1 Actuals (from period_02 folder):**
- Count: {N} records
- Min: 0.0, Max: {max_val}
- Mean: {mean}, Median: {median}
- Std Dev: {std_dev}
- Zero percentage: {X}% (reasonable if not all records have values)
- Sample values: [{val1}, {val2}, ...]

**Conclusion:** Values are realistic for your domain
```

**Red Flags That Should FAIL This Stage:**
- Zero percentage > 90% (almost all zeros)
- Std Dev = 0 (all same value)
- Min = Max (no variance)
- All values are 0.0
- Values outside realistic range for your domain

---

### Step 7: Verify Cross-File Consistency

**Action:** Verify that data across multiple files follows expected patterns

**Why This Matters:**
- Catches schema changes mid-dataset
- Validates that patterns are consistent
- Ensures implementation won't break on certain files

**Method:**
```python
# Check schema consistency across periods
def check_schema(period_data, period_num):
    """Verify data structure is consistent."""
    sample = period_data[0]

    # Replace these with your actual required fields
    required_keys = ['id', 'name', '{field_1}', '{field_2}',
                     'projected_value', 'actual_value']

    for key in required_keys:
        if key not in sample:
            print(f"❌ Period {period_num}: Missing key '{key}'")
            return False

    # Verify array lengths match expected
    proj_len = len(sample['projected_value'])
    act_len = len(sample['actual_value'])
    expected_length = {N}  # Replace with your expected array length

    if proj_len != expected_length:
        print(f"⚠️  Period {period_num}: projected_value has {proj_len} items (expected {expected_length})")

    if act_len != expected_length:
        print(f"⚠️  Period {period_num}: actual_value has {act_len} items (expected {expected_length})")

    print(f"✅ Period {period_num}: Schema valid")
    return True

# Test multiple periods
check_schema(period_01, 1)
check_schema(period_02, 2)
check_schema(period_03, 3)
```

**Document Findings:**
```markdown
## Schema Consistency Check

Verified periods 1-3:
- ✅ All have required keys
- ✅ All have {N}-item arrays
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
period_01 = json.load(open('{data_dir}/period_01/records.json'))
period_02 = json.load(open('{data_dir}/period_02/records.json'))

# Print actual values
print(f"Period 1 actuals in period_01: {period_01[0]['actual_value'][0]}")  # 0.0
print(f"Period 1 actuals in period_02: {period_02[0]['actual_value'][0]}")  # 33.6
\`\`\`

### Assumptions Tested

| Assumption | Verification | Result | Valid? |
|------------|--------------|--------|--------|
| period_N has period N actuals | Printed period_01[0]['actual_value'][0] | 0.0 | ❌ FALSE |
| period_N+1 has period N actuals | Printed period_02[0]['actual_value'][0] | 33.6 | ✅ TRUE |
| Pattern applies to all periods | Tested periods 1, 2, 3 | Consistent | ✅ TRUE |

### Value Range Analysis

**Period 1 Actuals (from period_02):**
- Count: {N}, Min: 0.0, Max: {max}
- Mean: {mean}, Median: {median}, Std Dev: {std}
- Zero percentage: {X}% (realistic for your domain)

### Key Findings

1. **period_N folder has 0.0 for period N actuals** (verified empirically)
2. **period_N+1 folder has real period N actuals** (verified empirically)
3. **Pattern is consistent across all periods** (tested periods 1-3)
4. **Values are in realistic range for your domain** (verified statistics)

### Implementation Impact

**Spec.md claimed:** "No special handling needed"
**Reality:** MUST load period_N+1 folder for actual values

**Code changes required:**
- Load TWO folders (period_N and period_N+1)
- Create TWO data loader instances
- Get projected values from period_N, actuals from period_N+1

---

### Discrepancies with Spec

**Discrepancy 1:** Spec says period_N has period N actuals
- **Spec claim:** "Arrays already handle offset"
- **Data shows:** period_N has 0.0 for period N actuals
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

Do NOT proceed to S6 (Implementation). Your implementation plan is based on wrong assumptions.

**Report to User:**

Use this template:

```markdown
## ⚠️ DATA INSPECTION FAILED - User Input Required

I completed S5.5 (Hands-On Data Inspection) and found discrepancies
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

**Option A (Recommended):** Fix spec and implementation plan, restart S5
1. Update spec.md based on actual data findings
2. Restart S5 Round 1 to regenerate implementation_plan.md
3. Re-run S5.5 to verify new assumptions
4. Proceed to S6 only after zero discrepancies

**Option B:** Fix spec and implementation plan, continue to S6
1. Update spec.md based on findings
2. Manually update implementation_plan.md tasks
3. Continue to S6
4. Risk: Implementation plan may still have subtle errors

**Option C:** Discuss findings first
1. Review each discrepancy together
2. Clarify data model
3. Then update spec/implementation plan
4. Re-run S5.5 to verify

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
**Conclusion:** Safe to proceed to S6

All TODO items are based on validated assumptions.
```

---

## Pass Criteria

S5.5 is complete when:

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
- [ ] **Proceed to S6**

**Scenario 2: Discrepancies Found**
- [ ] Documented ALL discrepancies with evidence
- [ ] Reported to user with 3 options
- [ ] Waited for user decision
- [ ] Executed user's choice (fix spec, restart S5, discuss, etc.)
- [ ] Re-ran S5.5 after fixes
- [ ] Now zero discrepancies
- [ ] **Proceed per user decision**

---

## Common Pitfalls

### ❌ Pitfall 1: Only Checking "Exists"

**Wrong:**
```python
print('actual_value' in period_01[0])  # True
# Conclusion: "Data exists, looks good"
```

**Right:**
```python
print(f"Actual value: {period_01[0]['actual_value'][0]}")  # 0.0
# Conclusion: "Key exists but value is 0.0 - investigate why"
```

### ❌ Pitfall 2: Only Loading One File

**Wrong:**
```python
period_01 = json.load(open('period_01/records.json'))
print(period_01[0]['actual_value'][0])  # 0.0
# Conclusion: "Period 1 actuals are 0.0" (but is this the pattern or special case?)
```

**Right:**
```python
period_01 = json.load(open('period_01/records.json'))
period_02 = json.load(open('period_02/records.json'))
period_03 = json.load(open('period_03/records.json'))
print(f"Period 1 in period_01: {period_01[0]['actual_value'][0]}")  # 0.0
print(f"Period 1 in period_02: {period_02[0]['actual_value'][0]}")  # 33.6
print(f"Period 2 in period_03: {period_03[0]['actual_value'][1]}")  # 22.4
# Conclusion: "Pattern is period_N has 0.0, period_N+1 has real values"
```

### ❌ Pitfall 3: Using Test Fixtures Instead of Real Data

**Wrong:**
```python
# Test fixtures might have simplified/fake data
data = json.load(open('tests/fixtures/sample_data.json'))
```

**Right:**
```python
# Real production data shows actual behavior
data = json.load(open('{data_dir}/period_01/records.json'))
```

### ❌ Pitfall 4: Trusting Variable Names

**Wrong:**
```python
# Variable name suggests it has period 1 actuals
period_1_actual_values = period_01[0]['actual_value'][0]
print(period_1_actual_values)  # 0.0
# Conclusion: "Period 1 actuals are 0.0, maybe no data yet?"
```

**Right:**
```python
# Don't trust names - verify the actual values
period_1_actual_in_period_01 = period_01[0]['actual_value'][0]  # 0.0
period_1_actual_in_period_02 = period_02[0]['actual_value'][0]  # 33.6
# Conclusion: "period_01 folder name is misleading - has 0.0, not real actuals"
```

### ❌ Pitfall 5: Silently Fixing Discrepancies

**Wrong:**
```python
# Find discrepancy
print(period_01[0]['actual_value'][0])  # 0.0 (expected > 0)
# Conclusion: "Spec is wrong, I'll fix it and continue"
# [Updates spec.md and implementation_plan.md silently]
# [Proceeds to S6]
```

**Right:**
```python
# Find discrepancy
print(period_01[0]['actual_value'][0])  # 0.0 (expected > 0)
# Conclusion: "Spec is wrong - STOP and report to user"
# [Documents discrepancy with evidence]
# [Reports to user with 3 options]
# [Waits for user decision]
```

---

## Critical Questions Checklist

Before marking S5.5 complete, answer ALL questions:

```markdown
## S5.5 Critical Questions

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

After S5.5:

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

## Example: What Should Have Happened

**What Actually Happened (WRONG):**

S5 → S6 (skipped data inspection)
- Assumed period_N folder has period N actuals
- Implemented based on assumption
- All actuals were 0.0
- Error calculations were meaningless
- Bug survived to user final review

**What Should Have Happened (RIGHT):**

S5 → **S5.5 (Data Inspection)** → S6

**S5.5 Process:**
```python
# Step 1: Load actual data
import json
period_01 = json.load(open('{data_dir}/period_01/records.json'))
period_02 = json.load(open('{data_dir}/period_02/records.json'))

# Step 2: Test assumption
print(f"Period 1 actuals in period_01: {period_01[0]['actual_value'][0]}")  # 0.0
print(f"Period 1 actuals in period_02: {period_02[0]['actual_value'][0]}")  # 33.6

# Step 3: Realize assumption is WRONG
# period_01 folder does NOT have period 1 actuals (has 0.0)
# period_02 folder DOES have period 1 actuals (has 33.6)

# Step 4: Report to user
# "Spec.md says 'no code changes needed' but data shows we need period_N+1"

# Step 5: User chooses Option A (fix spec, restart S5)

# Step 6: Update spec.md with correct data model

# Step 7: Restart S5 with correct understanding

# Step 8: Re-run S5.5 to verify fixes

# Step 9: Proceed to S6 with validated assumptions
```

**Result:** Bug caught before writing any code.

---

## Integration with Other Stages

**S5 Round 3 (Implementation Planning):**
- Creates implementation_plan.md based on spec.md assumptions
- Does NOT verify assumptions with actual data

**S5.5 (Hands-On Data Inspection) - THIS STAGE:**
- Verifies spec.md assumptions with REAL data
- Catches wrong assumptions BEFORE implementing
- Reports discrepancies to user
- May trigger restart of S5 if spec is wrong

**S6 (Implementation Execution):**
- Implements based on implementation_plan.md
- Assumes implementation plan is correct (validated by S5.5)
- If S5.5 skipped, may implement wrong solution

---

## Why 30 Seconds of Data Inspection Saves Days

**Time to catch bug in S5.5:** 30 seconds
```python
import json
period_01 = json.load(open('{data_dir}/period_01/records.json'))
print(period_01[0]['actual_value'][0])  # 0.0 → "Wait, this should be > 0!"
```

**Time to fix bug caught in S5.5:** 30 minutes
- Update spec.md with correct data model
- Restart S5 to regenerate implementation_plan.md
- Proceed to S6 with correct plan

**Time to fix bug caught in S9 (Epic QC):** 4+ hours
- Debug why error calculations are wrong
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

**MORAL: Spend 30 seconds in S5.5 to save hours (or days) later.**

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

**S5.5 is complete when ALL of these are true:**

- [ ] **Data Dependencies Identified:**
  - All data files listed from implementation_plan.md and spec.md
  - File paths verified (files exist)
  - Data format identified (JSON, CSV, etc.)

- [ ] **Python REPL Inspection Complete:**
  - Each data file opened in Python REPL
  - Actual data values printed and inspected
  - Data structure verified (keys, fields, nesting)

- [ ] **Assumptions Verified:**
  - Every data assumption from spec.md tested against real data
  - Data location verified (which folder/file contains what data)
  - Data offset verified (does period_N contain period N data or period N-1?)
  - Data completeness verified (are expected values present or null/zero?)

- [ ] **Discrepancies Documented:**
  - Wrong assumptions identified and documented
  - Correct behavior documented with examples
  - Evidence collected (actual data values, file paths)

- [ ] **Specs Updated (if needed):**
  - spec.md updated with correct data model
  - implementation_plan.md updated with correct data loading logic
  - questions.md updated if clarification needed

- [ ] **Confidence Verified:**
  - Confident about data structure
  - Confident about data location
  - Confident about data values
  - Ready to implement with correct assumptions

**Exit Condition:** S5.5 is complete when you have opened actual data files in Python REPL, printed real values, verified all data assumptions against reality, corrected any wrong assumptions in spec/implementation plan, and are confident the implementation will load correct data.

---

## Next Stage

**If Zero Discrepancies:**
- Proceed to S6 (Implementation Execution)

**If Discrepancies Found:**
- Follow user's decision (restart S5 / fix and continue / discuss)

---

*This stage was created after a feature's catastrophic data-loading bug survived 7 stages before being caught by the user. Opening a Python REPL for 30 seconds would have prevented the bug entirely.*
