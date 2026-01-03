# Bug Fix Lessons Learned: Week Offset Logic

**Created:** 2026-01-02
**Bug Priority:** HIGH
**Feature:** feature_02_accuracy_sim_json_integration

---

## Why This Bug Happened

### Root Cause Summary

This catastrophic bug occurred due to **THREE compounding failures** during Stage 2 (spec creation):

1. **Reading Comprehension Failure** - Misinterpreted epic line 8 as "week 17 special case" instead of "ALL weeks use week_N + week_N+1"
2. **Data Model Investigation Failure** - Never investigated json_exporter.py or manually inspected data files
3. **Assumption Validation Failure** - Assumed week_N folder contains week N actuals (WRONG)

### Detailed Breakdown

**Stage 2 Failure (Original Feature Spec Creation):**
```
Epic notes line 8: "use week_17 folders for projected_points,
                   then look at actual_points array in week_18 folders"

MY INTERPRETATION (WRONG):
"Week 17 is a special case that needs week_18"

CORRECT INTERPRETATION:
"Week 17 is an EXAMPLE of the pattern ALL weeks follow"
```

**What I Should Have Done (Stage 2.5 Principles):**
1. Close spec.md, re-read epic notes with fresh eyes
2. Ask: "Why would week 17 be special? What makes it different?"
3. Realize: Nothing makes week 17 special → pattern must apply to ALL weeks
4. Manually inspect data: week_01 vs week_02 to verify assumption
5. Investigate json_exporter.py to understand data model
6. Document evidence BEFORE writing spec

**What I Actually Did:**
1. Read epic notes once
2. Made assumption: "Week_N folder has week N actuals"
3. Wrote spec based on assumption (no verification)
4. Never opened data files to verify
5. Never questioned the assumption through 7 stages

### The Systemic Failures

**7 Stages Failed to Catch This Bug:**

1. **Stage 2 (Spec Creation):** Misinterpreted epic, no data inspection
2. **Stage 5a (TODO Creation):** Trusted spec, 24 iterations never questioned it
3. **Stage 5b (Implementation):** Implemented spec exactly (which was wrong)
4. **Stage 5ca (Smoke Testing):** **CATASTROPHIC** - Saw "(0 have non-zero points)" and marked PASS
5. **Stage 5cb Round 1:** Checked structure exists, never checked values
6. **Stage 5cb Round 2:** Verified test coverage, never ran actual calculations
7. **Stage 5cb Round 3:** Fixed data access bug, never questioned data source

**User Discovery (Stage 5cc):**
- User asked ONE basic verification question
- Immediately exposed the bug
- This is the question ALL stages should have asked

---

## Prevention Strategies Applied in This Bug Fix

### Strategy 1: Stage 2.5 Principles (Spec Validation)

**What We're Doing Differently:**

✅ **Re-Read Epic Notes with Fresh Eyes**
- Closed existing spec.md before re-reading epic notes
- Treated epic line 8 as if seeing it for first time
- Asked: "What does this ACTUALLY say?" (not "what do I think it says?")

✅ **Validate EVERY Claim Against Evidence**
- Created "Assumption Validation Table" in spec.md
- For EACH assumption, documented HOW verified (code line OR data value)
- No claims without evidence

✅ **Investigate Codebase Independently**
- Read json_exporter.py lines 303-312 to understand data generation
- Found explicit comment: "actuals for weeks 1 to N-1, 0.0 for N to 17"
- Verified code matches data model

**Evidence:**
- Spec.md "Epic Requirement" section - direct quote from notes
- Spec.md "Assumption Validation Table" - 5 assumptions, all verified
- Spec.md "Data Model Investigation" - json_exporter.py analysis

### Strategy 2: Stage 5a.5 Principles (Hands-On Data Inspection)

**What We're Doing Differently:**

✅ **Manual Data Inspection BEFORE Implementing**
- Opened Python REPL
- Loaded week_01/qb_data.json and week_02/qb_data.json
- Printed ACTUAL VALUES (not just "exists" checks)
- Verified week_01 has 0.0, week_02 has 33.6

```python
# ACTUAL COMMAND RUN:
import json
week_01 = json.load(open('simulation/sim_data/2021/weeks/week_01/qb_data.json'))
week_02 = json.load(open('simulation/sim_data/2021/weeks/week_02/qb_data.json'))
print(f'Week 1 actuals in week_01 folder: {week_01[0]["actual_points"][0]}')  # 0.0
print(f'Week 1 actuals in week_02 folder: {week_02[0]["actual_points"][0]}')  # 33.6
```

✅ **Documented Findings with Real Data**
- Spec.md includes actual output from manual inspection
- Evidence is empirical (real data values), not theoretical
- Can reproduce findings by running same commands

