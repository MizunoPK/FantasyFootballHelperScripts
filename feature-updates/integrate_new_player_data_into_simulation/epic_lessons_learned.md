# Epic: integrate_new_player_data_into_simulation - Lessons Learned

**Purpose:** Document cross-feature patterns and systemic insights from this epic

---

## Planning Phase Lessons (Stages 1-4)

{Will be populated during Stages 1-4}

## Implementation Phase Lessons (Stage 5)

### 🚨 CRITICAL: The Two-Part Rule for Data Format Changes

**Discovered During:** Feature 02, Stage 5cb QC Round 3
**Impact:** HIGH - Would have resulted in completely non-functional feature
**Caught By:** Skeptical review questioning "what could still be broken?"

**The Problem:**
When changing data formats (CSV → JSON, SQL → NoSQL, etc.), there are TWO distinct parts:
1. **Data Loading** - How data enters the system (file paths, parsing, storage)
2. **Data Consumption** - How loaded data is accessed downstream (APIs, attributes, methods)

**What Happened:**
- Feature 02 spec identified Part 1 (change file loading) ✅
- Feature 02 spec missed Part 2 (change data access patterns) ❌
- Code loaded JSON correctly but tried accessing data via old attributes
- Result: All players skipped, MAE = NaN/empty (feature completely broken)

**Why It Was Missed:**
- Spec assumed "PlayerManager abstracts data format" meant no downstream changes
- Reality: PlayerManager abstracts *file format*, but FantasyPlayer *API* changed
- Old: `player.week_17_points` attribute
- New: `player.actual_points[16]` array index
- Stage 2 didn't trace how data is consumed after loading
- Stage 5a didn't verify downstream consumption patterns
- Smoke testing verified data loading but not end-to-end calculation

**Prevention:** See Feature 02 lessons_learned.md for detailed prevention strategies

**Key Takeaways:**
1. **Stage 2 must have 3 research phases:** Loading, Consumption, Cross-Feature Patterns
2. **User must confirm scope:** "Does this include API/consumption changes?"
3. **Stage 5a needs new iteration:** "Downstream Consumption Tracing"
4. **Smoke testing must be end-to-end:** Verify calculation output, not just data loading
5. **Cross-feature pattern analysis:** If Feature 1 updated consumption, we probably need to also

**Workflow Improvements Proposed:**
- Stage 2: Add mandatory 3-phase research checklist
- Stage 2: Add mandatory user scope clarification questions
- Stage 5a: Add Iteration 5a "Downstream Consumption Tracing"
- Stage 5a: Add cross-feature pattern check to Iteration 24
- Stage 5ca: Update smoke testing requirements (Part 3 must verify output values)

**See:** `feature_02_accuracy_sim_json_integration/lessons_learned.md` (lines 66-293) for complete analysis

---

### 🚨🚨 CATASTROPHIC: The Week Offset Logic Bug (Second Critical Failure)

**Discovered During:** Feature 02, Stage 5cc (Final Review) - caught by user questioning
**Impact:** CRITICAL - Feature completely non-functional, calculating MAE with all 0.0 actual points
**Caught By:** User asking critical question that ALL 7 stages failed to catch
**Previous Stages That Failed:** Stage 2, Stage 5a (all 24 iterations), Stage 5b, Stage 5ca, Stage 5cb (all 3 rounds)

**The Bug:**
```python
# CURRENT (BROKEN):
for week_num in range(1, 17):
    projected_path, actual_path = self._load_season_data(season_path, week_num)
    # BOTH return week_num folder
    player.actual_points[week_num - 1]  # Gets 0.0 from week_num folder!

# CORRECT (NEEDED):
for week_num in range(1, 17):
    projected_path = load week_num folder      # For projections ✓
    actual_path = load week_num+1 folder       # For actuals ✓
    # Use actual_points[week_num-1] from week_num+1 folder
```

**The Data Model (Why week_num folder has 0.0):**
- Each week_N folder represents data "as of" week N's start
- week_N folder contains actual_points for weeks 1 to N-1 (not N)
- Week N hasn't completed yet when week_N folder is created
- Week N's actuals appear in week_N+1 folder

**Evidence:**
- week_01 QB actual_points[0] = 0.0 (week 1 not complete yet)
- week_02 QB actual_points[0] = 33.6 (week 1 now complete)

**Epic Explicitly Called This Out:**
From `integrate_new_player_data_into_simulation_notes.txt` line 8:
> "When running score_player calculations, it should use the week_17 folders to determine a projected_points of the player, then it should look at the actual_points array in week_18 folders to determine what the player actually scored in week 17"

