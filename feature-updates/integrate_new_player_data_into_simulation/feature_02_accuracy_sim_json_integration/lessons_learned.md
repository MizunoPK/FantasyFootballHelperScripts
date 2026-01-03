# Feature 02: Accuracy Simulation JSON Integration - Lessons Learned

**Purpose:** Document issues encountered and solutions for this feature

---

## Planning Phase Lessons (Stage 2)

### ✅ Lesson 1: Leverage Previous Feature Findings

**Approach:** Instead of re-investigating shared questions, leveraged Feature 1's findings
**Result:** All 7 questions answered immediately using Feature 1's CODEBASE_INVESTIGATION_FINDINGS.md
**Time saved:** Significant - avoided duplicate investigation of PlayerManager, FantasyPlayer, array indexing
**Key insight:** Cross-feature alignment starts early - reuse research when features share infrastructure

### ✅ Lesson 2: Simpler ≠ Less Important

**Discovery:** Feature 2 is simpler than Feature 1 (~40-50 LOC vs ~150 LOC)
**Reason:** Different use case (on-demand loading vs pre-loading/caching)
**Takeaway:** Simplicity doesn't mean less planning rigor - still requires full Stage 2 deep dive
**Impact:** Avoided assumption-based errors by following full protocol

### ✅ Lesson 3: Epic Requests May Include Validation Tasks

**Epic mentioned:** "Use week_17 folders for projected, week_18 for actual in week 17"
**Investigation found:** JSON arrays already handle this (projected_points[16], actual_points[16])
**Conclusion:** Epic was asking to VERIFY this works, not implement new logic
**Same for:** DEF/K evaluation - no special code needed, just validation during QC
**Lesson:** Distinguish between "implement new feature" vs "verify existing behavior"

### ✅ Lesson 4: Feature 1's Patterns Directly Applicable

**Reused from Feature 1:**
- Same player_data/ subfolder requirement
- Same array indexing (week_num - 1)
- Same field type handling (FantasyPlayer.from_json())
- Same error handling pattern (return None if missing)