**Evidence:**
- Spec.md "Manual Data Inspection Results" section
- Shows actual Python commands and actual output
- Documented BEFORE designing solution

### Strategy 3: Data Sanity Checks in Smoke Testing

**What We're Doing Differently:**

✅ **Statistical Validation (Not Just Structure)**
- Zero percentage check: >90% zeros → AUTOMATIC FAIL
- Variance check: stddev = 0 → AUTOMATIC FAIL
- Realistic range check: MAE should be 3-8 for NFL
- Non-zero count check: 0 players with non-zero → AUTOMATIC FAIL

✅ **EXPLICIT RULE for "0 Have Non-Zero"**
- Any smoke test output containing "0 have non-zero points" → AUTOMATIC FAIL
- No exceptions
- No "maybe it's okay" reasoning

✅ **Critical Question BEFORE Marking PASS**
- "If I saw these values in production, would I be suspicious?"
- If answer is YES → mark FAIL (investigate)
- If answer is NO → proceed with other checks

**Evidence:**
- Spec.md "Smoke Testing" section includes complete statistical validation code
- Documented explicit failure conditions
- Critical question checklist included

### Strategy 4: Statistical Validation in QC Round 2

**What We're Doing Differently:**

✅ **Output Validation Iteration (NEW)**
- Run actual MAE calculations (not just check "tests pass")
- Verify MAE in realistic range (3-8 for QB)
- Check variance across positions
- Compare with historical data if available

✅ **Semantic Validation (Not Just Structure)**
- Verify VALUES are realistic, not just that arrays exist
- Check: Do these numbers make sense for NFL?
- Ask: Would this be useful to a user?

**Evidence:**
- Spec.md includes MAE range validation (3-8)
- Smoke testing checks variance and zero percentage
- QC Round 2 will verify output values

### Strategy 5: Spec Re-Validation (Iteration 25)

**What We're Doing Differently:**

✅ **Epic Notes as Source of Truth**
- During TODO creation, will re-read epic notes (ignore spec.md)
- Verify TODO matches EPIC NOTES (not just spec.md)
- If discrepancy found → STOP and report to user

✅ **Mandatory User Reporting If Discrepancies Found**
- Do NOT silently fix discrepancies
- Report ALL issues to user with impact analysis
- Ask user: "Do you want to restart TODO iterations from beginning after fixing spec?"
- Options:
  - A) Fix spec, restart Stage 5a from Iteration 1 (recommended)
  - B) Fix spec and TODO, continue (risky - TODO may be wrong)
  - C) Discuss discrepancies first
- Wait for user decision before proceeding

**Evidence:**
- This bug fix spec was created by re-reading epic notes first
- Spec directly quotes epic notes line 8
- All claims traced back to epic notes or empirical evidence

### Strategy 6: Critical Questions Checklists

**What We're Doing Differently:**

✅ **Added to Verification Plan**
- Stage 2: "Did I verify this claim with code/data?"
- Stage 5a: "Does this contradict epic requirements?"
- Stage 5ca: "Are these values statistically realistic?"
- Stage 5cb: "If I saw this in production, would I be suspicious?"

✅ **Mandatory for Each Stage**
- Must answer ALL critical questions
- Cannot mark stage complete without checklist
- Documented in spec.md "Verification Plan"

**Evidence:**
- Spec.md includes critical questions for each stage
- Smoke testing includes "Critical Question Checklist"
- Verification plan requires answering all questions

---

## How This Bug Fix is Different

### Original Feature 02 Spec (BROKEN):

```markdown
### Week 17/18 Logic Clarification

**Epic request says:**
> "Use week_17 folders for projected_points, week_18 folders for actual_points"

**Investigation findings:**
- JSON arrays already handle this
- NO special handling needed ❌ WRONG

**Conclusion:**
- Epic request is asking to VERIFY this works
- No code changes needed ❌ WRONG
```

**Problems:**
- Never investigated actual data model
- Made assumption "no code changes needed"
- Treated epic request as "verification only"
- Never manually inspected data files

### This Bug Fix Spec (CORRECT):

```markdown
### Epic Requirement (Direct Quote)

**Source:** integrate_new_player_data_into_simulation_notes.txt line 8

> "use week_17 folders for projected_points, then look at
   actual_points array in week_18 folders"

**Interpretation:**
- Pattern applies to ALL weeks (not just 17)

**Manual Data Inspection:**
- week_01[0]['actual_points'][0] = 0.0 (verified empirically)
- week_02[0]['actual_points'][0] = 33.6 (verified empirically)

**Data Model Investigation:**
- json_exporter.py:306 - "if week < current_week"
- Week_N folder has actuals for weeks 1 to N-1 only

**Conclusion:**
- ALL weeks need week_N + week_N+1 pattern
- Code changes required: Update _load_season_data()
```

