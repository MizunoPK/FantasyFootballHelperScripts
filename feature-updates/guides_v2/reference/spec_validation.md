# S2.5: Spec Validation Guide

---

## Quick Start

**What is this guide?**
Spec Validation is a critical gate where you re-validate spec.md against the original epic by assuming the spec is completely wrong and verifying everything from scratch to catch fundamental misunderstandings before implementation.

**When do you use this guide?**
- After S2 (Feature Deep Dive) complete
- Before S3 (Cross-Feature Sanity Check)
- When you need to validate spec accuracy against epic intent

**Key Outputs:**
- ✅ Epic notes re-read with fresh perspective (spec closed during initial review)
- ✅ Requirements validated against epic (literal meaning checked)
- ✅ Spec assumptions questioned and verified
- ✅ Misalignments identified and corrected
- ✅ Ready for S3 (Cross-Feature Sanity Check)

**Time Estimate:**
30-45 minutes per feature

**Exit Condition:**
Spec Validation is complete when the spec is re-validated against epic from scratch (assuming spec is wrong), all discrepancies are corrected, and you have high confidence spec reflects epic intent

---

**Premise:** **ASSUME SPEC.MD IS COMPLETELY WRONG**

---

## Why This Stage Exists

**Historical Evidence:** Feature 02 (Accuracy Sim) spec.md contained a fundamental error that survived:
- S2 (spec creation)
- S5 (22 verification iterations)
- S6 (implementation)
- S7.P1-S7.P2 (smoke testing and QC rounds)
- **User caught it in S9.P3**

**The Problem:** Once spec.md is written, all subsequent stages trust it as gospel truth and never question it against the original epic.

**The Solution:** This mandatory validation stage assumes the spec is wrong and re-validates everything from scratch.

---

## Prerequisites

Before starting S2.5:

- [x] S2 (Feature Deep Dive) completed
- [x] spec.md file exists
- [x] checklist.md file exists
- [x] Epic notes file available

---

## The Validation Process

### Step 1: Close the Spec (Don't Reference It)

**Action:** Close spec.md and DO NOT look at it during initial validation

**Why:** Reading the spec first creates confirmation bias. You'll look for evidence that supports the spec rather than questioning it.

**Method:**
```bash
# Physically close the file in your editor
# Work ONLY from epic notes during Steps 2-4
```

---

### Step 2: Re-Read Epic Notes from Scratch

**Action:** Read the epic notes file word-for-word as if seeing it for the first time

**Critical Reading Questions:**

- [ ] **Literal Meaning:** What does each sentence ACTUALLY say? (not what I think it means)
- [ ] **Examples vs Patterns:** Is this an example of a general pattern, or a special case?
  - Example: "Use week_17 for projected, week_18 for actual"
  - Question: Is week 17 special, or is this a pattern for ALL weeks?
- [ ] **Implicit Requirements:** What requirements are implied but not stated?
- [ ] **Ambiguous Terms:** What terms could be interpreted multiple ways?

**Document Findings:**
```markdown
## Epic Re-Reading Findings

**Requirement 1:** [Quote from epic]
- Literal meaning: [What it actually says]
- My interpretation: [How I understand it]
- Ambiguity: [Any unclear parts]
- Evidence needed: [What would verify this]

[Repeat for each requirement]
```

---

### Step 3: Investigate Each Requirement Independently

**For EACH epic requirement, perform independent investigation:**

#### 3A: Code Investigation

**Question:** What does the actual codebase do?

**Method:**
- Read relevant source files
- Document actual behavior with line numbers
- Quote relevant code snippets
- Note any differences from epic description

**Example:**
```markdown
Requirement: "Use week_18 folders for actual points in week 17"

Code Investigation:
- File: simulation/json_exporter.py lines 303-312
- Finding: "actuals for weeks 1 to N-1, 0.0 for N to 17"
- Interpretation: Week_N folder has 0.0 for week N actuals
- Implication: Must use week_N+1 to get week N actuals
```

#### 3B: Data Investigation (MANDATORY)

**Question:** What do actual data files contain?