**This was NOT a subtle requirement** - it was explicitly stated in the epic request.

---

### Why This Was Catastrophic (The "0.0 Acceptance" Failure)

**Stage 2 Failure (Spec Creation):**
- I misinterpreted epic line 8 as "week 17 is a special case"
- Should have realized: "week_17 + week_18" example implies ALL weeks use week_N + week_N+1
- Wrote in spec: "NO special handling needed - arrays contain all data"
- Failed to investigate the actual data model (json_exporter.py)
- Failed to manually inspect data files to verify assumptions

**Stage 5a Failure (TODO Creation - 24 Iterations):**
- ALL 24 iterations trusted spec.md as gospel truth
- Never questioned "no special handling needed" claim
- Never re-read epic notes to verify spec interpretation
- Never investigated how week folders are actually structured
- Iteration 23a (Pre-Implementation Spec Audit) checked spec completeness, not correctness

**Stage 5b Failure (Implementation):**
- Followed spec exactly (which was wrong)
- No hands-on data inspection before coding
- Never opened a Python REPL to manually load and inspect data
- Never printed actual values from week_01 vs week_02 files

**Stage 5ca Failure (Smoke Testing) - THE MOST CATASTROPHIC:**
- Smoke test OUTPUT showed: "(0 have non-zero actual points)"
- **I marked this as PASSED**
- This is statistically impossible for NFL data (players score points every week)
- Confirmation bias: looked for "data is accessible" not "data is realistic"
- No statistical sanity checking (variance, range, zero percentage)

**Stage 5cb Round 1 Failure (Basic Validation):**
- Checked data structures exist (actual_points array) ✓
- Never checked what VALUES are in those arrays
- Structure validation ≠ semantic validation

**Stage 5cb Round 2 Failure (Deep Verification):**
- Checked >95% test coverage ✓
- Never questioned if tests verify the right thing
- Tests verified data access, not data correctness

**Stage 5cb Round 3 Failure (Skeptical Review):**
- Fixed data consumption bug (week_N_points → actual_points[N-1]) ✓
- Never questioned if week_N folder is the right data source
- Fixed HOW we access data, not WHICH data we access

**User Discovery (Stage 5cc):**
- User asked: "does it correctly use projected points from Week X's file, and actual points from Week X+1's file?"
- This is the question EVERY stage should have asked and answered
- User's feedback: "it is unacceptable that this was allowed to pass through"

---

### Systemic Root Causes

**1. Spec Treated as Gospel (Stage 5a+)**
- Once spec.md is created, all subsequent stages trust it completely
- No "assume spec is wrong and validate" stage exists
- 24 verification iterations never questioned spec correctness

**2. No Hands-On Data Inspection Requirement**
- Never required to manually load data in Python REPL
- Never required to print actual values before coding
- All validation was abstract/theoretical, not empirical

**3. Smoke Testing Checks Wrong Thing**
- Verified data is accessible (structure)
- Never verified data is realistic (semantics)
- "(0 have non-zero points)" was treated as acceptable

**4. No Statistical Sanity Validation**
- No checks for impossible data patterns (all zeros, no variance)
- No checks for realistic value ranges
- No "would this make sense in production?" questions

**5. Confirmation Bias in Testing**
- Looked for evidence of success ("data loads")
- Never looked for evidence of failure ("are these values possible?")
- Acceptance criteria biased toward passing

**6. No "Assume Documents Are Wrong" Stage**
- Epic notes → spec.md → todo.md → code
- Each step trusts previous step completely
- No stage exists that goes back to original source with fresh eyes

---

### Prevention Strategies (Detailed in Feature Lessons Learned)

See `feature_02_accuracy_sim_json_integration/lessons_learned.md` lines 604-890 for complete details:

**Strategy 1: Stage 2.5 - Spec Validation**
- NEW STAGE after Stage 2
- Close spec.md, re-read epic notes from scratch
- Investigate codebase independently for each claim
- Compare findings with spec, document ALL discrepancies

**Strategy 2: Stage 5a.5 - Hands-On Data Inspection**
- NEW STAGE after Stage 5a (after TODO, before implementation)
- Open Python REPL, manually load data files
- Print actual values (not just check "exists")
- Verify assumptions with real data

**Strategy 3: Data Sanity Checks in Smoke Testing**
- Add statistical validation to Part 3 (E2E test)
- Check zero percentage (>90% → fail)
- Check variance (stddev = 0 → fail)
- Check value ranges (unrealistic → fail)

