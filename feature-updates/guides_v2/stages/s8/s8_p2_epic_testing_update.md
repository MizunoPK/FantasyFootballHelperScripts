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
```markdown

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

## 🛑 Critical Rules

```bash
1. ⚠️ UPDATE BASED ON ACTUAL IMPLEMENTATION (Not specs)
   - Read the ACTUAL CODE that was written
   - Don't rely on specs or TODO list
   - Verify actual interfaces, data structures, behaviors
   - Test plan must reflect reality, not plans

2. ⚠️ IDENTIFY INTEGRATION POINTS DISCOVERED
   - Look for cross-feature interactions implementation revealed
   - Identify dependencies specs didn't predict
   - Note data flows between features
   - Document edge cases discovered during implementation

3. ⚠️ ADD SPECIFIC TEST SCENARIOS (Not vague categories)
   - Bad: "Test feature integration"
   - Good: "Test that PlayerManager.calculate_score() applies ADP multiplier to final score"
   - Include WHAT to test, HOW to verify, EXPECTED result

4. ⚠️ UPDATE EXISTING SCENARIOS (Don't just append)
   - If implementation contradicts existing scenario → update it
   - If behavior more complex than assumed → expand scenario
   - Remove scenarios that don't apply anymore
   - Keep test plan internally consistent

5. ⚠️ FOCUS ON EPIC-LEVEL TESTING (Not feature unit tests)
   - Feature unit tests covered in S7 (Testing & Review)
   - This is about EPIC-LEVEL integration testing
   - Test cross-feature workflows
   - Test epic success criteria

6. ⚠️ DOCUMENT UPDATE RATIONALE
   - Add notes explaining WHY test added
   - Reference feature that drove update
   - Link to actual code locations if relevant
   - Update history table with changes

7. ⚠️ KEEP PLAN EXECUTABLE
   - Test scenarios should be runnable during S9
   - Include commands/steps to execute tests
   - Specify expected outputs
   - Make plan actionable, not aspirational

8. ⚠️ PRESERVE STAGE 1 AND 4 UPDATES
   - Don't delete original test categories from S1
   - Don't remove test scenarios added in S4
   - ADD to the plan (don't replace it)
   - Evolution builds on previous stages

9. ⚠️ COMMIT TEST PLAN UPDATES
   - Update epic_smoke_test_plan.md
   - Commit changes with descriptive message
   - Include feature name in commit message
   - Keep git history clear

10. ⚠️ SHORT BUT THOROUGH
    - This stage should take 15-30 minutes
    - Focus on significant insights
    - Don't overthink minor details
    - But don't skip if no obvious changes
```markdown

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
```markdown

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

**Purpose:** Understand what was ACTUALLY built to inform test plan updates

---

#### 1a. Read Just-Completed Feature Code

**Actions:**
1. Open the actual source files created/modified in just-completed feature
2. Review key implementation details:
   - **Interfaces created:** New methods, classes, public APIs
   - **Data structures:** CSV formats, JSON structures, object fields
   - **Integration points:** Calls to other features, shared modules
   - **Configuration:** New config keys, settings, defaults
   - **Edge cases handled:** Error handling, validation, boundary conditions

**Example:**
```python
# Just completed: feature_01_adp_integration

# Reading actual code:
# File: league_helper/util/ConfigManager.py

def get_adp_multiplier(self, adp_value: float) -> Tuple[float, int]:
    """
    Calculate ADP multiplier for draft recommendations.

    Implementation notes for testing:
    - Returns tuple (multiplier, score)
    - Multiplier range: 0.85-1.50
    - Uses exponential curve for top 10 picks
    - Uses linear scaling for picks 11-250
    - Returns (1.0, 50) for unknown ADP values
    """
    # Key integration point: Called by PlayerManager.calculate_total_score()
    # Data dependency: Requires data/player_data/adp_data.csv
    # Config dependency: Uses config['scoring']['adp']['curve_exponent']
```bash

---

#### 1b. Identify Integration Points

**Purpose:** Find where this feature interacts with other parts of the system

**Look for:**
- Methods called FROM other modules (entry points)
- Methods that CALL other modules (dependencies)
- Shared data structures (files read/written by multiple features)
- Configuration shared across features
- Workflows that span multiple features

**Template:**
```markdown
## Integration Points Found in feature_01_adp_integration

**Entry Points** (other code calls into this feature):
1. PlayerManager.calculate_total_score() calls ConfigManager.get_adp_multiplier()
   - Location: league_helper/util/PlayerManager.py:145
   - When: During draft recommendations (AddToRosterMode)
   - Impact: ADP multiplier affects all draft recommendations

**Dependencies** (this feature calls other code):
1. ConfigManager.__init__() loads config from league_config.json
   - Location: league_helper/util/ConfigManager.py:67
   - What: Loads scoring.adp.curve_exponent setting
   - Fallback: Defaults to 2.0 if not present

**Shared Data:**
1. data/player_data/adp_data.csv
   - Read by: ADPDataLoader (feature_01)
   - Will be read by: PlayerRatingIntegration (feature_02) - shares same directory
   - Format: [name, position, team, adp_rank, adp_value]

**Cross-Feature Workflows:**
1. Draft Recommendation Flow:
   - User → AddToRosterMode → PlayerManager → ConfigManager.get_adp_multiplier()
   - Future: PlayerManager will also call get_rating_multiplier() (feature_02)
   - Integration test needed: Verify both multipliers apply correctly
```markdown

---

#### 1c. Note Edge Cases and Behaviors

**Look for:**
- How does feature handle missing data?
- How does feature handle invalid input?
- What are the boundary conditions?
- Any surprising behaviors discovered during implementation?

**Example:**
```markdown
## Edge Cases Discovered in Implementation

1. **Missing ADP data:**
   - Behavior: Returns (1.0, 50) - neutral multiplier
   - Log message: INFO level "Player {name} missing ADP, using default"
   - Test needed: Verify neutral multiplier doesn't advantage/disadvantage players

2. **ADP rank 0 (undrafted):**
   - Behavior: Treated as very low draft value (multiplier 0.85)
   - Reasoning: Undrafted = market doesn't value them
   - Test needed: Verify undrafted players get penalty, not neutral

3. **ADP value > 250:**
   - Behavior: Capped at rank 250 (multiplier 0.85)
   - Reasoning: Beyond 250 all have minimal value
   - Test needed: Verify ranks 251+ all get same multiplier
```markdown

---

### STEP 2: Compare to Current Test Plan

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
```markdown

---

### STEP 3: Update Test Plan

**Purpose:** Apply updates to epic_smoke_test_plan.md

---

#### 3a. Update "Last Updated" Timestamp

**Action:**
```markdown
# Epic Smoke Test Plan: {epic_name}

**Purpose:** Define how to validate the complete epic end-to-end

**Created:** 2025-12-25 (S1)
**Last Updated:** 2025-12-30 (S8.P2 (Epic Testing Update) - after feature_01_adp_integration)
```markdown

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
   ```bash
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
```markdown

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
```markdown

**After (S8.P2 (Epic Testing Update) enhancement):**
```markdown
### Scenario 2: Draft Recommendations

**What to test:** Verify draft recommendations work correctly

**How to test:**
1. Run draft mode:
   ```bash
   python run_league_helper.py --mode draft
   ```text

2. Verify output file created:
   ```bash
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
```markdown

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
   ```bash
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
```markdown

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
```markdown

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
```markdown

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
```markdown

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
   - Current Guide: "stages/s5/s5_p1_planning_round1.md" (if more features) OR "stages/s9/s9_epic_final_qc.md" (if all features done)
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
```markdown

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

**Mistake:**
"Spec said feature_01 would use ConfigManager.get_adp(), so I'll add test for that interface."

**Why it's wrong:** Actual implementation might be different from spec. Must read actual code.

**Correct approach:** Read actual source file, verify actual method name and signature.

---

### Anti-Pattern 2: Vague Test Scenarios

**Mistake:**
```markdown
### Test ADP Integration
- Run the system
- Check it works
```markdown

**Why it's wrong:** Not executable. Can't determine pass/fail in S9.

**Correct approach:**
```markdown
### Test ADP Multiplier Integration
- Run: python run_league_helper.py --mode draft
- Open: data/recommendations.csv
- Verify: adp_multiplier column exists with values 0.85-1.50
- Verify: final_score = projected_points * adp_multiplier
```markdown

---

### Anti-Pattern 3: Skipping If "No Obvious Changes"

**Mistake:**
"Feature_01 was straightforward, test plan probably doesn't need updates. I'll skip S8.P2 (Epic Testing Update)."

**Why it's wrong:** Even simple implementations reveal integration points and edge cases.

**Correct approach:** Always do S8.P2 (Epic Testing Update). Even if only adding 1-2 scenarios, it's worth 15 minutes.

---

### Anti-Pattern 4: Duplicate Unit Tests in Epic Plan

**Mistake:**
```markdown
### Test get_adp_multiplier returns tuple
- Call ConfigManager.get_adp_multiplier(10)
- Assert: returns (float, int) tuple
```markdown

**Why it's wrong:** This is feature_01's unit test, not epic-level integration test.

**Correct approach:** Epic tests focus on cross-feature integration and end-to-end workflows.

---

### Anti-Pattern 5: Not Updating Existing Scenarios

**Mistake:**
"I'll just add new scenarios at the bottom. Won't touch existing ones."

**Why it's wrong:** Existing scenarios might have become outdated or too vague.

**Correct approach:** Review existing scenarios, enhance with specific details from implementation.

---

### Anti-Pattern 6: Missing Update Rationale

**Mistake:**
```markdown
### Scenario 8: Test missing data

{Test details...}
```markdown

**Why it's wrong:** Future agents won't know why this was added or what feature drove it.

**Correct approach:**
```markdown
### Scenario 8: Missing ADP Data Handling

**Added:** S8.P2 (Epic Testing Update) (feature_01_adp_integration)

{Test details...}

**Why added:** Implementation discovered fallback behavior (neutral multiplier)
for missing ADP data. Needs explicit test to ensure it works correctly.
```markdown

---

### Anti-Pattern 7: Forgetting to Commit

**Mistake:**
"I updated epic_smoke_test_plan.md but I'll commit later with other changes."

**Why it's wrong:** If something goes wrong, test plan updates are lost. Can't track which feature drove which updates.

**Correct approach:** Commit test plan updates immediately, before moving to next feature.

---

### Anti-Pattern 8: Deleting S1/4 Content

**Mistake:**
"S1 test plan was just placeholders. I'll delete it and replace with real tests."

**Why it's wrong:** Loses evolution history. Can't see how plan matured.

**Correct approach:** Enhance S1/4 content. Mark updates clearly: `[UPDATED S8.P2 (Epic Testing Update) - feature_01]`

---

### Anti-Pattern 9: Not Reading Actual Code

**Mistake:**
"I implemented the feature, I know what I built. Don't need to re-read code."

**Why it's wrong:** Memory is unreliable. Details matter for test scenarios.

**Correct approach:** Open source files, read actual implementation, note specific details.

---

### Anti-Pattern 10: Unclear Update History

**Mistake:**
```text
| 2025-12-30 | S8.P2 (Epic Testing Update) | Added tests | Feature 1 |
```markdown

**Why it's wrong:** No detail on what was added or why.

**Correct approach:**
```text
| 2025-12-30 | S8.P2 (Epic Testing Update) (Feature 1) | Added 6 test scenarios, updated 2 existing | feature_01 revealed integration points, edge cases, multiplier ranges not in S4 |
```markdown

---

## Real-World Examples

### Example 1: Adding Integration Point Test

**Just completed:** feature_01_adp_integration

**Implementation review reveals:**
```python
# File: league_helper/util/PlayerManager.py

def calculate_total_score(self, player: FantasyPlayer) -> float:
    """Calculate final player score with all multipliers."""

    # Start with projected points
    score = player.projected_points

    # Apply ADP multiplier (NEW in feature_01)
    adp_multiplier, adp_score = self.config.get_adp_multiplier(player.adp)
    player.adp_multiplier = adp_multiplier  # Store for display
    player.adp_score = adp_score  # Store for debugging
    score *= adp_multiplier  # Apply to final score

    return score
```markdown

**Current test plan (from S4):**
```markdown
### Scenario 3: Scoring Calculation

**What to test:** Verify player scores calculated correctly

**How to test:**
- Load players
- Calculate scores
- Check scores are reasonable

**Expected result:** Players have scores
```markdown

**S8.P2 (Epic Testing Update) updates:**

**Update existing scenario:**
```markdown
### Scenario 3: Scoring Calculation

**What to test:** Verify player scores calculated correctly

**How to test:**
1. Load players:
   ```bash
   python run_league_helper.py --mode draft
   ```markdown

2. Review recommendations output:
   - Open data/recommendations.csv
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify all players have adp_multiplier column
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify all players have adp_score column
   - **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Verify final_score = projected_points * adp_multiplier

**Expected result:**
- Players have scores
- **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** All adp_multiplier values between 0.85-1.50
- **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** All adp_score values between 0-100
- **[UPDATED S8.P2 (Epic Testing Update) - feature_01]:** Math verifies: final_score = projected * multiplier
```markdown

**Add new integration scenario:**
```markdown
### Scenario 9: PlayerManager → ConfigManager Integration

**Added:** S8.P2 (Epic Testing Update) (feature_01_adp_integration)

**What to test:** Verify PlayerManager correctly integrates with ConfigManager for ADP multipliers

**How to test:**
1. Create test player with known ADP:
   - Player: "Test Player"
   - Position: QB
   - Projected Points: 300.0
   - ADP: 10 (elite pick)

2. Run scoring calculation:
   ```bash
   python -c "
   from league_helper.util.PlayerManager import PlayerManager
   from league_helper.util.ConfigManager import ConfigManager
   from league_helper.util.FantasyPlayer import FantasyPlayer

   config = ConfigManager('data/')
   manager = PlayerManager(config)

   player = FantasyPlayer('Test Player', 'QB', projected_points=300.0, adp=10)
   score = manager.calculate_total_score(player)

   print(f'Final score: {score}')
   print(f'ADP multiplier: {player.adp_multiplier}')
   print(f'ADP score: {player.adp_score}')
   print(f'Math check: {300.0 * player.adp_multiplier}')
   "
   ```text

3. Verify integration:
   - ConfigManager.get_adp_multiplier() was called
   - Returned tuple was unpacked correctly
   - Multiplier was stored in player.adp_multiplier
   - Score was stored in player.adp_score
   - Final score = 300.0 * multiplier

**Expected result:**
- ADP multiplier ≈ 1.45 (elite pick gets high multiplier)
- ADP score ≈ 95 (elite rating)
- Final score ≈ 435.0 (300 * 1.45)
- Math check matches final score

**Why added:** Implementation revealed specific integration pattern (ConfigManager → tuple return → PlayerManager unpacks and stores). S4 plan didn't specify this interaction. Need explicit test to ensure it works correctly.
```markdown

**Result:** Test plan now has specific, executable test for integration point discovered during implementation.

---

### Example 2: Adding Edge Case Test

**Just completed:** feature_01_adp_integration

**Implementation review reveals:**
```python
# File: league_helper/util/ConfigManager.py

def get_adp_multiplier(self, adp_value: float) -> Tuple[float, int]:
    """Calculate ADP multiplier."""

    # Handle missing ADP data
    if adp_value is None or adp_value == 0:
        self.logger.info(f"ADP value missing or zero, using neutral multiplier")
        return (1.0, 50)  # Neutral multiplier, mid-range score

    # Handle undrafted players (rank > 250)
    if adp_value > 250:
        adp_value = 250  # Cap at 250

    # Calculate multiplier...
```markdown

**Current test plan (from S4):**
- No edge case scenarios for missing data or boundary conditions

**S8.P2 (Epic Testing Update) update - Add new scenario:**
```markdown
### Scenario 10: Edge Case - Missing ADP Data

**Added:** S8.P2 (Epic Testing Update) (feature_01_adp_integration)

**What to test:** Verify system handles players with missing ADP data gracefully

**How to test:**
1. Create test scenario:
   - Edit data/player_data/adp_data.csv
   - Remove entry for "P.Mahomes"
   - Ensure "P.Mahomes" exists in data/players.csv

2. Run draft mode:
   ```bash
   python run_league_helper.py --mode draft
   ```bash

3. Check output:
   - Open data/recommendations.csv
   - Find "P.Mahomes" row
   - Verify adp_multiplier = 1.0 (neutral)
   - Verify adp_score = 50 (mid-range)
   - Verify final_score = projected_points * 1.0 (no advantage/penalty)

4. Check logs:
   - Should have INFO log: "ADP value missing or zero, using neutral multiplier"
   - Should NOT have ERROR or WARNING

**Expected result:**
- "P.Mahomes" appears in recommendations (not excluded)
- adp_multiplier = 1.0 exactly
- adp_score = 50 exactly
- No crashes, exceptions, or errors
- Missing ADP doesn't advantage or penalize player

**Why added:** Implementation discovered fallback behavior for missing ADP data (returns neutral multiplier 1.0). This wasn't specified in original spec and needs explicit testing to ensure it works correctly. Important for data quality scenarios where ADP data is incomplete.
```markdown

**Add another edge case scenario:**
```markdown
### Scenario 11: Edge Case - ADP Rank > 250

**Added:** S8.P2 (Epic Testing Update) (feature_01_adp_integration)

**What to test:** Verify system caps ADP ranks above 250 to prevent extreme penalties

**How to test:**
1. Create test scenario:
   - Edit data/player_data/adp_data.csv
   - Add test player: "Test Player,QB,TEST,500,500.0"
   - ADP rank 500 (very late pick)

2. Run draft mode:
   ```bash
   python run_league_helper.py --mode draft
   ```bash

3. Check output:
   - Open data/recommendations.csv
   - Find "Test Player" row
   - Verify adp_multiplier ≈ 0.85 (minimum, capped)
   - Verify adp_score ≈ 0 (lowest rating)
   - Compare to player with ADP rank 250 (should have same multiplier)

**Expected result:**
- ADP rank 500 gets same multiplier as rank 250 (both capped at 0.85)
- No extreme penalties for very late picks
- Multiplier doesn't go below 0.85

**Why added:** Implementation discovered capping behavior for ADP > 250. Prevents extreme penalties for late-round picks. Need test to verify cap is applied correctly and consistently.
```markdown

**Result:** Test plan now covers edge cases discovered during implementation that weren't anticipated in S4.

---

### Example 3: Updating Success Criteria

**Just completed:** feature_01_adp_integration

**Implementation reveals:** System must handle missing data gracefully (wasn't in original epic success criteria)

**Original Epic Success Criteria (from S1):**
```markdown
## Epic Success Criteria

**The epic is successful if:**

1. Draft recommendations incorporate all planned scoring multipliers (ADP, rating, schedule, injury, bye week)
2. Trade simulator evaluates trades using updated scoring algorithm
3. All data integrates without breaking existing functionality
4. User can see breakdown of score components for transparency
```markdown

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
```markdown

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
```markdown

### At Completion of S8.P2 (Epic Testing Update)
```markdown
**Current Phase:** {Next phase based on remaining features}
**Previous Guide:** stages/s8/s8_p2_epic_testing_update.md (COMPLETE)
**Current Guide:** {Next guide based on status below}
**Guide Last Read:** {Not read yet for next guide}
**Next Action:**
- If more features remain: "Read stages/s5/s5_p1_planning_round1.md for feature_02 (Round 1)"
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
- [ ] Ready to read stages/s5/s5_p1_planning_round1.md (Round 1 for next feature)

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