**Not applicable:**
- JSON parsing method (Feature 2 doesn't need it - just file copying)
- Week data caching (Feature 2 loads on-demand)

**Lesson:** Identify which patterns transfer and which are use-case specific

### ✅ Lesson 5: Intentional Differences Are Valid

**Feature 1 approach:** Pre-load and cache all 17 weeks
**Feature 2 approach:** Load 1 week per evaluation

**Initially seemed inconsistent, but investigation showed:**
- Win Rate Sim runs thousands of iterations across all weeks → caching essential
- Accuracy Sim runs once per config per week → caching unnecessary overhead

**Lesson:** Document WHY implementations differ (intentional vs inconsistent)

---

## Implementation Phase Lessons

{Will be populated during Stage 5b implementation}

---

## Post-Implementation Lessons

### 🚨 CRITICAL LESSON: Data Loading ≠ Data Consumption

**Discovered:** Stage 5cb QC Round 3 (Skeptical Review)
**Severity:** HIGH - Feature would have been completely non-functional
**Status:** Caught before commit (QC process worked as designed)

#### What Went Wrong

**The Spec Said:**
> "AccuracyCalculator.py - No changes needed: PlayerManager abstracts data format"

**Fatal Assumption:** Changing how data is LOADED (CSV → JSON files) doesn't require changing how data is CONSUMED (accessing player attributes).

**Reality Check:**
- **Data Loading:** ✅ Changed correctly (copy 6 JSON files instead of 2 CSV files)
- **Data Consumption:** ❌ Missed completely (code still used `player.week_17_points` instead of `player.actual_points[16]`)

**Result:** Accuracy calculation would skip ALL players (hasattr returns False) → MAE = NaN/empty

#### Root Cause Analysis

**1. Incomplete Scope Definition (Stage 2)**

The spec identified FILES to change:
- ✅ AccuracySimulationManager.py (file loading methods)
- ✅ ParallelAccuracyRunner.py (file loading methods)
- ❌ **MISSED:** Same files need DATA ACCESS changes (lines 452-456)

**Fatal assumption:** "PlayerManager abstracts data format" meant zero downstream changes.

**What this actually meant:**
- PlayerManager handles JSON parsing ✅
- PlayerManager returns FantasyPlayer objects ✅
- **But:** FantasyPlayer's API changed (week_N_points → actual_points[N-1]) ❌

**The spec should have traced:** "How is player data consumed AFTER PlayerManager loads it?"

**2. Stage 5a Verification Missed It (24 iterations)**

The verification iterations focused on:
- ✅ File path changes (return week_folder)
- ✅ File structure changes (create player_data/)
- ✅ Integration points (caller uses .parent)
- ❌ **MISSING:** How downstream code accesses loaded player data

**Gap:** No iteration for "Trace data consumption from PlayerManager → AccuracyCalculator"

**3. Smoke Testing Verified Wrong Thing (Stage 5ca)**

Smoke testing checked:
- ✅ PlayerManager loads 100 QB players
- ✅ Data values are real (sum=332.8)
- ❌ **MISSED:** MAE calculation produces valid results (not NaN/empty)

**Gap:** Verified DATA LOADING but not END-TO-END CALCULATION

**4. Feature 1 Pattern Not Applied**

Feature 1 (Win Rate Sim) faced same issue:
- **Old:** CSV had single `fantasy_points` value per week
- **New:** JSON has `projected_points[week_num-1]` array
- **Solution:** Created `_parse_players_json()` to extract array values

Feature 2 should have recognized:
- **Old:** Player objects had `week_17_points` attribute
- **New:** Player objects have `actual_points[16]` array
- **Solution:** Update consumption code to use array indexing

**Gap:** No cross-feature pattern analysis ("Feature 1 changed consumption code, do we need similar?")

#### How It Survived Multiple Checks

| Stage | What Was Checked | What Was Missed |
|-------|------------------|-----------------|
| Stage 2 (Spec) | Files to modify for loading | **Data access pattern changes** |
| Stage 5a Round 1 (Iteration 1-7) | Requirements coverage, integration points | **Downstream consumption tracing** |
| Stage 5a Round 2 (Iteration 8-16) | Test strategy, edge cases | **End-to-end calculation verification** |
| Stage 5a Round 3 (Iteration 17-24) | Task ordering, success criteria | **Comparison with Feature 1 patterns** |
| Stage 5b (Implementation) | Checklist verification during coding | **Assumption that spec was complete** |
| Stage 5ca (Smoke Testing) | Data loading verification | **Full calculation pipeline execution** |
| Stage 5cb Round 1 (Basic) | Code structure, tests passing | **Runtime behavior with real data** |
| Stage 5cb Round 2 (Deep) | Baseline comparison, edge cases | **Actual vs expected output values** |
| **Stage 5cb Round 3 (Skeptical)** | **"What could still be broken?"** | **🎯 CAUGHT THE BUG** |

**Key Insight:** The bug survived 8+ verification stages because each checked STRUCTURE (files, paths, tests) but not SEMANTICS (does calculation produce correct output?).

#### Prevention Strategies

**1. Multi-Phase Research During Stage 2**

**Current:** Single deep dive focuses on "what files to change"

**Proposed:** Three research phases in Stage 2:

**Phase A: Data Loading Research**
- What files are loaded? (CSV → JSON)
- Where are they loaded from? (week folder)
- What format do they have? (6 position files, 17-element arrays)

**Phase B: Data Consumption Research**
- How is loaded data accessed in downstream code? (Grep for player.week_)
- What APIs changed? (week_N_points → actual_points[N-1])
- Where is this consumption happening? (AccuracySimulationManager lines 452-456)

**Phase C: Cross-Feature Pattern Analysis**
- What similar changes did related features make? (Feature 1 changed consumption code)
- Are there patterns to replicate? (_parse_players_json extracts array values)
- Are there patterns to avoid? (Different caching strategies)

**Checklist addition for Stage 2:**
```markdown
- [ ] Phase A: Data loading research complete (files, formats, locations)
- [ ] Phase B: Data consumption research complete (APIs, access patterns, call sites)
- [ ] Phase C: Cross-feature pattern analysis complete (similar features, reusable patterns)
- [ ] User clarification: Confirmed scope includes BOTH loading AND consumption changes
```

**2. Explicit User Scope Clarification**

**Current:** Spec assumes "change file loading" scope is clear

**Proposed:** Explicit user questions during Stage 2:

Example questions for THIS feature:
```markdown
## Scope Clarification Questions (ASK USER)

**Q1:** This epic mentions "load player data from JSON files". Does this include:
  - [ ] A) Only changing how files are loaded (file paths, file formats)
  - [ ] B) Changing how player data is accessed after loading (API changes)
  - [ ] C) Both A and B

**Q2:** I found that FantasyPlayer objects no longer have week_N_points attributes
      (changed to actual_points[N] arrays). The accuracy calculation code currently
      uses week_N_points. Should I:
  - [ ] A) Update accuracy calculation to use new array API
  - [ ] B) Keep existing code (assumes PlayerManager handles conversion)

**My recommendation:** Option A (update consumption code) - confirmed via Feature 1 investigation
```

**Benefit:** Forces agent to identify API changes and get user sign-off on scope

**3. Stage 5a Iteration Addition: "Downstream Consumption Tracing"**

**New Iteration (between current Iteration 5 and 6):**

```markdown
## Iteration 5a: Downstream Data Consumption Tracing

**Purpose:** Verify how loaded data is CONSUMED after PlayerManager returns it

**Process:**
1. Identify all locations where PlayerManager data is accessed
2. List OLD access patterns (attributes, methods, properties)
3. List NEW access patterns (how JSON-loaded data must be accessed)
4. Compare OLD vs NEW - identify breaking changes
5. Add tasks for consumption code updates if needed

**Example for Feature 02:**
- Location: AccuracySimulationManager.py lines 452-456
- Old pattern: `getattr(player, 'week_17_points')`
- New pattern: `player.actual_points[16]`
- Breaking change: YES - week_N_points no longer exist
- Action: ADD TASK to update consumption code

**Output:**
- List of consumption locations
- List of API changes (OLD → NEW)
- New tasks for consumption updates (if needed)
```

**4. Smoke Testing Must Verify END-TO-END**

**Current:** Smoke testing Part 3 verified "data loads successfully"

**Proposed:** Part 3 must verify "calculation produces valid output"

**For Feature 02, this means:**
```python
# Current (insufficient):
qb_data = player_mgr.get_all_players_by_position('QB')
print(f"Loaded {len(qb_data)} QB players")  # ✅ Checks data loading

# Required (end-to-end):
# Run FULL accuracy calculation for 1 config, 1 week
result = manager.evaluate_single_config(config_dict, season_path, week_range=(1,1))
mae = result.week_1_5.mae
print(f"MAE for week 1: {mae}")  # ✅ Checks calculation output
assert mae > 0 and mae < 20, f"Invalid MAE: {mae}"  # ✅ Validates correctness
```

**Rule:** Smoke testing must execute the FULL code path, not just data loading

**5. Cross-Feature Pattern Checklist**

**Add to Stage 5a Iteration 24 (Implementation Readiness):**

```markdown
### Cross-Feature Pattern Check

**For each completed related feature, verify:**
- [ ] Feature 1 scope: What did it change? (File loading AND consumption code)
- [ ] Feature 1 patterns: What code patterns were introduced? (_parse_players_json)
- [ ] Applicability: Do we need similar changes? (YES - consumption code updates)
- [ ] Documented: Added to TODO if applicable
```

**Benefit:** Ensures patterns from completed features are applied to current feature

#### Summary: The Two-Part Rule

**Rule:** When changing data format (CSV → JSON, SQL → NoSQL, etc.):

**Part 1: Data Loading** (what the spec caught)
- Change file paths, file formats, parsing logic
- Update how data enters the system

**Part 2: Data Consumption** (what the spec missed)
- Change how loaded data is accessed downstream
- Update APIs, attribute names, method calls

**Both parts are mandatory.** Changing only Part 1 creates non-functional code.

**Verification:** Smoke testing must run END-TO-END calculation, not just data loading.

**User Alignment:** Explicitly confirm scope includes BOTH parts during Stage 2.

---

### 🚨🚨 CATASTROPHIC LESSON: Week Offset Logic - Epic Reading Comprehension Failure

**Discovered During:** Stage 5cc Final Review (user caught it, not agent)
**Severity:** CATASTROPHIC - Feature completely non-functional (calculating MAE with all 0.0 actuals)
**Status:** NOT YET FIXED (discovered during final review)

#### What Went Wrong

**The Epic Request Said (Line 8):**
> "When running score_player calculations, it should use the week_17 folders to determine a projected_points of the player, then it should look at the actual_points array in week_18 folders to determine what the player actually scored in week 17"

**What The Epic ACTUALLY Meant:**
- For **ANY week N**: Load week_N folder for projections, week_N+1 folder for actuals
- Week 17 was just the **EXAMPLE** (week_17 for proj, week_18 for actual)
- This applies to **ALL weeks** (week_1 + week_2, week_2 + week_3, etc.)

**What I Incorrectly Interpreted:**
- "Week 17 is a special case that needs validation"
- "JSON arrays already contain both projected and actual in same folder"
- "No code changes needed, just verify it works"

**What Was Actually Implemented:**
```python
# BROKEN CODE:
for week_num in range(1, 17):
    load week_N folder  # Has projected_points[N-1] ✓
    use player.actual_points[N-1]  # Gets 0.0 from week_N folder ✗
```

**What Should Have Been Implemented:**
```python
# CORRECT CODE:
for week_num in range(1, 17):
    load week_N folder for projections  # projected_points[N-1] ✓
    load week_N+1 folder for actuals    # actual_points[N-1] ✓
```

**The Data Model:**
- **week_01 folder** (current_week=1): actual_points[0] = **0.0** (week 1 not complete yet)
- **week_02 folder** (current_week=2): actual_points[0] = **33.6** (week 1 complete)

**Impact:**
- Feature calculates MAE using projected vs 0.0 (completely invalid)
- Would produce nonsense accuracy measurements
- Completely defeats the purpose of accuracy simulation

#### The "0.0 Acceptance" Catastrophe

**Evidence that was VISIBLE but IGNORED:**

**Smoke Test Output:**
```
[PASS] 108/108 QB players have accessible week 1 data
      (0 have non-zero actual points)  ← 🚨 SHOULD HAVE BEEN RED FLAG
```

**Every stage saw this and accepted it:**
- ✅ Smoke test: Marked PASSED (treated "0 have non-zero" as informational)
- ✅ QC Round 2: "Verified in smoke testing" (blindly trusted)
- ✅ QC Round 3: "All players accessible" (checked accessibility, not correctness)

**What should have happened:**
1. See "(0 have non-zero actual points)"
2. **STOP IMMEDIATELY**
3. Ask: "Why are ALL actual points zero? This is statistically impossible."
4. Investigate: Compare week_01 vs week_02 data
5. Discover: week_02 has actual_points[0] = 33.6
6. Realize: Need to load week_N+1 for actuals

#### Root Cause Analysis: Why EVERY Stage Failed

**Stage 2 (Spec Creation) - READING COMPREHENSION FAILURE**

What should have happened:
- Read epic carefully: "week_17 folders for projected, week_18 folders for actual"
- Ask: "Why two different folders? Is this pattern general?"
- Investigate: Load week_01 and week_02, compare actual_points arrays
- Document: TWO-FOLDER loading requirement

What actually happened:
- Misread epic as "week 17 is a special case" ❌
- Assumed: "JSON arrays already have everything" ❌
- Never compared week folders ❌
- Wrote spec saying "NO code changes needed" ❌

**Failure mode:** Reading comprehension + insufficient data model investigation

---

**Stage 5a (TODO Creation - 24 Iterations) - SPEC TRUSTED AS GOSPEL**

What should have happened:
- Iteration 2: Trace data flow - "Where do actual points come from?"
- Iteration 5: Document week_N and week_N+1 loading requirement
- Question: "Epic mentions TWO folders - why is spec saying one folder?"

What actually happened:
- Accepted spec's conclusion without verification ❌
- Never questioned the data model ❌
- All 24 iterations validated spec internally, not against epic ❌

**Failure mode:** Spec treated as ground truth instead of hypothesis to validate

---

**Stage 5b (Implementation) - NO HANDS-ON VALIDATION**

What should have happened:
- Before coding: Manually test with Python REPL
  ```python
  import json
  week_01 = json.load(open('week_01/qb_data.json'))
  print(week_01[0]['actual_points'][0])  # See 0.0
  week_02 = json.load(open('week_02/qb_data.json'))
  print(week_02[0]['actual_points'][0])  # See 33.6
  ```
- Realize: "Oh, week_01 doesn't have week 1 actuals yet"
- Fix implementation before writing code

What actually happened:
- Followed spec blindly ❌
- Never manually inspected data ❌

**Failure mode:** No hands-on data validation before coding

---

**Stage 5ca (Smoke Testing) - CATASTROPHIC CRITICAL THINKING FAILURE**

**This is the WORST failure.** The output literally showed:

```
(0 have non-zero actual points)  ← IMPOSSIBLE DATA
```

What should have happened:
- See "0 have non-zero actual points"
- **IMMEDIATE RED FLAG**: "This is statistically impossible - ALL players scored 0.0?"
- Stop and investigate
- Discover week offset issue

What actually happened:
- Saw "108/108 players have accessible data" ✅
- **COMPLETELY IGNORED** "(0 have non-zero)" ❌
- Marked smoke test as PASSED ❌

**Failure mode:**
1. **Confirmation bias**: Looking for success, not failure
2. **No sanity checking**: Accepted impossible data as valid
3. **No critical thinking**: Should have questioned statistical impossibility

---

**Stage 5cb Rounds 1-2 (QC) - STRUCTURE OVER SEMANTICS**

What should have happened:
- Round 2 "Output Data Validation": Run actual MAE calculation
- See MAE values are nonsense (|projected - 0.0| = projected)
- Investigate why all actuals are 0.0

What actually happened:
- Checked code structure, not runtime output ❌
- Deferred to smoke testing without verification ❌

**Failure mode:** QC validated structure but not semantic correctness

---

**Stage 5cb Round 3 (Skeptical Review) - PARTIAL SUCCESS**

What happened:
- Caught first bug (data access pattern) ✅
- But never asked: "Where do actual points come from?" ❌
- Verified data is ACCESSIBLE, not CORRECT ❌

**Failure mode:** Fixed access but didn't validate data model

---

**User Discovery (Stage 5cc Final Review) - USER CAUGHT IT**

**The user asked the right question:**
> "Does it correctly use projected points from Week X's file, and actual points from Week X+1's file?"

**This is the question that should have been asked in:**
- Stage 2 (during spec creation)
- Stage 5a Iteration 5 (end-to-end data flow)
- Stage 5ca (during smoke testing when seeing 0.0 values)

**The user applied critical thinking that every stage failed to apply.**

---

#### Systemic Workflow Failures

**1. Spec Is Treated As Gospel**

**Problem:** Once spec is written (Stage 2), all subsequent stages trust it completely
- Stage 5a validates spec internally, not against epic
- Stage 5b implements spec without questioning
- Stage 5c tests against spec, not against reality

**Evidence:**
- Spec said "NO code changes needed"
- 24 iterations in Stage 5a never questioned this
- Implementation followed spec blindly

**Fix Needed:**
- **Stage 2.5: Spec Validation Stage** (NEW)
- Assume spec is COMPLETELY WRONG
- Re-read epic from scratch
- Compare spec claims to actual codebase/data
- Get user confirmation on any assumptions

---

**2. Smoke Testing Checks Wrong Thing**

**Problem:** Validates "data is accessible" not "data is CORRECT"

**Evidence:**
- "(0 have non-zero actual points)" was treated as informational
- Never questioned why ALL values are 0.0
- Marked PASSED because data was accessible

**Fix Needed:**
- Add **Data Sanity Checks** section to smoke testing guide
- Mandatory checks: "Does this data make statistical sense?"
- Red flag triggers: All zeros, all same value, all nulls
- Require investigation before marking PASSED

---

**3. No Statistical Sanity Validation**

**Problem:** Accepted statistically impossible data as valid

**Evidence:**
- ALL 108 QB players have 0.0 actual points (probability: 0%)
- ALL 213 RB players have 0.0 actual points (probability: 0%)
- This is IMPOSSIBLE in real data - should trigger alarm

**Fix Needed:**
- Add **Statistical Sanity Checks** to QC Round 2
- Check: Are values realistic? (fantasy points typically 0-50)
- Check: Is there variance? (not all same value)
- Check: Do aggregates make sense? (average QB score ~20, not 0)

---

**4. No Manual Data Inspection Requirement**

**Problem:** Never manually loaded data and inspected values before coding

**Evidence:**
- If I had loaded week_01 and week_02 in Python, would have immediately seen:
  ```python
  week_01[0]['actual_points'][0]  # 0.0
  week_02[0]['actual_points'][0]  # 33.6
  ```
- Would have realized week offset immediately

**Fix Needed:**
- **Stage 5a.5: Hands-On Data Inspection** (NEW)
- Before writing TODO, manually load and inspect data
- Document actual data values, not just structure
- Compare multiple weeks/files to understand patterns

---

**5. Confirmation Bias in Testing**

**Problem:** Looking for evidence of success, not evidence of failure

**Evidence:**
- Smoke test looked for: "Data accessible?" ✓
- Smoke test should have looked for: "Data WRONG?" ✗
- Saw "108/108 accessible" as success
- Ignored "0 non-zero" as failure

**Fix Needed:**
- Add **"What Would Failure Look Like?"** section to testing guides
- Before testing, list: "What values would indicate failure?"
- For this feature: "All 0.0 = FAILURE", "All same value = FAILURE"
- Test for failure cases explicitly

---

**6. No "Assume Documents Are Wrong" Stage**

**Problem:** No stage exists to systematically validate previous work

**What's needed:**
- After Stage 2 (Spec): **Stage 2.5 - Spec Validation** (assume spec is wrong)
- After Stage 5a (TODO): **Stage 5a.5 - TODO Validation** (assume TODO is wrong)
- Method: Re-read epic, ignore all documents, rebuild understanding from scratch

**Process:**
1. Hide existing spec.md
2. Re-read epic notes from scratch
3. Re-investigate codebase from scratch
4. Rebuild mental model independently
5. Compare with spec.md
6. Document discrepancies
7. Get user to resolve discrepancies

---

#### Prevention Strategies (Specific & Actionable)

**1. Add Stage 2.5: Spec Validation (Assume Spec Is Wrong)**

**Location:** Insert between Stage 2 and Stage 3

**Process:**
```markdown
## Stage 2.5: Spec Validation

**Premise:** Assume spec.md is COMPLETELY WRONG

**Steps:**
1. Close spec.md (don't reference it)
2. Re-read epic notes from scratch
3. For EACH claim in notes:
   - Investigate codebase independently
   - Document finding
   - Note if it contradicts spec
4. Re-open spec.md
5. Compare findings with spec
6. Document ALL discrepancies
7. If discrepancies found:
   - Ask user to clarify
   - Update spec.md
   - Re-run Stage 2.5

**Specific Checks:**
- [ ] Every epic requirement has corresponding spec section
- [ ] Every spec claim verified against actual code
- [ ] Every assumption tested with hands-on data inspection
- [ ] No "this seems obvious" shortcuts taken

**Example for THIS feature:**
- Epic says: "week_17 folders for projected, week_18 folders for actual"
- Investigation: Load week_01 and week_02, compare actual_points
- Finding: week_01 has 0.0, week_02 has real values
- Conclusion: Must load week_N+1 for actuals (applies to ALL weeks)
- Spec check: Does spec.md document TWO-FOLDER loading? NO ← Discrepancy found
- Action: Update spec.md before proceeding
```

---

**2. Add Stage 5a.5: Hands-On Data Inspection (Before TODO)**

**Location:** After Stage 5a Round 3, before implementation

**Process:**
```markdown
## Stage 5a.5: Hands-On Data Inspection

**Premise:** Spec understanding != Reality

**Requirements:**
1. Open Python REPL
2. Manually load relevant data files
3. Print actual values (not just check "exists")
4. Document realistic value ranges
5. Compare multiple files/weeks
6. Verify assumptions from spec

**For JSON integration features:**
```python
import json
from pathlib import Path

# Load multiple weeks to understand pattern
week_01 = json.load(open('simulation/sim_data/2025/weeks/week_01/qb_data.json'))
week_02 = json.load(open('simulation/sim_data/2025/weeks/week_02/qb_data.json'))

# Print ACTUAL values
print("Week 1 folder - actual_points[0]:", week_01[0]['actual_points'][0])
print("Week 2 folder - actual_points[0]:", week_02[0]['actual_points'][0])

# Document finding
# Finding: week_01 has 0.0, week_02 has real values
# Conclusion: Week N folder doesn't have week N actuals yet
# Implication: Must load week_N+1 for actuals
```

**Checklist:**
- [ ] Loaded real data files (not test fixtures)
- [ ] Printed actual values (not just checked existence)
- [ ] Compared multiple files/weeks
- [ ] Documented value ranges (min, max, typical)
- [ ] Verified spec assumptions against real data
- [ ] Updated TODO if findings contradict spec
```

---

**3. Update Smoke Testing Guide: Add Data Sanity Checks**

**File:** `STAGE_5ca_smoke_testing_guide.md`

**Add new section:**
```markdown
### Part 3b: Data Sanity Validation (MANDATORY)

**Run AFTER Part 3 (E2E Execution)**

**Purpose:** Verify data values are REALISTIC, not just accessible

**Checks:**

1. **Zero/Null Check**
   - [ ] Count how many values are 0.0 or null
   - [ ] If >50% are zero/null → INVESTIGATE (likely bug)
   - [ ] If >90% are zero/null → STOP AND FIX (definitely bug)

2. **Variance Check**
   - [ ] Calculate stddev of values
   - [ ] If stddev = 0 (all same value) → INVESTIGATE
   - [ ] Real data should have variance

3. **Range Check**
   - [ ] Check min, max, mean values
   - [ ] Compare to expected ranges (e.g., fantasy points: 0-50)
   - [ ] If outside realistic range → INVESTIGATE

4. **Statistical Impossibility Check**
   - [ ] Ask: "Is this data statistically possible?"
   - [ ] Examples of impossible data:
     - All players same score (probability ≈ 0%)
     - All players score 0.0 (probability ≈ 0%)
     - All players same exact projection (probability ≈ 0%)

**Example Code:**
```python
import statistics

values = [p['actual_points'][0] for p in player_data]

# Count zeros
zero_count = sum(1 for v in values if v == 0.0 or v is None)
zero_pct = (zero_count / len(values)) * 100

print(f"Zeros: {zero_count}/{len(values)} ({zero_pct:.1f}%)")

if zero_pct > 90:
    print("🚨 CRITICAL: >90% zeros - THIS IS A BUG")
    return False

# Check variance
if len(values) > 1:
    stddev = statistics.stdev(values)
    if stddev == 0:
        print("🚨 CRITICAL: All values identical - THIS IS A BUG")
        return False

# Check range
min_val, max_val = min(values), max(values)
mean_val = statistics.mean(values)
print(f"Range: {min_val} - {max_val}, Mean: {mean_val:.1f}")

# Sanity check for fantasy points
if mean_val < 5 or mean_val > 100:
    print(f"⚠️ WARNING: Mean {mean_val} outside typical range (5-50)")
```

**Red Flag Triggers:**
- >90% of values are zero → STOP AND FIX
- All values identical → STOP AND FIX
- Mean outside realistic range → INVESTIGATE
- No variance in data → INVESTIGATE
```

---

**4. Update QC Round 2 Guide: Add Statistical Validation**

**File:** `STAGE_5cb_qc_rounds_guide.md`

**Add to Round 2 checklist:**
```markdown
### Iteration X: Statistical Output Validation (NEW)

**Purpose:** Verify output values are statistically realistic

**Checklist:**
- [ ] Run feature with real data
- [ ] Collect output values (MAE, scores, projections, etc.)
- [ ] Calculate statistics: min, max, mean, median, stddev
- [ ] Compare to expected ranges:
  - MAE for fantasy: typically 3-8 points
  - Fantasy scores: typically 5-50 points
  - Projections: typically 10-30 points
- [ ] Check for statistical impossibilities:
  - All same value (variance = 0)
  - All zeros (unless explicitly expected)
  - Outliers beyond 3 standard deviations
- [ ] Document realistic value ranges in code_changes.md

**Example:**
```python
mae_values = [3.2, 4.5, 5.1, 3.8, 4.2]  # Sample MAE values
mean_mae = statistics.mean(mae_values)  # 4.16

# Sanity check
if mean_mae < 1.0:
    print("🚨 MAE too low - projections too perfect (likely bug)")
if mean_mae > 15.0:
    print("🚨 MAE too high - projections terrible (likely bug)")
if 3.0 <= mean_mae <= 8.0:
    print("✓ MAE in realistic range")
```

**Pass Criteria:**
- Output values within expected statistical ranges
- Data has realistic variance (not all same)
- No statistical impossibilities
- Aggregates make sense (averages, sums, counts)
```

---

**5. Add "Assume Wrong" Validation Iterations**

**Update guides to add validation iterations that assume previous work is wrong:**

**Stage 5a Round 3 - Add New Iteration:**
```markdown
## Iteration 25: Spec Re-Validation (Assume Spec Is Wrong)

**When:** After Iteration 24 (Implementation Readiness), before GO decision

**Premise:** Assume spec.md contains fundamental errors

**Process:**
1. Re-read epic notes (ignore spec.md)
2. For each epic requirement:
   - What does it ACTUALLY say?
   - What does spec.md say?
   - Do they match EXACTLY?
3. For each spec assumption:
   - How was this verified?
   - Was real data inspected?
   - Could this be wrong?
4. Compare findings with spec.md
5. Document ALL discrepancies (even minor)

**Discrepancy Resolution:**

**IF ANY DISCREPANCIES FOUND:**

1. **STOP IMMEDIATELY** - Do not proceed to implementation
2. **Report to User:**
   - List ALL discrepancies found (epic vs spec)
   - Explain the impact of each discrepancy
   - Show what was wrong in spec.md
   - Show what epic actually requires
3. **Ask User How to Proceed:**
   ```
   I found [X] discrepancies between the epic and the spec during Iteration 25:

   Discrepancy 1: [Description]
   - Epic says: [Quote from epic]
   - Spec says: [Quote from spec]
   - Impact: [What this means for implementation]

   [Repeat for each discrepancy]

   These discrepancies suggest the spec.md and potentially the TODO.md
   may be fundamentally incorrect.

   How would you like to proceed?
   A) Update spec.md to match epic, then restart TODO iterations (Iteration 1-24) from the beginning
   B) Update spec.md and TODO.md, then continue to implementation (risky - TODO may be wrong)
   C) Discuss the discrepancies first before deciding

   My recommendation: Option A (restart TODO iterations after fixing spec)
   Reason: If the spec is wrong, the 24 TODO iterations validated the wrong requirements.
   ```

4. **Wait for User Decision** - Do NOT make this choice autonomously
5. **Execute User's Choice:**
   - If restart: Update spec.md, then go back to Stage 5a Iteration 1
   - If continue: Update spec.md and TODO.md, document risk, proceed
   - If discuss: Have conversation with user about each discrepancy

**Pass Criteria:**
- Zero discrepancies between epic and spec, OR
- User has been informed of ALL discrepancies and chosen path forward
- All assumptions verified with real data
- User confirmed any ambiguous interpretations
```