**Method:**
```python
# Open Python REPL
import json
from pathlib import Path

# Load REAL data files (not test fixtures)
week_01 = json.load(open('simulation/sim_data/2021/weeks/week_01/qb_data.json'))
week_02 = json.load(open('simulation/sim_data/2021/weeks/week_02/qb_data.json'))

# Print ACTUAL values (not just check "exists")
print(f"Week 1 actuals in week_01: {week_01[0]['actual_points'][0]}")
print(f"Week 1 actuals in week_02: {week_02[0]['actual_points'][0]}")

# Compare multiple weeks to understand pattern
week_03 = json.load(open('simulation/sim_data/2021/weeks/week_03/qb_data.json'))
print(f"Week 2 actuals in week_03: {week_03[0]['actual_points'][1]}")
```

**Document Findings:**
```markdown
Data Investigation Results:

File: simulation/sim_data/2021/weeks/week_01/qb_data.json
- actual_points[0] (week 1): 0.0

File: simulation/sim_data/2021/weeks/week_02/qb_data.json
- actual_points[0] (week 1): 33.6

Pattern: Week_N folder has 0.0 for week N, week_N+1 has real value
Conclusion: Must load week_N+1 for week N actuals
```

#### 3C: Pattern Recognition

**Question:** Is this an example or a special case?

**Method:**
- If epic gives one example (e.g., "week 17"), test with other values (week 1, week 2)
- Check if pattern holds across all cases
- Document whether it's general or special

**Example:**
```markdown
Epic says: "week_17 folders for projected, week_18 folders for actual"

Pattern Test:
- Week 1: week_01 (projected), week_02 (actual) ✓ Pattern holds
- Week 2: week_02 (projected), week_03 (actual) ✓ Pattern holds
- Week 17: week_17 (projected), week_18 (actual) ✓ Pattern holds

Conclusion: This is a GENERAL PATTERN, not week 17 special case
```

---

### Step 4: Build Evidence Table

**Create a table documenting HOW each claim was verified:**

```markdown
## Assumption Validation Table

| Assumption | Verified How | Evidence | Valid? |
|------------|--------------|----------|--------|
| Week_N folder has week N actuals | Manual data inspection | week_01[0]['actual_points'][0] = 0.0 | ❌ FALSE |
| Week_N+1 folder has week N actuals | Manual data inspection | week_02[0]['actual_points'][0] = 33.6 | ✅ TRUE |
| Pattern applies to all weeks | Tested weeks 1,2,17 | All follow same pattern | ✅ TRUE |
| PlayerManager handles conversion | Code inspection | PlayerManager.py line 327 hardcodes path | ❌ Partial |
```

**Rules:**
- Every assumption must have "Verified How" entry
- "Verified How" must be one of: Manual data inspection, Code inspection, Test execution, User confirmation
- No assumptions without evidence
- Document FALSE assumptions (these are the bugs!)

---

### Step 5: Compare Findings with Spec

**Action:** NOW open spec.md and compare with your independent findings

**For each spec claim:**

```markdown
## Spec Comparison

**Spec Claim 1:** [Quote from spec.md]
- Epic says: [Quote from epic notes]
- Investigation found: [Your findings from Step 3]
- Match? [YES/NO]
- Discrepancy: [Describe if NO]

[Repeat for each claim]
```

---

### Step 6: Document ALL Discrepancies

**Even minor discrepancies must be documented:**

```markdown
## Discrepancies Found

### Discrepancy 1: [Name]

**Epic Says:**
> [Exact quote from epic]

**Spec Says:**
> [Exact quote from spec.md]

**Investigation Found:**
- [What code inspection revealed]
- [What data inspection revealed]

**Impact:**
- [What this means for implementation]
- [How severe is this error]

**Recommended Fix:**
- [How spec.md should be updated]

---

[Repeat for each discrepancy]
```

---

### Step 7: User Reporting (If Discrepancies Found)

**IF ANY DISCREPANCIES FOUND:**

#### 7A: STOP IMMEDIATELY

- Do NOT proceed to S3
- Do NOT proceed to implementation
- Do NOT "fix it yourself and continue"

#### 7B: Report to User

Use this template:

```markdown
## ⚠️ SPEC VALIDATION FAILED - User Input Required

I completed S2.5 (Spec Validation) and found [X] discrepancies between
the epic requirements and spec.md.

### Discrepancy Summary

1. **[Discrepancy Name]**
   - **Epic says:** [Quote]
   - **Spec says:** [Quote]
   - **Impact:** [What this means]

[Repeat for each discrepancy]

### Analysis

These discrepancies suggest spec.md may be fundamentally incorrect.

**Why This Matters:**
- Spec.md drives all subsequent stages (S5 TODO creation, S6 implementation)
- If spec is wrong, TODO will be wrong, implementation will be wrong
- Better to catch now than after implementing wrong solution

### How Would You Like to Proceed?

**Option A (Recommended):** Fix spec, restart from S2
- Update spec.md to match epic requirements
- Re-run S2.5 to verify fixes
- Continue to S3 only after zero discrepancies

**Option B:** Fix spec, continue to S3
- Update spec.md
- Continue to S3 (Cross-Feature Sanity Check)
- Risk: May still have subtle errors

**Option C:** Discuss discrepancies first
- Review each discrepancy together
- Clarify epic intent
- Then decide on path forward

**My Recommendation:** Option A
**Reason:** [Specific reason based on severity of discrepancies]

Please advise how you'd like to proceed.
```

#### 7C: Wait for User Decision

**DO NOT make this choice autonomously**

Wait for user to choose:
- Option A: Fix and restart
- Option B: Fix and continue
- Option C: Discuss first

#### 7D: Execute User's Choice

**If Option A (Fix and Restart):**
1. Update spec.md based on discrepancies
2. Update checklist.md if needed
3. Re-run S2.5 from Step 1
4. Continue only when zero discrepancies
5. Proceed to S3

**If Option B (Fix and Continue):**
1. Update spec.md based on discrepancies
2. Update checklist.md if needed
3. Document risk in spec.md
4. Proceed to S3

**If Option C (Discuss):**
1. Have conversation about each discrepancy
2. Get user clarification on intent
3. Update spec.md based on clarifications
4. Return to S2.5 Step 1 to re-verify

---

### Step 8: Final Verification

**IF ZERO DISCREPANCIES:**

Answer these critical questions:

```markdown
## Critical Questions Checklist

S2.5 Validation:
- [ ] Did I close spec.md before re-reading epic? (no confirmation bias)
- [ ] Did I re-read ENTIRE epic word-for-word?
- [ ] Did I test every example with multiple values? (pattern vs special case)
- [ ] Did I manually inspect actual data files? (not just code)
- [ ] Did I document evidence for EVERY assumption?
- [ ] Did I compare EVERY spec claim with epic + investigation?
- [ ] Did I document even minor discrepancies?
- [ ] Would a new agent reading this spec make correct implementation?

Data Investigation:
- [ ] Did I load REAL data files (not test fixtures)?
- [ ] Did I print ACTUAL values (not just check exists)?
- [ ] Did I compare multiple files/weeks?
- [ ] Did I document value ranges (min, max, typical)?
- [ ] Did I verify spec assumptions against real data?

Code Investigation:
- [ ] Did I read actual source code (not assume behavior)?
- [ ] Did I document line numbers for claims?
- [ ] Did I quote relevant code snippets?
- [ ] Did I test assumptions with actual API calls?

Pattern Analysis:
- [ ] Did I test general patterns with multiple examples?
- [ ] Did I distinguish example from special case?
- [ ] Did I verify patterns hold across all cases?
```

All questions must be YES to pass.

---

## Pass Criteria

S2.5 is complete when:

**Scenario 1: Zero Discrepancies**
- [ ] All epic requirements have matching spec claims
- [ ] All spec claims verified with evidence (code OR data)
- [ ] All assumptions tested with hands-on investigation
- [ ] Evidence table complete (no empty cells)
- [ ] All critical questions answered YES
- [ ] Proceed to S3

**Scenario 2: Discrepancies Found and Resolved**
- [ ] All discrepancies reported to user
- [ ] User chose path forward
- [ ] Spec.md updated based on user decision
- [ ] Re-ran S2.5 after updates
- [ ] Now zero discrepancies
- [ ] Proceed per user decision

---

## Common Pitfalls

### ❌ Pitfall 1: Reading Spec First

**Wrong:**
```
Read spec.md → Re-read epic → "Yep, matches"
```

**Right:**
```
Close spec.md → Re-read epic → Investigate independently → Compare
```

