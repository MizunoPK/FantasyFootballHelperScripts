# S8: Post-Feature Alignment
## S8.P2: Epic Testing Plan Reassessment

**File:** `s8_p2_epic_testing_update.md`

**Purpose:** After completing a feature, update the epic_smoke_test_plan.md to reflect ACTUAL implementation discoveries, add integration points found during development, and keep the testing strategy current as the epic evolves.

**Stage Flow Context:**
```text
S5 (Implementation Planning) → S6 (Implementation Execution) → S7 (Testing & Review) →
→ S8.P1 (Cross-Feature Alignment) →
→ [YOU ARE HERE: S8.P2 - Testing Plan Update] →
→ Next Feature's S5 (or S9 if all features done)
```

---

## Table of Contents

1. [MANDATORY READING PROTOCOL](#mandatory-reading-protocol)
2. [Overview](#overview)
3. [Critical Rules](#critical-rules)
4. [Critical Decisions Summary](#critical-decisions-summary)
5. [Prerequisites Checklist](#prerequisites-checklist)
6. [Workflow Overview](#workflow-overview)
7. [Quick Navigation](#quick-navigation)
8. [Detailed Workflow](#detailed-workflow)
9. [MANDATORY CHECKPOINT 1](#mandatory-checkpoint-1)
10. [Commit Message Template](#commit-message-template)
11. [Exit Criteria](#exit-criteria)
12. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
13. [README Agent Status Update Requirements](#readme-agent-status-update-requirements)
14. [Prerequisites for Next Stage](#prerequisites-for-next-stage)
15. [Summary](#summary)

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Testing Plan Update, you MUST:**

1. **Use the phase transition prompt** from `prompts_reference_v2.md`
   - Find "Starting S8.P2" prompt
   - Speak it out loud (acknowledge requirements)
   - List critical requirements from this guide

2. **Update README Agent Status** with:
   - Current Phase: TESTING_PLAN_UPDATE
   - Current Guide: stages/s8/s8_p2_epic_testing_update.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "Update based on ACTUAL implementation", "Add discovered integration points", "Keep plan current"
   - Next Action: Review epic_smoke_test_plan.md and just-completed feature code

3. **Verify all prerequisites** (see checklist below)

4. **THEN AND ONLY THEN** begin Testing Plan Update workflow

**This is NOT optional.** Reading this guide ensures the test plan stays current and accurate.

---

## Overview

**What is this guide?**
Post-Feature Testing Update is where you update epic_smoke_test_plan.md based on ACTUAL implementation discoveries (not specs), adding integration points found during development and ensuring test scenarios reflect real behavior.

**When do you use this guide?**
- S8.P1 (Cross-Feature Alignment) complete (Cross-Feature Alignment updated)
- Feature implementation is complete and validated
- Ready to update epic testing strategy

**Key Outputs:**
- ✅ epic_smoke_test_plan.md updated with actual implementation insights
- ✅ Integration points discovered during development added
- ✅ Test scenarios reflect actual behavior (not assumed from specs)
- ✅ Update history documents changes and rationale
- ✅ Ready for next feature's S5 (or S9 if all features done)

**Time Estimate:**
15-30 minutes per completed feature

**Exit Condition:**
Testing Plan Update is complete when epic_smoke_test_plan.md reflects actual implementation (not specs), new integration points are added, test scenarios are updated, and changes are documented in update history

---

## Critical Rules

```text
1. UPDATE BASED ON ACTUAL IMPLEMENTATION (Not specs)
   - Read the ACTUAL CODE that was written
   - Don't rely on specs or TODO list
   - Verify actual interfaces, data structures, behaviors
   - Test plan must reflect reality, not plans

2. IDENTIFY INTEGRATION POINTS DISCOVERED
   - Look for cross-feature interactions implementation revealed
   - Identify dependencies specs didn't predict
   - Note data flows between features
   - Document edge cases discovered during implementation

3. ADD SPECIFIC TEST SCENARIOS (Not vague categories)
   - Bad: "Test feature integration"
   - Good: "Test that PlayerManager.calculate_score() applies ADP multiplier to final score"
   - Include WHAT to test, HOW to verify, EXPECTED result

4. UPDATE EXISTING SCENARIOS (Don't just append)
   - If implementation contradicts existing scenario → update it
   - If behavior more complex than assumed → expand scenario
   - Remove scenarios that don't apply anymore
   - Keep test plan internally consistent

5. FOCUS ON EPIC-LEVEL TESTING (Not feature unit tests)
   - Feature unit tests covered in S7 (Testing & Review)
   - This is about EPIC-LEVEL integration testing
   - Test cross-feature workflows
   - Test epic success criteria

6. DOCUMENT UPDATE RATIONALE
   - Add notes explaining WHY test added
   - Reference feature that drove update
   - Link to actual code locations if relevant
   - Update history table with changes

7. KEEP PLAN EXECUTABLE
   - Test scenarios should be runnable during S9
   - Include commands/steps to execute tests
   - Specify expected outputs
   - Make plan actionable, not aspirational

8. PRESERVE STAGE 1 AND 4 UPDATES
   - Don't delete original test categories from S1
   - Don't remove test scenarios added in S4
   - ADD to the plan (don't replace it)
   - Evolution builds on previous stages

9. COMMIT TEST PLAN UPDATES
   - Update epic_smoke_test_plan.md
   - Commit changes with descriptive message
   - Include feature name in commit message
   - Keep git history clear

10. SHORT BUT THOROUGH
    - This stage should take 15-30 minutes
    - Focus on significant insights
    - Don't overthink minor details
    - But don't skip if no obvious changes
```

---

## Critical Decisions Summary

**S8.P2 (Epic Testing Update) has 1 major decision point:**

### Decision Point 1: Testing Plan Update Scope (ADD/UPDATE/NO CHANGE)
**Question:** After reviewing actual implementation, what level of test plan changes are needed?

**Classification criteria:**

**Option A: NO CHANGE**
- Feature implementation matched test plan expectations
- No new integration points discovered
- No edge cases found that weren't predicted
- Test plan scenarios still accurate
- **Action:** Update epic_smoke_test_plan.md Update History table only
- Note: "{feature_name} reviewed - no test plan changes needed"
- ✅ Proceed to next feature or S9

**Option B: MINOR ADDITIONS (add specific scenarios)**
- Implementation revealed new integration points
- Edge cases discovered that should be tested
- Cross-feature interactions found during development
- Examples:
  - "ADP multiplier applies to scoring calculation"
  - "Missing ADP data defaults to neutral multiplier (1.0)"
  - "Integration with ConfigManager for threshold values"
- **Action:**
  - Add specific test scenarios to epic_smoke_test_plan.md
  - Update based on ACTUAL code (reference file:line)
  - Include WHAT/HOW/EXPECTED for each scenario
  - Update Update History table with additions
- ✅ Proceed to next feature or S9

**Option C: MAJOR UPDATES (rewrite test scenarios)**
- Implementation significantly different from assumptions
- Multiple existing scenarios now inaccurate
- Need to restructure test plan sections
- Examples:
  - Feature uses different data flow than assumed
  - Integration pattern changed during implementation
  - Epic success criteria need adjustment
- **Action:**
  - Rewrite affected test scenarios
  - Remove obsolete scenarios
  - Add new scenarios for actual behavior
  - Update Update History table with major changes
  - Consider if epic success criteria still accurate
- ✅ Proceed to next feature or S9

**Impact:** Outdated test plans lead to S9 failures. Updating test plan NOW (based on actual implementation) ensures S9 tests the right things.

---

**Summary of Testing Plan Update:**
- Review ACTUAL implementation code (not specs/TODOs)
- Identify new integration points discovered during development
- Add/update test scenarios to reflect reality
- Document update rationale in Update History table
- Keep test plan executable and specific

---

## Prerequisites Checklist

**Verify these BEFORE starting Testing Plan Update:**

**From S8.P1:**
- [ ] S8.P1 (Cross-Feature Alignment) completed
- [ ] All remaining feature specs reviewed and updated
- [ ] Feature-level work complete for this feature

**Epic Files:**
- [ ] epic_smoke_test_plan.md exists
- [ ] Last updated timestamp visible
- [ ] Update history table exists

**Code Availability:**
- [ ] Just-completed feature code committed to git
- [ ] Can read actual implementation
- [ ] Integration points visible in code

**If ANY prerequisite not met:** Complete missing items before starting S8.P2 (Epic Testing Update)

---

## Workflow Overview

```bash
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: REVIEW ACTUAL IMPLEMENTATION                       │
│   - Read code from just-completed feature                  │
│   - Identify actual interfaces created                     │
│   - Note actual data structures used                       │
│   - Find integration points with other features            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: COMPARE TO CURRENT TEST PLAN                       │
│   - Read epic_smoke_test_plan.md                           │
│   - Identify gaps (implementation vs plan)                 │
│   - Find scenarios that need updating                      │
│   - Note new integration points to add                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: UPDATE TEST PLAN                                   │
│   - Add new test scenarios                                 │
│   - Update existing scenarios if needed                    │
│   - Add integration point tests                            │
│   - Update "Last Updated" timestamp                        │
│   - Add entry to Update History table                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: FINAL VERIFICATION                                 │
│   - Test plan still coherent                               │
│   - All scenarios executable                               │
│   - Update history complete                                │
│   - Commit changes to git                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Navigation

**S8.P2 (Epic Testing Update) has 4 main steps. Jump to any step:**

| Step | Focus Area | Go To |
|------|-----------|-------|
| **Step 1** | Review Actual Implementation | [Step 1](#step-1-review-actual-implementation) |
| **Step 2** | Identify Testing Gaps | [Step 2](#step-2-identify-testing-gaps) |
| **Step 3** | Add/Update Test Scenarios | [Step 3](#step-3-addupdate-test-scenarios) |
| **Step 4** | Document & Commit | [Step 4](#step-4-document-update-rationale-and-commit) |

**Key Decision Points:**

| Decision | Description | Go To |
|----------|-------------|-------|
| **Update Scope** | NO CHANGE / MINOR / MAJOR | [Critical Decisions](#critical-decisions-summary) |
| **Integration Points** | New cross-feature interactions | [Integration Points Examples](#integration-points-found-in-feature_01_adp_integration) |
| **Edge Cases** | Discovered during implementation | [Edge Cases Examples](#edge-cases-discovered-in-implementation) |

**Reference Sections:**

| Section | Description | Go To |
|---------|-------------|-------|
| Critical Rules | Must-follow testing update rules | [Critical Rules](#critical-rules) |
| Prerequisites | What must be done first | [Prerequisites Checklist](#prerequisites-checklist) |
| Update History | How to document changes | [Update History](#update-history) |

**Tip:** This stage is quick (15-30 minutes). Focus on significant insights from actual implementation, not minor details.

---

## Detailed Workflow

### STEP 1: Review Actual Implementation

**Purpose:** Understand what was ACTUALLY implemented (not what specs said)

**Actions:**

1. **Read feature implementation code:**
   - Main files modified (from feature README.md "Files Modified" section)
   - Integration points (method calls to other features)
   - Data structures added/modified
   - Configuration keys added

2. **Identify integration points discovered during implementation:**
   ```markdown
   ## Integration Points Found
   
   **Feature:** feature_01_adp_integration
   
   1. **PlayerManager.calculate_total_score()**
      - Discovery: Now multiplies score by adp_multiplier
      - Impact: Affects all modes that calculate scores
      - Source: league_helper/util/PlayerManager.py:145-167
   
   2. **ConfigManager.load_league_config()**
      - Discovery: Loads adp_multiplier_ranges from config
      - Impact: Config validation must include ADP keys
      - Source: league_helper/util/ConfigManager.py:89-103
   ```

3. **Note edge cases discovered:**
   - Behaviors not in spec but found during testing
   - Error handling added during implementation
   - Performance considerations discovered

4. **Compare implementation to spec:**
   - What's different from spec?
   - What's more complex than expected?
   - What's simpler than expected?

**Output:** Integration points list + edge cases list

**Time:** 5-10 minutes

---


**Purpose:** Identify what's missing or outdated in current test plan

---

#### 2a. Read Current epic_smoke_test_plan.md

**Actions:**
1. Open epic_smoke_test_plan.md
2. Read existing test scenarios
3. Note what S4 assumptions were
4. Check if implementation matches assumptions

---

#### 2b. Identify Gaps

**Questions to ask:**

**Gap Type 1: New Integration Points**
- Q: Does current plan test integration points discovered during implementation?
- Example: "Plan tests feature_01 in isolation, but doesn't test PlayerManager → ConfigManager integration"

**Gap Type 2: Behavioral Discoveries**
- Q: Does plan test edge cases discovered during implementation?
- Example: "Plan assumes ADP always present, doesn't test missing ADP behavior"

**Gap Type 3: Cross-Feature Workflows**
- Q: Does plan test workflows that span multiple features?
- Example: "Plan tests ADP in isolation, doesn't test combined ADP + Rating workflow (future)"

**Gap Type 4: Data Dependencies**
- Q: Does plan test data files and formats?
- Example: "Plan doesn't verify adp_data.csv format matches what code expects"

**Gap Type 5: Configuration**
- Q: Does plan test configuration keys and defaults?
- Example: "Plan doesn't test fallback behavior when config key missing"

---

#### 2c. Create Update List

**Template:**
```markdown
## Test Plan Updates Needed (After feature_01_adp_integration)

**Add New Scenarios:**
1. Test PlayerManager → ConfigManager.get_adp_multiplier() integration
2. Test missing ADP data returns neutral multiplier
3. Test ADP rank 0 (undrafted) gets penalty multiplier
4. Test ADP rank > 250 gets capped multiplier
5. Test adp_data.csv format matches code expectations
6. Test config fallback when scoring.adp.curve_exponent missing

**Update Existing Scenarios:**
1. "Test draft recommendations" → Add verification that ADP multiplier applied to scores
2. "Test data loading" → Add adp_data.csv to list of files that must load successfully

**Remove Scenarios:**
None - all S4 scenarios still relevant

**Notes:**
- Scenarios 1-6 are NEW (discovered during implementation)
- Updates 1-2 enhance existing scenarios with specifics
- Focus: Integration testing, not unit tests (those in feature_01 tests/)
```

---

### STEP 3: Update Test Plan

**Purpose:** Apply updates to epic_smoke_test_plan.md

---

#### 3a. Update "Last Updated" Timestamp

**Action:**
```markdown
## Epic Smoke Test Plan: {epic_name}

**Purpose:** Define how to validate the complete epic end-to-end

**Created:** 2025-12-25 (S1)
**Last Updated:** 2025-12-30 (S8.P2 (Epic Testing Update) - after feature_01_adp_integration)
```

---

#### 3b. Add New Test Scenarios

**Template for adding scenarios:**

```markdown
## Integration Test Scenarios

### Scenario 7: ADP Multiplier Integration

**Added:** S8.P2 (Epic Testing Update) (feature_01_adp_integration)

**What to test:** Verify that ADP multiplier is correctly applied to draft recommendations

**How to test:**
1. Ensure adp_data.csv has test data:
   - Player A: ADP rank 1 (expect high multiplier ~1.50)
   - Player B: ADP rank 50 (expect medium multiplier ~1.15)
   - Player C: ADP rank 200 (expect low multiplier ~0.90)

2. Run draft mode:
   ```
   python run_league_helper.py --mode draft
   ```text

3. Review draft recommendations output:
   - Open data/recommendations.csv
   - Verify Player A (rank 1) has higher final_score than projected_points
   - Verify Player C (rank 200) has lower final_score than projected_points

**Expected result:**
- Player A final_score ≈ projected_points * 1.50
- Player B final_score ≈ projected_points * 1.15
- Player C final_score ≈ projected_points * 0.90
- All multipliers visible in adp_multiplier column

**Why added:** Implementation revealed specific multiplier ranges. S4 plan just said "verify ADP affects scores" (too vague). This scenario is executable and verifiable.
```

---

#### 3c. Update Existing Scenarios

**Example - Enhancing vague scenario:**

**Before (from S4):**
```markdown
### Scenario 2: Draft Recommendations

**What to test:** Verify draft recommendations work correctly

**How to test:**
- Run draft mode
- Check output file exists

**Expected result:**
- File created with recommendations
```

**After (S8.P2 (Epic Testing Update) enhancement):**
```markdown
### Scenario 2: Draft Recommendations

**What to test:** Verify draft recommendations work correctly

**How to test:**
1. Run draft mode:
   ```
   python run_league_helper.py --mode draft
   ```text

2. Verify output file created:
   ```
   ls data/recommendations.csv
   ```markdown

3. Verify output content quality:
   - Open data/recommendations.csv
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify adp_multiplier column exists and has values in range 0.85-1.50
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify final_score = projected_points * adp_multiplier
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify top recommendations have high ADP multipliers

**Expected result:**
- File created with recommendations
- **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** All players have adp_multiplier between 0.85-1.50
- **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Final scores correctly incorporate ADP multiplier
- Top 10 recommendations include players with elite ADP (ranks 1-20)

**Why updated:** feature_01 implementation revealed specific multiplier range and integration. Original scenario just checked "file exists" - now verifies data quality and correctness.
```

---

#### 3d. Add Edge Case Scenarios

**Template:**

```markdown
## Edge Case Test Scenarios

### Scenario 12: Missing ADP Data Handling

**Added:** S8.P2 (Epic Testing Update) (feature_01_adp_integration)

**What to test:** Verify system handles players missing from adp_data.csv

**How to test:**
1. Create test scenario:
   - Remove one player (e.g., "J.Smith") from adp_data.csv
   - Ensure "J.Smith" exists in players.csv

2. Run draft mode:
   ```
   python run_league_helper.py --mode draft
   ```text

3. Check handling:
   - Verify "J.Smith" appears in recommendations (not excluded)
   - Verify "J.Smith" has adp_multiplier = 1.0 (neutral)
   - Check logs for INFO message: "Player J.Smith missing ADP, using default"

**Expected result:**
- Players missing ADP data get neutral multiplier (1.0)
- No ERROR or WARNING logs
- No crashes or exceptions
- Missing ADP doesn't exclude player from recommendations

**Why added:** Implementation discovered fallback behavior for missing data. Needs explicit test to ensure it works correctly.
```

---

#### 3e. Update "Integration Points" Section

**Add discovered integration points:**

```markdown
## Integration Points to Validate

**Updated:** S8.P2 (Epic Testing Update) (feature_01_adp_integration)

### Integration Point 1: PlayerManager → ConfigManager

**Components:**
- PlayerManager.calculate_total_score() (league_helper/util/PlayerManager.py:145)
- ConfigManager.get_adp_multiplier() (league_helper/util/ConfigManager.py:234)

**Flow:**
1. PlayerManager calls ConfigManager.get_adp_multiplier(player.adp)
2. ConfigManager returns (multiplier, score) tuple
3. PlayerManager applies: final_score *= multiplier
4. PlayerManager stores multiplier for display

**Test:**
- Verify multiplier is applied (final_score changes)
- Verify multiplier is stored (visible in output)
- Verify score is stored (for debugging)

**Future integration:** feature_02 (player_rating) will add similar integration. S9 must test BOTH multipliers apply correctly together.
```

---

#### 3f. Update "Epic Success Criteria" If Needed

**If implementation revealed new success criteria:**

```markdown
## Epic Success Criteria

**The epic is successful if:**

1. {Original criterion from S1}
2. {Original criterion from S1}
3. **[ADDED S8.P2 (Epic Testing Update) - feature_01]** All scoring multipliers (ADP, rating, schedule, etc.) correctly apply to final scores
4. **[ADDED S8.P2 (Epic Testing Update) - feature_01]** Missing data handled gracefully with neutral multipliers (not crashes)
```

---

#### 3g. Add Entry to Update History

**Maintain clear audit trail:**

```markdown
## Update History

| Date | Stage | Changes Made | Reason |
|------|-------|--------------|--------|
| 2025-12-25 | S1 | Initial creation | Epic planning |
| 2025-12-27 | S4 | Major update | Deep dive findings (all features spec'd) |
| 2025-12-30 | S8.P2 (Epic Testing Update) (Feature 1) | Added 6 test scenarios, updated 2 existing scenarios | feature_01_adp_integration implementation revealed integration points, edge cases, and specific multiplier ranges not captured in S4 assumptions |

**Current version is informed by:**
- S1: Initial epic analysis (high-level categories)
- S4: Deep dive findings from Stages 2-3 (all feature specs)
- S8.P2 (Epic Testing Update) updates:
  - feature_01_adp_integration (6 new scenarios, 2 updated)
  - {future features will add rows here}
```

---

### STEP 4: Final Verification

**Purpose:** Ensure test plan is coherent, executable, and ready for S9

---

#### Final Verification Checklist

**Test Plan Quality:**
- [ ] All new scenarios have clear "What to test"
- [ ] All new scenarios have executable "How to test" (commands, steps)
- [ ] All new scenarios have verifiable "Expected result"
- [ ] All scenarios include "Why added" rationale

**Consistency:**
- [ ] "Last Updated" timestamp is current
- [ ] Update History table has entry for this update
- [ ] Integration Points section includes new integrations
- [ ] Epic Success Criteria updated if needed

**Coherence:**
- [ ] New scenarios don't contradict existing ones
- [ ] Test plan flows logically
- [ ] No duplicate scenarios
- [ ] Scenarios are at appropriate level (epic, not feature unit tests)

**Executability:**
- [ ] Commands are correct (can copy-paste and run)
- [ ] File paths are accurate
- [ ] Expected results are measurable
- [ ] Test plan is actionable (not aspirational)

**Git:**
- [ ] epic_smoke_test_plan.md updated
- [ ] Changes committed with descriptive message
- [ ] Commit message includes feature name

**README Agent Status:**
- [ ] Updated with S8.P2 (Epic Testing Update) completion
- [ ] Next action set appropriately:
  - If more features remain → "Next Feature's S5"
  - If all features done → "S9: Epic Final QC"

**If ALL boxes checked:** S8.P2 (Epic Testing Update) complete

**If ANY box unchecked:** Complete missing items before proceeding

---

## 🛑 MANDATORY CHECKPOINT 1

**You are about to declare S8.P2 complete**

⚠️ STOP - DO NOT PROCEED TO NEXT FEATURE YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Critical Rules" section at top of this guide
2. [ ] Verify you updated based on ACTUAL implementation (not spec.md)
3. [ ] Verify test scenarios are SPECIFIC (include file names, function names, data values)
4. [ ] Update EPIC_README.md Agent Status:
   - Current Guide: "stages/s5/s5_v2_validation_loop.md" (if more features) OR "stages/s9/s9_epic_final_qc.md" (if all features done)
   - Current Step: "S8.P2 complete, ready to start next feature OR S9"
   - Last Updated: [timestamp]
5. [ ] Output acknowledgment: "✅ CHECKPOINT 1 COMPLETE: Re-read Critical Rules, verified test scenarios are specific"

**Why this checkpoint exists:**
- 85% of agents write vague test scenarios ("test integration")
- Vague scenarios cause 70% test case miss rate in S9
- 2 minutes of specificity prevents hours of S9 rework

**ONLY after completing ALL 5 actions above, proceed to next section**

---

## Commit Message Template

**When committing test plan updates:**

```text
Update epic smoke test plan after feature_01_adp_integration

Added test scenarios:
- ADP multiplier integration test (PlayerManager → ConfigManager)
- Missing ADP data handling (neutral multiplier fallback)
- ADP rank 0 (undrafted) penalty test
- ADP rank > 250 cap test
- adp_data.csv format validation
- Config fallback when scoring.adp.curve_exponent missing

Updated scenarios:
- Draft recommendations: Add ADP multiplier verification
- Data loading: Add adp_data.csv to required files

Rationale: Implementation revealed specific multiplier ranges (0.85-1.50),
integration points (PlayerManager → ConfigManager), and edge case behaviors
(missing data, rank 0, rank > 250) that weren't captured in S4 plan.

Ensures S9 epic QC tests actual implementation, not assumptions.
```

---

## Exit Criteria

**S8.P2 (Epic Testing Update) is complete when ALL of the following are true:**

### Test Plan Updated
- [x] epic_smoke_test_plan.md reviewed
- [x] Actual implementation code reviewed (not just specs)
- [x] Integration points identified and added to test plan
- [x] Edge cases discovered during implementation added to test plan
- [x] New test scenarios added with specific details (what, how, expected)

### Plan Quality
- [x] All scenarios have clear "What to test"
- [x] All scenarios have executable "How to test" (commands/steps)
- [x] All scenarios have verifiable "Expected result"
- [x] All updates include "Why added/updated" rationale
- [x] Scenarios are epic-level (not feature unit tests)

### Documentation
- [x] "Last Updated" timestamp current
- [x] Update History table has entry for this feature
- [x] Integration Points section updated if new integrations found
- [x] Epic Success Criteria updated if needed

### Git Status
- [x] epic_smoke_test_plan.md committed
- [x] Descriptive commit message includes feature name
- [x] Working directory clean

### README Agent Status
- [x] Updated with S8.P2 (Epic Testing Update) completion
- [x] Next action set appropriately:
  - More features remain → "Read S5 guide for feature_02"
  - All features done → "Read stages/s9/s9_p1_epic_smoke_testing.md"

**If ALL criteria met:**
- If more features remain → Proceed to next feature's S5
- If all features done → Proceed to S9 (Epic Final QC)

**If ANY criteria not met:** Do NOT proceed until all are met

---

## Common Mistakes to Avoid

### Anti-Pattern 1: Updating Based on Specs (Not Code)

**Wrong:** Reading feature spec and adding test scenarios based on planned behavior
**Right:** Reading ACTUAL implemented code and adding scenarios based on real behavior
**Why:** Implementation often differs from specs (edge cases, design changes, discovered dependencies)

---

### Anti-Pattern 2: Vague Test Scenarios

**Wrong:** "Test ADP integration works"
**Right:**
```
Test Scenario: ADP Multiplier Integration
Context: After feature_01_adp_integration complete
Steps:
  1. Load player with adp_value=15 (high draft pick)
  2. Call PlayerManager.calculate_total_score(player)
  3. Verify: Final score includes adp_multiplier boost
Expected: score > base_score (multiplier applied)
```

---

### Anti-Pattern 3: Only Adding Scenarios (Not Updating Existing)

**Wrong:** Always appending new scenarios to end of test plan
**Right:** Update existing scenarios if implementation contradicts them, remove obsolete scenarios
**Why:** Test plan must stay internally consistent as implementation reveals reality

---

### Anti-Pattern 4: Not Documenting Why Scenario Added

**Wrong:** Adding test scenario without explanation
**Right:** Include rationale in Update History: "Added because implementation revealed cross-feature dependency not in spec"
**Why:** Future maintainers need to understand why test exists

---

### Anti-Pattern 5: Testing Feature Details (Not Epic Integration)

**Wrong:** "Test that _parse_adp_csv() handles malformed CSV"
**Right:** "Test that ADP data successfully integrates with draft recommendations across features"
**Why:** Feature unit tests in S7, epic tests in S8.P2 focus on cross-feature workflows

---

### Anti-Pattern 6: Skipping Updates After Simple Features

**Wrong:** "Feature was simple, no epic testing changes needed"
**Right:** Always review - even simple features often reveal integration points
**Why:** "Simple" features frequently have unexpected cross-feature impacts

---

### Quick Checklist to Avoid Mistakes

Before completing S8.P2, verify:
- [ ] Read actual CODE (not just specs)
- [ ] Test scenarios have specific steps and expected results
- [ ] Updated/removed existing scenarios (not just appended)
- [ ] Documented WHY each change made (Update History)
- [ ] Focus on EPIC-level integration (not feature unit tests)
- [ ] Reviewed even if feature seemed "simple"


**Detailed examples extracted to reference file for easier navigation:**

**File:** `reference/s8_p2_testing_examples.md` (~240 lines)

**What's covered:**
1. **Example 1: After Feature 01 (ADP Integration)**
   - Integration points discovered during implementation
   - Test scenarios added based on actual code
   - Update history showing rationale

2. **Example 2: After Feature 02 (Injury Assessment)**
   - Cross-feature dependencies found
   - Edge cases discovered in testing
   - Test plan refinements

3. **Example 3: After Feature 04 (Integration Feature)**
   - Complex integration scenarios
   - Epic-level success criteria updates
   - Final testing strategy adjustments

**When to reference:**
- First time doing S8.P2 (learn the pattern)
- Unsure how to document discovered integration points
- Need examples of specific test scenario format

**See:** `reference/s8_p2_testing_examples.md` for complete examples


**The epic is successful if:**

1. Draft recommendations incorporate all planned scoring multipliers (ADP, rating, schedule, injury, bye week)
2. Trade simulator evaluates trades using updated scoring algorithm
3. All data integrates without breaking existing functionality
4. User can see breakdown of score components for transparency
```

**S8.P2 (Epic Testing Update) update:**
```markdown
## Epic Success Criteria

**The epic is successful if:**

1. Draft recommendations incorporate all planned scoring multipliers (ADP, rating, schedule, injury, bye week)
2. Trade simulator evaluates trades using updated scoring algorithm
3. All data integrates without breaking existing functionality
4. User can see breakdown of score components for transparency
5. **[ADDED S8.P2 (Epic Testing Update) - feature_01]** System handles missing or incomplete data gracefully (no crashes, neutral fallbacks logged clearly)
6. **[ADDED S8.P2 (Epic Testing Update) - feature_01]** All multiplier calculations use consistent patterns (return Tuple[multiplier, score], range 0.85-1.50)

**Rationale for updates:**
- Criterion 5: feature_01 implementation revealed importance of missing data handling. Original epic didn't consider data quality scenarios.
- Criterion 6: feature_01 established pattern (tuple return, specific range) that all features should follow for consistency.
```

**Result:** Epic success criteria now reflect implementation realities, not just original assumptions.

---

## README Agent Status Update Requirements

**Update README Agent Status at these points:**

### At Start of S8.P2 (Epic Testing Update)
```markdown
**Current Phase:** TESTING_PLAN_UPDATE
**Current Guide:** stages/s8/s8_p2_epic_testing_update.md
**Guide Last Read:** 2025-12-30 17:00
**Critical Rules:** "Update based on ACTUAL implementation", "Add discovered integration points", "Keep scenarios executable"
**Next Action:** Review feature_01 code and epic_smoke_test_plan.md
**Completed Feature:** feature_01_adp_integration (just completed S8.P1 (Cross-Feature Alignment))
```

### At Completion of S8.P2 (Epic Testing Update)
```markdown
**Current Phase:** {Next phase based on remaining features}
**Previous Guide:** stages/s8/s8_p2_epic_testing_update.md (COMPLETE)
**Current Guide:** {Next guide based on status below}
**Guide Last Read:** {Not read yet for next guide}
**Next Action:**
- If more features remain: "Read stages/s5/s5_v2_validation_loop.md for feature_02 (Round 1)"
- If all features done: "Read stages/s9/s9_p1_epic_smoke_testing.md"
**S8.P2 (Epic Testing Update) Summary:**
- Reviewed feature_01_adp_integration implementation
- Added 6 new test scenarios to epic_smoke_test_plan.md
- Updated 2 existing scenarios with specific verification steps
- Added integration point documentation
- Updated Epic Success Criteria with 2 new criteria
**S8.P2 (Epic Testing Update) Completion:** 2025-12-30 17:15
```

---

## Prerequisites for Next Stage

**Before transitioning to next stage, verify:**

### S8.P2 (Epic Testing Update) Complete
- [ ] All S8.P2 (Epic Testing Update) completion criteria met
- [ ] epic_smoke_test_plan.md updated with implementation insights
- [ ] Test scenarios specific and executable
- [ ] Git committed with descriptive message

### Next Stage Determination
- [ ] Checked epic README for remaining features
- [ ] Determined next action:
  - **More features remain** → Next feature's S5 (Implementation Planning)
  - **All features done** → S9 (Epic Final QC)

### If More Features Remain
- [ ] Next feature identified (e.g., feature_02_player_rating)
- [ ] Next feature has spec.md and checklist.md ready
- [ ] Ready to read stages/s5/s5_v2_validation_loop.md (Round 1 for next feature)

### If All Features Done
- [ ] Verified ALL features completed S8.P2 (Epic Testing Update)
- [ ] Epic README shows all features complete
- [ ] No pending bug fixes
- [ ] Ready to read stages/s9/s9_p1_epic_smoke_testing.md

**If ALL verified:** Ready for next stage

---

## Summary

**S8.P2 (Epic Testing Update) keeps epic testing plan current through:**

1. **Actual Implementation Review** - Read code that was actually written (not specs)
2. **Gap Identification** - Find what test plan is missing based on implementation
3. **Specific Scenario Addition** - Add executable test scenarios with clear verification
4. **Evolution Documentation** - Track how plan matured from S1 → 4 → 5e

**Critical protocols:**
- Update based on ACTUAL implementation (read the code)
- Add SPECIFIC test scenarios (executable, verifiable)
- Focus on EPIC-LEVEL testing (cross-feature integration)
- DOCUMENT update rationale (why added/updated)
- COMMIT immediately (don't defer)

**Success criteria:**
- Test plan updated with implementation insights
- New integration points added
- Edge cases discovered during implementation captured
- Scenarios are specific and executable
- Ready for S9 to execute evolved test plan

**Why this matters:** Test plans based on assumptions miss integration points discovered during implementation. S8.P2 (Epic Testing Update) ensures the test plan reflects what was actually built, making S9 epic QC accurate and effective.

---

*End of stages/s8/s8_p2_epic_testing_update.md*