**Differences:**
- ✓ Direct quote from epic notes (not interpretation)
- ✓ Manual data inspection with actual values
- ✓ Code investigation (json_exporter.py)
- ✓ Evidence for every claim
- ✓ Assumption Validation Table

---

## Cross-Epic Verification (User Requirement)

**User specified:** "verify ALL changes made in this epic against the notes and original documentation/code of the simulations"

**How We're Implementing This:**

1. **Epic Notes Verification:**
   - [ ] Line 1: Update to use JSON files (feature_01 ✓, feature_02 ✓)
   - [ ] Line 3-6: Load JSON from week folders (feature_01 ✓, feature_02 ✓)
   - [ ] Line 6: Handle new fields (feature_01 ✓, feature_02 ✓)
   - [ ] Line 8: Week_N + week_N+1 pattern (feature_01 N/A, feature_02 ⏳ THIS FIX)

2. **Original Simulation Code Verification:**
   - Read pre-epic AccuracySimulationManager.py
   - Identify calculation algorithms (MAE, ranking metrics)
   - Verify only data loading changed (not algorithms)

3. **Feature 01 Consistency Check:**
   - Compare WinRateSimulationManager changes with AccuracySimulationManager
   - Verify shared patterns (array indexing, error handling)
   - Check for unintended interactions

4. **CSV vs JSON Comparison:**
   - How did CSV version handle projected vs actual?
   - Did CSV have separate files? (players_projected.csv vs players.csv)
   - Are we maintaining equivalent functionality?

**Documentation:**
- Spec.md "Cross-Epic Verification" section
- Checklist.md Phase F (items 22-25)
- Will execute during Stage 5cb (QC Round 2)

---

## What Success Looks Like

**This bug fix will be complete when:**

1. **Code Works:**
   - Accuracy calculation uses week_N for projections, week_N+1 for actuals
   - Week 17 uses week_18 for actuals
   - MAE values are realistic (3-8 range for QB)

2. **Tests Pass:**
   - All unit tests pass (2463/2463)
   - Integration tests verify realistic MAE
   - Smoke tests show >0% non-zero actuals (NOT "0 have non-zero")

3. **Statistical Validation:**
   - Zero percentage <90% ✓
   - Variance > 0 ✓
   - MAE in realistic range ✓
   - Critical questions answered ✓

4. **Cross-Epic Verification:**
   - Feature 01 tests still pass ✓
   - Epic notes requirements all met ✓
   - Original algorithms unchanged ✓

5. **Never Again:**
   - Will NEVER accept "(0 have non-zero points)" as PASS
   - Will ALWAYS manually inspect data BEFORE implementing
   - Will ALWAYS validate assumptions with evidence
   - Will ALWAYS re-read epic notes with fresh eyes

---

## Key Takeaways

1. **Empirical Validation is Mandatory**
   - NEVER trust assumptions
   - ALWAYS verify with actual code OR actual data
   - "It should work" ≠ "I verified it works"

2. **Statistical Sanity Checks Prevent Catastrophes**
   - "(0 have non-zero points)" should NEVER pass testing
   - Realistic value ranges are as important as structure
   - Ask: "Would this make sense in production?"

3. **Epic Notes are Source of Truth**
   - Spec.md can be wrong (this proves it)
   - Always trace back to original epic notes
   - Re-read with fresh eyes during each stage

4. **Hands-On Inspection Catches Assumptions**
   - Opening a Python REPL takes 30 seconds
   - Would have caught this bug immediately
   - Prevented days of wasted implementation

5. **"Assume Documents Are Wrong" Stages Are Critical**
   - Stage 2.5 (Spec Validation) would have caught this
   - Stage 5a.5 (Hands-On Data Inspection) would have caught this
   - These stages are now MANDATORY

---

## Post-Fix Action Items

**After bug fix complete:**

1. **Update Guides:**
   - Add Stage 2.5 guide (Spec Validation)
   - Add Stage 5a.5 guide (Hands-On Data Inspection)
   - Update smoke testing guide (statistical sanity checks)
   - Update QC Round 2 guide (output validation)

2. **Update Templates:**
   - spec.md template: Add "Assumption Validation Table"
   - checklist.md template: Add "Data Inspection" phase
   - smoke_test template: Add statistical validation code

3. **Document in Epic Lessons Learned:**
   - This bug fix as example of prevention strategies working
   - Before/after comparison (original spec vs bug fix spec)
   - Guide improvements catalog

4. **User Presentation:**
   - Show evidence of prevention strategies applied
   - Demonstrate hands-on data inspection
   - Present statistical sanity checks
   - Verify ALL epic changes against original notes

---

*This bug fix demonstrates that we learned from the catastrophic failure. Every principle from lessons_learned.md is applied here.*