---

**6. Add Critical Questions Checklist**

**Add to multiple stages:**

```markdown
## Critical Questions (Answer Before Proceeding)

**Stage 2 (Spec Creation):**
- [ ] Did I read the ENTIRE epic request word-for-word?
- [ ] Did I manually inspect actual data files?
- [ ] Did I compare multiple data files to understand patterns?
- [ ] Did I test every assumption with hands-on code?
- [ ] Would a new agent reading this spec make the same implementation?

**Stage 5a (TODO Creation):**
- [ ] Did I verify spec claims against actual code?
- [ ] Did I load real data and inspect values?
- [ ] Did I question every "obvious" assumption?
- [ ] Would this TODO produce correct output?

**Stage 5ca (Smoke Testing):**
- [ ] Are the output values statistically realistic?
- [ ] If I saw these values in production, would I be suspicious?
- [ ] Did I check for impossible data (all zeros, no variance)?
- [ ] Does the data make common sense?

**Stage 5cb Round 3 (Skeptical Review):**
- [ ] What would make this feature completely wrong?
- [ ] What data would indicate total failure?
- [ ] Am I looking at actual values or just structure?
- [ ] Would I ship this to production confidently?
```

---

#### Summary: The Three-Part Failure

**Part 1: Reading Comprehension (Stage 2)**
- Epic said: week_N + week_N+1 (using week 17 as example)
- I read: week 17 is special case only
- **Fix:** Stage 2.5 re-validates epic understanding