**Strategy 4: Statistical Validation in QC Round 2**
- Add output validation iteration
- Run calculations, verify realistic results
- MAE too low (<1.0) or too high (>15.0) → investigate
- Compare with historical data if available

**Strategy 5: Iteration 25 - Spec Re-Validation**
- NEW ITERATION in Stage 5a Round 3
- Re-read epic notes (ignore spec.md)
- For each epic requirement, verify spec matches EXACTLY
- Document discrepancies, update spec if needed

**Strategy 6: Critical Questions Checklists**
- Add to each stage guide
- Stage 2: "Did I verify this claim with code/data?"
- Stage 5a: "Does this contradict any epic requirements?"
- Stage 5ca: "Are these values statistically realistic?"
- Stage 5cb: "If I saw this in production, would I be suspicious?"

---

### Impact Assessment

**Feature Status:** COMPLETELY NON-FUNCTIONAL
- All accuracy calculations use 0.0 for actual points
- MAE calculations meaningless (comparing projections to zeros)
- Would produce garbage output in production

**Workflow Status:** FUNDAMENTALLY BROKEN
- 7 stages executed (Stage 2, 5a, 5b, 5ca, 5cb R1-3)
- All 7 failed to catch an explicitly-stated requirement
- User caught it by asking a basic verification question

**Trust in Process:** SEVERELY DAMAGED
- Can't trust spec.md (Stage 2 misinterpretation)
- Can't trust TODO (Stage 5a based on bad spec)
- Can't trust implementation (Stage 5b followed bad TODO)
- Can't trust smoke testing (Stage 5ca accepted impossible data)
- Can't trust QC rounds (Stage 5cb R1-3 checked wrong thing)

**Required Actions:**
1. Fix week offset logic bug immediately
2. RESTART from Stage 5ca (per QC Restart Protocol)
3. Update ALL guides with 6 prevention strategies
4. Implement Stage 2.5 and Stage 5a.5 as mandatory stages
5. Never allow "0 have non-zero points" to pass testing again

**See:** `feature_02_accuracy_sim_json_integration/lessons_learned.md` (lines 296-930) for complete post-mortem

## QC Phase Lessons (Stage 6)

{Will be populated during Stage 6 epic final QC}

## Guide Improvements Identified

{Track guide gaps/improvements discovered during this epic}