### ❌ Pitfall 2: Trusting Assumptions

**Wrong:**
```
"Week_N folder should have week N actuals" → [Don't verify]
```

**Right:**
```
"Week_N folder should have week N actuals" → [Load file, print value, verify]
```

### ❌ Pitfall 3: Ignoring Minor Discrepancies

**Wrong:**
```
"Small difference in wording, same meaning" → [Ignore]
```

**Right:**
```
"Small difference in wording" → [Document, get user confirmation]
```

### ❌ Pitfall 4: Silently Fixing Errors

**Wrong:**
```
Find discrepancy → Fix spec.md → Continue
```

**Right:**
```
Find discrepancy → Report to user → Wait for decision → Execute choice
```

---

## Example: How Feature 02 Should Have Used This

**What Actually Happened (WRONG):**

S2:
- Read epic line 8: "week_17 folders for projected, week_18 for actual"
- Interpreted as: "Week 17 is special case"
- Wrote spec: "No code changes needed"
- Never manually inspected data

Result: Catastrophic bug that survived 7 stages

**What Should Have Happened (RIGHT):**

S2.5:
1. Close spec.md ✓
2. Re-read epic: "week_17 folders for projected, week_18 for actual"
3. Question: "Why week 17? Is this special or pattern?"
4. Investigate code: json_exporter.py shows week_N has 0.0 for week N
5. Manual inspection:
   ```python
   week_01[0]['actual_points'][0]  # 0.0
   week_02[0]['actual_points'][0]  # 33.6
   ```
6. Realize: Pattern applies to ALL weeks
7. Compare with spec: "Spec says 'no code changes' but need week_N+1!"
8. Document discrepancy
9. Report to user
10. Update spec: "Load week_N for projected, week_N+1 for actual"

Result: Bug caught before implementation

---

## Time Estimate

- **Normal case (zero discrepancies):** 30-60 minutes
- **Discrepancies found:** 1-2 hours (includes user discussion)

**Note:** This time investment prevents days/weeks of implementing wrong solution.

---

## Output Artifacts

After S2.5:

1. **spec_validation_findings.md** (NEW FILE):
   - Epic re-reading notes
   - Code investigation findings
   - Data investigation results
   - Evidence table
   - Comparison with spec.md
   - Discrepancies (if any)

2. **Updated spec.md** (if discrepancies found)

3. **Updated checklist.md** (if needed)

---

## Completion Criteria

**S2.5 is complete when ALL of these are true:**

□ **Epic Re-Reading Complete:**
  - Epic notes file re-read word-for-word (spec.md closed during initial read)
  - Critical reading questions answered for each requirement
  - Literal meaning documented for ambiguous terms

□ **Code Investigation Complete:**
  - Method signatures verified from actual source code
  - Integration points verified (data passed between components)
  - Assumptions validated against real code

□ **Data Investigation Complete:**
  - Sample data files opened and inspected
  - Data structure verified (format, fields, types)
  - Spec assumptions validated against actual data

□ **Evidence Collected:**
  - File paths cited for code evidence
  - Line numbers cited for epic evidence
  - Data examples collected from real files

□ **Validation Findings Documented:**
  - spec_validation_findings.md created
  - Epic vs spec comparison complete
  - Discrepancies identified (if any)

□ **Discrepancies Resolved:**
  - If discrepancies found: spec.md updated OR user decision documented
  - If zero discrepancies: validation confidence documented

**Exit Condition:** S2.5 is complete when spec.md is validated against epic from scratch, all discrepancies are resolved or user-approved, and you have high confidence the spec accurately reflects epic intent.

---

## Next Stage

**If Zero Discrepancies:**
- Proceed to S3 (Cross-Feature Sanity Check)

**If Discrepancies Found:**
- Follow user's decision (restart S2 / continue / discuss)

---

## Remember

**Core Principle:** ASSUME SPEC IS WRONG

- Spec.md is a hypothesis, not truth
- Epic notes are source of truth
- Evidence (code + data) validates hypothesis
- User resolves ambiguities

**Goal:** Prevent implementing the wrong solution by catching spec errors early.

---

*This stage was created after Feature 02's catastrophic failure. It would have prevented the bug that survived 7 stages.*