**Part 2: Data Model Investigation (Stage 2 & 5a)**
- Never compared week_01 vs week_02 data
- Never manually loaded and inspected actual values
- **Fix:** Stage 5a.5 requires hands-on data inspection

**Part 3: Critical Thinking (Stage 5ca & 5cb)**
- Saw "0 have non-zero actual points"
- Accepted as valid instead of questioning
- **Fix:** Data sanity checks + statistical validation

**All three failures must be prevented:**
1. Better reading comprehension validation
2. Mandatory hands-on data inspection
3. Statistical sanity checks in testing

---

## Patterns to Reuse

**For future JSON integration features:**
1. Always check how data is created/written first (compile_historical_data.py)
2. Leverage PlayerManager's existing JSON handling (don't reinvent)
3. Rely on FantasyPlayer.from_json() for validation and type conversion
4. player_data/ subfolder is MANDATORY for PlayerManager compatibility
5. Array indexing: index 0 = Week 1, index N-1 = Week N
6. Distinguish "implement new logic" from "verify existing behavior" in epic requests
7. **CRITICAL:** For time-series data, verify which folder contains which time period's data
8. **CRITICAL:** Never accept "all zeros" as valid - investigate immediately
9. **CRITICAL:** Manually inspect data before coding - load real files, print real values
10. **CRITICAL:** Question every "obvious" assumption - test it with real data