| Guide File | Issue | Proposed Fix | Status | Bug Source |
|------------|-------|--------------|--------|------------|
| **FIRST CRITICAL BUG (Data Consumption Pattern)** | | | | |
| STAGE_2_feature_deep_dive_guide.md | No guidance on tracing downstream data consumption | Add 3-phase research requirement: (A) Data Loading, (B) Data Consumption, (C) Cross-Feature Patterns | Pending | Bug #1 |
| STAGE_2_feature_deep_dive_guide.md | No requirement to ask user about scope clarification | Add mandatory user questions: "Does scope include API changes?" with examples | Pending | Bug #1 |
| STAGE_5aa_round1_guide.md | No iteration for downstream consumption tracing | Add Iteration 5a "Downstream Consumption Tracing" between current 5 and 6 | Pending | Bug #1 |
| STAGE_5ac_round3_guide.md | No cross-feature pattern analysis in Iteration 24 | Add checklist: "Compare with completed features, identify applicable patterns" | Pending | Bug #1 |
| STAGE_5ca_smoke_testing_guide.md | Part 3 only requires "data loads successfully" | Update to require "end-to-end calculation produces valid output values" | Pending | Bug #1 |
| templates_v2.md | checklist.md template missing consumption tracing | Add Phase B checklist items for data consumption research | Pending | Bug #1 |
| templates_v2.md | spec.md template missing consumption section | Add "Data Consumption Changes" section after "Data Loading Changes" | Pending | Bug #1 |
| **SECOND CRITICAL BUG (Week Offset Logic - "0.0 Acceptance" Catastrophe)** | | | | |
| **NEW:** STAGE_2.5_spec_validation_guide.md | No stage exists to validate spec.md against original sources | CREATE NEW STAGE: Assume spec is wrong, re-read epic notes, investigate codebase independently, document discrepancies. MANDATORY after Stage 2. | Pending | Bug #2 |
| **NEW:** STAGE_5a.5_hands_on_data_inspection_guide.md | No requirement for empirical data validation before coding | CREATE NEW STAGE: Open Python REPL, manually load data files, print actual values, verify assumptions. MANDATORY after Stage 5a, before Stage 5b. | Pending | Bug #2 |
| STAGE_2_feature_deep_dive_guide.md | No requirement to manually inspect data files during research | Add mandatory step: "Open data files, print sample values, verify claims empirically" | Pending | Bug #2 |
| STAGE_2_feature_deep_dive_guide.md | Spec claims not validated against actual data/code | Add checklist: "For EACH claim in spec, did I verify with code OR data (not just documentation/assumptions)?" | Pending | Bug #2 |
| STAGE_5aa_round1_guide.md | No iteration to re-validate spec against epic notes | Add checklist to Iteration 4a (TODO Spec Audit): "Does todo.md match EPIC NOTES (not just spec.md)?" | Pending | Bug #2 |
| STAGE_5ac_round3_guide.md | Iteration 23a checks spec completeness, not correctness | **ADD ITERATION 25: Spec Re-Validation** - Re-read epic notes, verify spec matches EXACTLY, update spec if discrepancies found | Pending | Bug #2 |
| STAGE_5ac_round3_guide.md | No guidance on when to update spec during Round 3 | Add protocol: If Iteration 25 finds discrepancies, update spec.md AND todo.md before Iteration 24 (GO/NO-GO) | Pending | Bug #2 |
| STAGE_5ca_smoke_testing_guide.md | No statistical sanity validation in Part 3 | Add **MANDATORY** data sanity checks: zero percentage (>90% → FAIL), variance (stddev=0 → FAIL), realistic ranges | Pending | Bug #2 |
| STAGE_5ca_smoke_testing_guide.md | Acceptance criteria biased toward passing | Add critical question: "If I saw these values in production, would I be suspicious?" Must ask BEFORE marking PASS | Pending | Bug #2 |
| STAGE_5ca_smoke_testing_guide.md | No guidance on what makes data "realistic" | Add domain-specific sanity check examples: NFL (MAE 3-8, some non-zero points), Finance (no negative prices), etc. | Pending | Bug #2 |
| STAGE_5cb_qc_rounds_guide.md (Round 2) | No iteration for output validation with real calculations | Add iteration between 15-16: "Output Validation" - Run actual calculations, verify realistic results (e.g., MAE in 3-8 range) | Pending | Bug #2 |
| STAGE_5cb_qc_rounds_guide.md (Round 2) | No statistical validation of calculation results | Add checklist: "Are output values statistically realistic? (check ranges, variance, zero percentage)" | Pending | Bug #2 |
| STAGE_5cb_qc_rounds_guide.md (Round 3) | Skeptical review doesn't include "data source" questions | Add critical question: "Are we loading data from the RIGHT source? (not just accessing it correctly)" | Pending | Bug #2 |
| STAGE_5cb_qc_rounds_guide.md (Round 3) | No guidance on distinguishing "access" vs "source" bugs | Add example: "player.actual_points[0] accesses correctly ✓, but week_01 folder has 0.0 (wrong source) ✗" | Pending | Bug #2 |
| STAGE_5ca_smoke_testing_guide.md | "(0 have non-zero points)" was accepted as PASS | Add **EXPLICIT RULE**: Any message containing "0 have non-zero" or "all values are 0.0" is an **AUTOMATIC FAIL** | Pending | Bug #2 |
| STAGE_5cb_qc_rounds_guide.md (All Rounds) | No critical questions checklist per round | Add "Critical Questions" section to each round with domain-specific skeptical questions | Pending | Bug #2 |
| prompts_reference_v2.md | No prompt for Stage 2.5 (new stage) | Add phase transition prompt for Stage 2.5 (Spec Validation) | Pending | Bug #2 |
| prompts_reference_v2.md | No prompt for Stage 5a.5 (new stage) | Add phase transition prompt for Stage 5a.5 (Hands-On Data Inspection) | Pending | Bug #2 |
| templates_v2.md | spec.md template has no "Assumptions Validation" section | Add section: "Assumptions Validation" with table: Assumption / How Verified / Evidence (code/data reference) | Pending | Bug #2 |
| templates_v2.md | checklist.md template doesn't track data inspection | Add Phase: "Data Inspection" with items: Opened data files? Printed values? Verified assumptions? | Pending | Bug #2 |
| EPIC_WORKFLOW_USAGE.md | Doesn't mention Stage 2.5 or 5a.5 in workflow overview | Update workflow diagram and stage descriptions to include new mandatory stages | Pending | Bug #2 |
| PLAN.md | Workflow specification doesn't include validation stages | Update Stage 2 and Stage 5 specifications to include new substages (2.5, 5a.5) | Pending | Bug #2 |
| CLAUDE.md | Quick reference doesn't mention new stages | Update "Stage 5: Feature Implementation" section to list 5a→5a.5→5b→5ca→5cb→5cc→5d→5e | Pending | Bug #2 |
