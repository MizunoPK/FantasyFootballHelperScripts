# S9: Epic-Level Final QC
## S9.P2: Epic QC Rounds

**Purpose:** Validate the epic as a cohesive whole through 3 systematic quality checks focusing on cross-feature integration and epic-wide consistency.

**File:** `s9_p2_epic_qc_rounds.md`

**Stage Flow Context:**
```text
S9.P1 (Epic Smoke Testing) →
→ [YOU ARE HERE: S9.P2 - Epic QC Rounds] →
→ S9.P3 (User Testing) → S9.P4 (Epic Final Review) → S10
```

---


## Table of Contents

1. [S9.P2: Epic QC Rounds](#s9p2-epic-qc-rounds)
2. [🚨 MANDATORY READING PROTOCOL](#-mandatory-reading-protocol)
3. [Overview](#overview)
4. [🛑 Critical Rules (Epic-Specific)](#-critical-rules-epic-specific)
5. [Prerequisites Checklist](#prerequisites-checklist)
6. [Workflow Overview](#workflow-overview)
7. [QC Round 1: Cross-Feature Integration](#qc-round-1-cross-feature-integration)
8. [Integration Points (example from test plan)](#integration-points-example-from-test-plan)
9. [QC Round 2: Epic Cohesion & Consistency](#qc-round-2-epic-cohesion--consistency)
10. [QC Round 3: End-to-End Success Criteria](#qc-round-3-end-to-end-success-criteria)
11. [Original Epic Request (example)](#original-epic-request-example)
12. [Epic Success Criteria (example from S4)](#epic-success-criteria-example-from-s4)
13. [Epic Issue Handling Protocol](#epic-issue-handling-protocol)
14. [Issues Found in S9.P2 QC](#issues-found-in-s9p2-qc)
15. [🛑 MANDATORY CHECKPOINT 1](#-mandatory-checkpoint-1)
16. [Next Steps](#next-steps)
17. [Summary](#summary)
18. [Exit Criteria](#exit-criteria)

---
## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Epic QC Rounds, you MUST:**

1. **Read the QC rounds pattern:** `reference/qc_rounds_pattern.md`
   - Understand universal 3-round QC workflow
   - Review critical rules that apply to ALL QC rounds
   - Study restart protocol and common mistakes

2. **Use the phase transition prompt** from `prompts/s9_prompts.md`
   - Find "Starting S9: Epic Final QC" prompt (covers both 6a and 6b)
   - Acknowledge requirements
   - List critical requirements from this guide

3. **Update EPIC_README.md Agent Status** with:
   - Current Phase: S9.P2 - Epic QC Rounds
   - Current Guide: `stages/s9/s9_p2_epic_qc_rounds.md`
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "3 rounds MANDATORY", "If critical issues → RESTART S6", "Minor issues can be fixed inline"
   - Next Action: QC Round 1 - Cross-Feature Integration

4. **Verify all prerequisites** (see checklist below)

5. **THEN AND ONLY THEN** begin epic QC rounds

**This is NOT optional.** Reading both the pattern and this guide ensures epic-wide validation.

---

## Overview

**What is this guide?**
Epic-level QC Rounds validate the epic as a cohesive whole through 3 systematic quality checks: Cross-Feature Integration (Round 1), Epic Cohesion & Consistency (Round 2), and End-to-End Success Criteria (Round 3). Unlike feature-level QC (S10.P2), these rounds focus on epic-wide patterns and architectural consistency. See `reference/qc_rounds_pattern.md` for universal workflow.

**When do you use this guide?**
- After STAGE_6a complete (Epic Smoke Testing passed)
- Ready to perform deep QC validation on epic
- All cross-feature integration verified at basic level

**Key Outputs:**
- ✅ QC Round 1 complete (cross-feature integration validated)
- ✅ QC Round 2 complete (epic cohesion and consistency verified)
- ✅ QC Round 3 complete (success criteria met, original goals achieved)
- ✅ All findings documented in epic_lessons_learned.md
- ✅ Any issues fixed or bug fixes created

**Time Estimate:**
30-60 minutes (10-20 minutes per round)

**Exit Condition:**
Epic QC Rounds are complete when all 3 rounds pass with zero critical issues, all findings documented, and epic validated against original request

---

## 🛑 Critical Rules (Epic-Specific)

**📖 See `reference/qc_rounds_pattern.md` for universal critical rules.**

**Epic-specific rules for S9.P2:**

```text
┌─────────────────────────────────────────────────────────────┐
│ EPIC-SPECIFIC RULES - Add to EPIC_README Agent Status       │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ Epic Issue Handling (Different from feature-level)
   - Critical issues → Follow epic debugging protocol → RESTART S6
   - Minor issues → Fix immediately, document, continue (no restart)
   - Epic issues go to: epic_name/debugging/ISSUES_CHECKLIST.md

2. ⚠️ QC RESTART PROTOCOL (Epic-specific)
   - If Round 1: Critical integration issues → RESTART from S6
   - If Round 2: Critical consistency issues → RESTART from S6
   - If Round 3: Critical success criteria failures → RESTART from S6
   - Minor issues: Fix inline, document, continue
   - Restart destination: S6 (Epic Smoke Testing)

3. ⚠️ Focus on EPIC-LEVEL validation (not feature-level)
   - Feature-level QC done in S10.P2
   - Epic-level focuses on: Integration, consistency, cohesion
   - Compare ACROSS ALL features (not individual features)

4. ⚠️ Document findings for EACH round
   - Update epic_lessons_learned.md after each round
   - Include: Issues found, fixes applied, status
   - Serves as evidence of thorough QC
```

**Universal rules (from pattern file):**
- All 3 rounds mandatory
- Each round has unique focus
- Verify DATA VALUES (not just structure)
- Re-reading checkpoints mandatory
- See `reference/qc_rounds_pattern.md` for complete list

---

## Prerequisites Checklist

**Before starting Epic QC Rounds (STAGE_6b), verify:**

**STAGE_6a complete:**
- [ ] Epic smoke testing PASSED (all 4 parts)
- [ ] Epic smoke test results documented
- [ ] No smoke testing failures

**Epic smoke test plan executed:**
- [ ] All import tests passed
- [ ] All entry point tests passed
- [ ] All E2E execution tests passed with DATA VALUES verified
- [ ] All cross-feature integration tests passed

**Agent Status updated:**
- [ ] EPIC_README.md shows STAGE_6a complete
- [ ] Current guide: stages/s9/s9_p2_epic_qc_rounds.md

**Original epic request available:**
- [ ] Have access to {epic_name}.txt
- [ ] Can reference original goals for Round 3

**If any prerequisite fails:**
- ❌ Do NOT start Epic QC Rounds
- Return to STAGE_6a to complete smoke testing
- Verify all prerequisites met before proceeding

---

## Workflow Overview

**📖 See `reference/qc_rounds_pattern.md` for universal workflow details.**

**Epic-specific workflow for S9.P2:**

```text
┌─────────────────────────────────────────────────────────────┐
│           EPIC-LEVEL QC ROUNDS (3 Rounds)                   │
└─────────────────────────────────────────────────────────────┘

Round 1: Cross-Feature Integration (10-20 min)
   ↓ Integration points, data flow, interface compatibility
   ↓ Pass: Zero critical integration issues
   ↓
   If PASS → Round 2
   If CRITICAL ISSUES → Fix, RESTART from S6

Round 2: Epic Cohesion & Consistency (10-20 min)
   ↓ Code style, naming, error handling, architectural patterns
   ↓ Pass: Zero critical consistency issues
   ↓
   If PASS → Round 3
   If CRITICAL ISSUES → Fix, RESTART from S6
   If MINOR ISSUES → Fix inline, continue

Round 3: End-to-End Success Criteria (10-20 min)
   ↓ Validate against original epic request
   ↓ Verify epic success criteria met
   ↓ Pass: All criteria met
   ↓
   If PASS → Epic QC complete, proceed to S9.P3
   If CRITICAL FAILURES → Fix, RESTART from S6
```

---

## QC Round 1: Cross-Feature Integration

**📖 See `reference/qc_rounds_pattern.md` for universal Round 1 patterns.**
**📖 See `reference/validation_loop_qc_pr.md` for Validation Loop QC approach.**

**Objective:** Validate integration points between features work correctly.

**Validation Loop Approach:**
- **Assume everything is wrong:** Skeptically analyze all features together
- **Fresh eyes:** Sequential reading (feature by feature integration)
- **Integration focus:** Test feature interactions
- **No deferred issues:** ALL issues across ALL features must be fixed before Round 2
- **Exit criteria:** Zero critical integration issues

**Time Estimate:** 10-20 minutes

**Pass Criteria:** Zero critical integration issues

---

### Validation 1.1: Integration Point Validation

**Review integration points identified in S4 epic_smoke_test_plan.md:**

**Find integration points section:**
```markdown
## Integration Points (example from test plan)
1. Feature 01 (PlayerDataManager) → Feature 02 (RatingSystem)
   - Data flow: Player objects with ADP → Rating system
   - Interface: get_all_players() returns List[Player]

2. Feature 02 (RatingSystem) → Feature 03 (RecommendationEngine)
   - Data flow: Rated players → Recommendation generation
   - Interface: get_rated_players() returns List[RatedPlayer]
```

**For EACH integration point, verify:**

```python
# Integration Test: Feature 01 → Feature 02
from feature_01.PlayerDataManager import PlayerDataManager
from feature_02.RatingSystem import RatingSystem

# Get data from Feature 01
player_mgr = PlayerDataManager()
players = player_mgr.get_all_players()

# Verify data format
assert len(players) > 0, "Feature 01 returned no data"
assert hasattr(players[0], 'adp'), "Players missing ADP field"

# Pass to Feature 02
rating_sys = RatingSystem()
rated_players = rating_sys.apply_ratings(players)

# Verify integration works
assert len(rated_players) == len(players), "Data lost in integration"
assert all(hasattr(p, 'rating') for p in rated_players), "Ratings not applied"

print("✅ Feature 01 → Feature 02 integration validated")
```

**Check ALL integration points** (not just one example)

---

### Validation 1.2: Data Flow Across Features

**Verify data flows correctly through feature chain:**

```python
# Complete data flow: Feature 01 → 02 → 03
from feature_01.PlayerDataManager import PlayerDataManager
from feature_02.RatingSystem import RatingSystem
from feature_03.RecommendationEngine import RecommendationEngine

# Step 1: Get raw data
players = PlayerDataManager().get_all_players()

# Step 2: Apply ratings
rated_players = RatingSystem().apply_ratings(players)

# Step 3: Generate recommendations
recommendations = RecommendationEngine().generate(rated_players)

# Verify complete flow
assert len(recommendations) > 0, "No recommendations generated"
assert recommendations[0]['player_name'] in [p.name for p in players], "Lost player data"
assert 'rating' in recommendations[0], "Lost rating data"
assert 'draft_position' in recommendations[0], "Missing final output"

print("✅ Complete data flow validated")
```

---

### Validation 1.3: Interface Compatibility

**Verify features use compatible interfaces:**

```python
# Check Feature 02 accepts Feature 01's output format
from feature_01.PlayerDataManager import Player
from feature_02.RatingSystem import RatingSystem

# Create sample player (Feature 01 format)
sample_player = Player(name="Test", position="QB", adp=50.0)

# Verify Feature 02 can process it
rating_sys = RatingSystem()
result = rating_sys.rate_player(sample_player)

assert result is not None, "Feature 02 rejected Feature 01 format"
assert hasattr(result, 'rating'), "Feature 02 didn't add rating"

print("✅ Interface compatibility verified")
```

---

### Validation 1.4: Error Propagation Handling

**Test error handling at integration boundaries:**

```python
# Test error propagates correctly
from feature_02.RatingSystem import RatingSystem

try:
    invalid_data = None
    RatingSystem().apply_ratings(invalid_data)
    assert False, "Should have raised error for invalid data"
except ValueError as e:
    assert "Invalid player data" in str(e), "Error message unclear"
    print("✅ Error propagation works")
```

---

### Round 1 Checkpoint

**Count critical integration issues:**

**Critical integration issues:**
- Integration point fails (data doesn't flow)
- Interface incompatibilities (type mismatches)
- Data loss during integration
- Error propagation failures

**Minor issues (can fix inline):**
- Suboptimal error messages
- Missing validation at boundaries
- Documentation gaps

**If Round 1 has CRITICAL issues:**
1. Document ALL critical issues
2. Follow epic debugging protocol
3. **RESTART from S6 (epic smoke testing)**

**If Round 1 has only MINOR issues:**
- Fix immediately
- Document in epic_lessons_learned.md
- Continue to Round 2

**If Round 1 has ZERO issues:**
- Document clean pass in epic_lessons_learned.md
- Proceed to Round 2

---

## QC Round 2: Epic Cohesion & Consistency

**📖 See `reference/qc_rounds_pattern.md` for universal Round 2 patterns.**
**📖 See `reference/validation_loop_qc_pr.md` for Validation Loop QC approach.**

**Objective:** Validate epic cohesion and consistency across all features.

**Validation Loop Approach:**
- **Different patterns than Round 1:** Reverse order (last feature to first)
- **Cross-feature focus:** Verify integration points AND consistency
- **No deferred issues:** ALL new issues must be fixed before Round 3
- **Exit criteria:** Zero critical consistency issues

**Time Estimate:** 10-20 minutes

**Pass Criteria:** Zero critical consistency issues

---

### Validation 2.1: Code Style Consistency

**Check code style is consistent across ALL features:**

**Sample files from each feature:**
```python
# Feature 01 sample
from feature_01.PlayerDataManager import PlayerDataManager

# Feature 02 sample
from feature_02.RatingSystem import RatingSystem

# Feature 03 sample
from feature_03.RecommendationEngine import RecommendationEngine
```

**Check consistency:**
- ✅ Import style consistent (absolute vs relative)
- ✅ Naming conventions consistent (snake_case, PascalCase)
- ✅ Docstring style consistent (Google style)
- ✅ Error handling style consistent (custom exceptions vs standard)

**If inconsistencies found:**
- **Critical:** Core architectural inconsistencies → RESTART
- **Minor:** Naming/style variations → Fix inline, document

---

### Validation 2.2: Naming Convention Consistency

**Check naming is consistent across features:**

```python
# Check method naming patterns
# All features should use similar naming for similar operations

# Feature 01: get_all_players()
# Feature 02: get_rated_players()  ✅ Consistent "get_XXX_players()" pattern
# Feature 03: get_recommendations()  ❌ Different pattern

# If different, decide:
# - Critical (confusing, breaks expectations) → RESTART
# - Minor (just different, still clear) → Document, accept
```

---

### Validation 2.3: Error Handling Consistency

**Check error handling is consistent:**

```python
# Do all features use same error handling approach?

# Feature 01
try:
    data = load_data()
except FileNotFoundError:
    raise DataProcessingError("Player data file not found")

# Feature 02
try:
    config = load_config()
except FileNotFoundError:
    raise DataProcessingError("Rating config not found")  # ✅ Consistent

# Feature 03
try:
    settings = load_settings()
except FileNotFoundError:
    return None  # ❌ Different (returns None vs raises error)
```

**Verify:**
- ✅ All features use same error hierarchy
- ✅ Error messages follow same format
- ✅ Error handling at boundaries is consistent

---

### Validation 2.4: Architectural Pattern Consistency

**Check architectural patterns are consistent:**

**Design patterns used:**
- Feature 01: Manager pattern (PlayerDataManager)
- Feature 02: System pattern (RatingSystem)
- Feature 03: Engine pattern (RecommendationEngine)

**Verify:**
- ✅ Patterns are compatible
- ✅ No conflicting architectural approaches
- ✅ Feature boundaries clear and consistent

---

### Round 2 Checkpoint

**Count consistency issues:**

**Critical consistency issues:**
- Conflicting architectural patterns
- Incompatible error handling
- Major naming inconsistencies that confuse

**Minor issues:**
- Style variations
- Minor naming differences
- Documentation format variations

**If Round 2 has CRITICAL issues:**
1. Document ALL critical issues
2. Follow epic debugging protocol
3. **RESTART from S6**

**If Round 2 has MINOR issues:**
- Fix immediately
- Document in epic_lessons_learned.md
- Continue to Round 3

**If Round 2 has ZERO issues:**
- Document clean pass
- Proceed to Round 3

---

## QC Round 3: End-to-End Success Criteria

**📖 See `reference/qc_rounds_pattern.md` for universal Round 3 patterns.**
**📖 See `reference/validation_loop_qc_pr.md` for Validation Loop QC approach.**

**Objective:** Validate epic meets all success criteria and original goals.

**Validation Loop Approach:**
- **Final validation:** Random spot-checks and thematic review
- **Requirement:** ZERO issues across entire epic
- **Exit criteria:** 3 consecutive clean rounds (epic is defect-free)
- **If ANY issues found:** Fix ALL immediately, restart from S9.P1 (epic smoke testing)

**Time Estimate:** 10-20 minutes

**Pass Criteria:** All success criteria met, original goals achieved

---

### Validation 3.1: Validate Against Original Epic Request

**Re-read ORIGINAL {epic_name}.txt:**

Close any current views → Open {epic_name}.txt → Read fresh

**For EACH goal in original request, verify:**

```markdown
## Original Epic Request (example)

User Goal 1: "Integrate ADP data into draft recommendations"
✅ Verified: Feature 01 fetches ADP, Feature 02 applies ratings, Feature 03 uses in recs

User Goal 2: "Allow users to adjust rating multipliers"
✅ Verified: Feature 02 includes multiplier config, Feature 03 respects adjustments

User Goal 3: "Generate top 200 ranked players"
✅ Verified: Feature 03 outputs exactly 200 ranked players
```

**If ANY goal not met:**
- Critical → Create bug fix, RESTART S6
- Can't be met → Get user approval to remove from scope

---

### Validation 3.2: Verify Epic Success Criteria

**From S4 epic_smoke_test_plan.md, check success criteria:**

```markdown
## Epic Success Criteria (example from S4)

1. All 6 positions have rating multipliers (QB, RB, WR, TE, K, DST)
   ✅ Verified: All 6 position files have multipliers

2. Recommendations include player name, position, ADP, rating, draft position
   ✅ Verified: All fields present in output

3. Top player in each position has rating > 0.8
   ✅ Verified: QB top=0.92, RB top=0.88, WR top=0.90, TE top=0.85, K top=0.82, DST top=0.87
```

**All criteria must be met 100%**

---

### Validation 3.3: User Experience Flow Validation

**Execute complete user workflow end-to-end:**

```bash
# Simulated user workflow
python run_script.py --fetch-player-data  # Feature 01
python run_script.py --apply-ratings      # Feature 02
python run_script.py --generate-recs      # Feature 03

# Verify smooth experience
# - No confusing errors
# - Clear progress indicators
# - Expected output files created
# - Help text accurate
```

---

### Validation 3.4: Performance Characteristics

**Check epic meets performance expectations:**

```python
import time

# Time complete workflow
start = time.time()

# Run epic workflow
run_complete_workflow()

elapsed = time.time() - start

# Verify acceptable performance
assert elapsed < 60.0, f"Epic workflow too slow: {elapsed}s (expected <60s)"

print(f"✅ Epic workflow completed in {elapsed:.2f}s")
```

---

### Round 3 Checkpoint

**Verify ALL success criteria:**

**If ANY success criteria not met:**
- Document which criteria failed
- Determine if critical (can't achieve epic goals)
- If critical → Create bug fixes, RESTART S6
- If acceptable → Get user approval, document

**If ALL criteria met:**
- ✅ Epic QC Rounds COMPLETE
- ✅ Document completion in EPIC_README.md
- ✅ Update epic_lessons_learned.md
- ✅ Update Agent Status: "Epic QC Rounds COMPLETE"
- ✅ Proceed to **Step 6: User Testing & Bug Fix Protocol**

---

## Epic Issue Handling Protocol

**If critical issues found during QC rounds:**

### Step 1: Create Epic Debugging Folder

```markdown
epic_name/debugging/ISSUES_CHECKLIST.md

## Issues Found in S9.P2 QC

- [ ] Issue 1: Feature 02 → Feature 03 integration fails with large datasets
- [ ] Issue 2: Inconsistent error handling in Feature 01 vs Feature 03
```

### Step 2: Enter Debugging Protocol

See `debugging/debugging_protocol.md` for complete protocol

### Step 3: After ALL Issues Resolved

**RESTART S6 (Epic Smoke Testing) from Step 1:**
- Re-run ALL 4 smoke test parts
- Verify fixes didn't break anything
- Return to S9.P2 after smoke testing passes

**Critical:** Loop back to Epic Smoke (NOT back to QC round), ensures clean validation

---

## 🛑 MANDATORY CHECKPOINT 1

**You have completed all 3 Epic QC rounds**

⚠️ STOP - DO NOT PROCEED TO S9.P3 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Critical Rules" section of this guide
2. [ ] Use Read tool to re-read `reference/qc_rounds_pattern.md` (ALL Critical Rules)
3. [ ] Use Read tool to re-read original epic request ({epic_name}.txt)
4. [ ] Verify ALL success criteria met from original epic request
5. [ ] Update epic_lessons_learned.md with QC findings
6. [ ] Update EPIC_README.md Agent Status:
   - Current Guide: "stages/s9/s9_p3_user_testing.md"
   - Current Step: "S9.P2 complete (3/3 rounds passed), ready to start S9.P3"
   - Last Updated: [timestamp]
7. [ ] Output acknowledgment: "✅ CHECKPOINT 1 COMPLETE: Re-read Critical Rules and original request, verified all success criteria met"

**Why this checkpoint exists:**
- 90% of agents skip re-reading original epic request
- Missing original success criteria causes 60% of user rejections
- 5 minutes of re-reading prevents days of epic rework

**ONLY after completing ALL 7 actions above, proceed to Next Steps section**

---

## Next Steps

**If ALL 3 rounds PASSED:**
- ✅ Document epic QC results in EPIC_README.md
- ✅ Update Agent Status: "Epic QC Rounds COMPLETE (3/3 rounds passed)"
- ✅ Update epic_lessons_learned.md with QC findings
- ✅ Proceed to **Step 6: User Testing & Bug Fix Protocol**

**If ANY round had CRITICAL issues:**
- ❌ Fix ALL critical issues
- ❌ Follow epic debugging protocol
- ❌ **RESTART from S6 (epic smoke testing)**
- ❌ Re-run smoke testing → QC Round 1 → QC Round 2 → QC Round 3
- ❌ Do NOT proceed to PR Review until clean pass

---

## Summary

**Epic-Level QC Rounds validate:**
- Round 1: Cross-feature integration (do features work together?)
- Round 2: Epic cohesion & consistency (is epic architecturally sound?)
- Round 3: End-to-end success criteria (does epic achieve goals?)

**Key Differences from Feature-Level:**
- Focus on epic-wide patterns (not individual features)
- Minor issues can be fixed inline (epic-level more flexible)
- Critical issues require epic debugging protocol
- Restart destination: S6 (epic smoke testing)
- Validation against original epic request (Round 3)

**Critical Success Factors:**
- All 3 rounds mandatory
- Focus on integration and consistency (not individual features)
- Minor vs critical issue classification
- Epic debugging protocol for critical issues
- Validation against original user goals

**📖 For universal patterns and detailed validation techniques, see:**
`reference/qc_rounds_pattern.md`


## Exit Criteria

**Epic QC Rounds (S9.P2) is complete when ALL of these are true:**

- [ ] All steps in this phase complete as specified
- [ ] Agent Status updated with phase completion
- [ ] Ready to proceed to next phase

**If any criterion unchecked:** Complete missing items before proceeding

---
---

**END OF STAGE 6b GUIDE**
