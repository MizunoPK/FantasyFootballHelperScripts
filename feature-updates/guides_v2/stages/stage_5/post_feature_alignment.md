# STAGE 5d: Post-Feature Alignment Guide (V2)

**Purpose:** After completing a feature, review ALL remaining (not-yet-implemented) feature specs to ensure they align with the ACTUAL implementation (not just the plan). Update specs based on real insights from implementation to prevent spec drift and catch cascading changes early.

**Stage Flow Context:**
```
Stage 5a (TODO Creation) → Stage 5b (Implementation) → Stage 5c (Post-Implementation) →
→ [YOU ARE HERE: Stage 5d - Cross-Feature Alignment] →
→ Stage 5e (Testing Plan Update) → Next Feature's Stage 5a (or Stage 6 if all features done)
```

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Cross-Feature Alignment, you MUST:**

1. **Use the phase transition prompt** from `prompts_reference_v2.md`
   - Find "Starting Stage 5d (Cross-Feature Alignment)" prompt
   - Speak it out loud (acknowledge requirements)
   - List critical requirements from this guide

2. **Update README Agent Status** with:
   - Current Phase: CROSS_FEATURE_ALIGNMENT
   - Current Guide: STAGE_5d_post_feature_alignment_guide.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "Compare to ACTUAL implementation", "Update specs proactively", "Mark features needing rework"
   - Next Action: Review feature_01 spec (first remaining feature)

3. **Verify all prerequisites** (see checklist below)

4. **THEN AND ONLY THEN** begin Cross-Feature Alignment workflow

**This is NOT optional.** Reading this guide ensures you don't miss critical spec updates.

---

## Quick Start

**What is this stage?**
Post-Feature Alignment is where you update remaining feature specs based on the just-completed feature's actual implementation, ensuring pending features align with real code patterns and integration points discovered during development.

**When do you use this guide?**
- Stage 5c complete (feature fully validated and production-ready)
- There are remaining features to implement
- Ready to align pending specs with completed work

**Key Outputs:**
- ✅ Completed feature reviewed (actual implementation understood)
- ✅ Alignment impacts identified (which specs need updates)
- ✅ Remaining feature specs updated with implementation insights
- ✅ Integration points documented
- ✅ Ready for Stage 5e (Testing Plan Update)

**Time Estimate:**
15-30 minutes per completed feature

**Exit Condition:**
Post-Feature Alignment is complete when all remaining feature specs are updated to reflect actual implementation patterns, integration points are documented, and updates are logged in each affected spec

---

## 🛑 Critical Rules

```
1. ⚠️ REVIEW ALL REMAINING FEATURES (Not just "related" ones)
   - Don't assume which features are affected
   - Implementation insights can affect unexpected features
   - Review EVERY feature that hasn't completed Stage 5c yet
   - Sequentially go through all remaining features

2. ⚠️ COMPARE TO ACTUAL IMPLEMENTATION (Not the plan)
   - Don't compare to original TODO or plan
   - Look at ACTUAL code that was written
   - Check ACTUAL interfaces created
   - Verify ACTUAL data structures used
   - Review ACTUAL integration patterns implemented

3. ⚠️ UPDATE SPECS PROACTIVELY (Don't wait for implementation)
   - If spec assumptions wrong → update NOW
   - If interface changed → update dependent specs NOW
   - If data structure different → update dependent features NOW
   - Don't defer updates to "we'll figure it out during implementation"

4. ⚠️ MARK FEATURES NEEDING SIGNIFICANT REWORK
   - Use clear criteria (see "Significant Rework Criteria" section)
   - If feature needs >3 new TODO tasks → return to Stage 5a
   - If spec assumptions fundamentally wrong → return to Stage 2
   - If feature should be split/removed → return to Stage 1
   - Document WHY rework needed

5. ⚠️ DOCUMENT INSIGHTS IN SPEC
   - Don't just update spec silently
   - Add "Updated based on {feature_name} implementation" note
   - Explain WHY spec changed
   - Reference actual code locations that drove update

6. ⚠️ UPDATE CHECKLIST.MD TOO
   - Don't just update spec.md
   - Update corresponding checklist.md items
   - Mark any resolved questions/decisions
   - Add new questions if implementation revealed unknowns

7. ⚠️ CHECK DEPENDENCIES (Both directions)
   - Features that DEPEND on just-completed feature (downstream)
   - Features that just-completed feature DEPENDS on (upstream)
   - Shared interfaces, data structures, configuration
   - Integration points and workflows

8. ⚠️ NO "PROBABLY FINE" ASSUMPTIONS
   - If unsure if spec needs updating → READ THE ACTUAL CODE
   - If unsure if interface changed → CHECK THE ACTUAL CLASS
   - Don't assume → verify
   - 5 minutes checking saves hours of rework

9. ⚠️ UPDATE EPIC README
   - Document alignment check completion
   - Note any features marked for rework
   - Update epic status if significant changes needed

10. ⚠️ GET USER APPROVAL FOR SIGNIFICANT REWORK
    - If any feature needs to return to Stage 2 or 1 → ask user
    - Present: What changed, why rework needed, proposed approach
    - Don't proceed with major changes without user sign-off
```

---

## Critical Decisions Summary

**Stage 5d has 1 major decision point per remaining feature:**

### Decision Point (Per Feature): Spec Update Classification (UPDATE/REWORK/NO CHANGE)
**Question:** After comparing spec to actual implementation, what level of change is needed?

**Classification criteria:**

**Option A: NO CHANGE**
- Spec assumptions were correct
- Actual implementation matches spec expectations
- No cascading effects from completed feature
- ✅ Mark feature as "Reviewed - No changes needed"
- Proceed to next remaining feature

**Option B: MINOR UPDATE (update spec now, continue normally)**
- Spec assumptions slightly off but fixable with spec edits
- Changes are clarifications, not fundamental shifts
- Examples: Interface signature slightly different, data structure naming changed
- **Action:** Update spec.md and checklist.md NOW with actual implementation details
- ✅ Mark feature as "Spec updated based on {completed_feature}"
- Proceed to next remaining feature

**Option C: SIGNIFICANT REWORK REQUIRED (return to earlier stage)**
- Spec assumptions fundamentally wrong
- Completed feature revealed major gaps or conflicts
- **Criteria for REWORK:**
  - >3 new TODO tasks needed
  - Core algorithm approach no longer valid
  - Data dependencies changed fundamentally
  - Feature should be split or removed
- **Action based on severity:**
  - Return to Stage 5a (TODO creation) if >3 new tasks
  - Return to Stage 2 (Deep Dive) if spec fundamentally wrong
  - Return to Stage 1 (Epic Planning) if feature should be split/removed
- ❌ Mark feature as "REQUIRES REWORK - {reason}"
- Document WHY rework needed
- Get user approval before proceeding

**Impact:** Deferring spec updates to "during implementation" causes rework. Updating specs NOW based on actual implementation prevents cascading failures.

---

**Summary of Alignment Review:**
- Review ALL remaining features (not just "related" ones)
- Compare to ACTUAL implementation (not the plan)
- Classify EACH feature: NO CHANGE / MINOR UPDATE / REWORK
- Update specs proactively (don't defer to implementation)
- Get user approval for any REWORK classifications

---

## Prerequisites Checklist

**Verify these BEFORE starting Cross-Feature Alignment:**

**From Stage 5c (Post-Implementation):**
- [ ] Stage 5c completed for current feature
- [ ] All smoke tests passed
- [ ] All QC rounds passed (3 rounds)
- [ ] PR review complete
- [ ] lessons_learned.md updated
- [ ] Feature is production-ready

**Epic Structure:**
- [ ] Epic EPIC_README.md exists and is current
- [ ] At least one remaining feature exists (not yet implemented)
  - If NO remaining features → skip Stage 5d, proceed to Stage 5e then Stage 6
- [ ] All remaining features have spec.md and checklist.md files

**Code Availability:**
- [ ] Just-completed feature code is committed to git
- [ ] Code is available for review (not just in memory)
- [ ] Can read actual source code for verification

**If ANY prerequisite not met:** Complete missing items before starting Stage 5d

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: IDENTIFY REMAINING FEATURES                        │
│   - List all features not yet at Stage 5c                  │
│   - Determine review order (dependencies first)            │
│   - Create review checklist                                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: FOR EACH REMAINING FEATURE (Sequential)            │
│   2a. Read feature spec.md (fresh eyes)                    │
│   2b. Read just-completed feature's ACTUAL code            │
│   2c. Compare spec assumptions to actual implementation    │
│   2d. Identify misalignments and needed updates            │
│   2e. Update spec.md and checklist.md                      │
│   2f. Mark feature for rework if significant changes       │
│   ↓                                                         │
│   Repeat for next remaining feature                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: HANDLE FEATURES NEEDING REWORK                     │
│   - Review significant rework criteria                     │
│   - Determine which stage to return to (1, 2, or 5a)       │
│   - Get user approval for major rework                     │
│   - Update epic README with rework status                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: FINAL VERIFICATION                                 │
│   - All remaining features reviewed                        │
│   - All needed spec updates applied                        │
│   - Epic README updated                                    │
│   - Ready for Stage 5e                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Navigation

**Stage 5d has 4 main steps. Jump to any step:**

| Step | Focus Area | Go To |
|------|-----------|-------|
| **Step 1** | Identify Remaining Features | [Step 1](#step-1-identify-remaining-features) |
| **Step 2** | Review Each Feature Spec | [Step 2](#step-2-review-each-feature-spec-against-actual-implementation) |
| **Step 3** | Classify & Update Specs | [Step 3](#step-3-classify-and-update-specs) |
| **Step 4** | Document & Complete | [Step 4](#step-4-document-alignment-and-mark-complete) |

**Key Decision Points:**

| Decision | Description | Go To |
|----------|-------------|-------|
| **Update Classification** | NO CHANGE / UPDATE / REWORK | [Critical Decisions](#critical-decisions-summary) |
| **Rework Criteria** | When to return to earlier stages | [Significant Rework Criteria](#significant-rework-criteria-detailed) |
| **Completion Check** | Verify all features reviewed | [Completion Criteria](#completion-criteria) |

**Reference Sections:**

| Section | Description | Go To |
|---------|-------------|-------|
| Critical Rules | Must-follow alignment rules | [Critical Rules](#critical-rules) |
| Common Mistakes | What to avoid | [Common Mistakes](#common-mistakes-to-avoid) |
| Prerequisites | What must be done first | [Prerequisites Checklist](#prerequisites-checklist) |

**Tip:** For each remaining feature, follow Steps 2-3, then move to next feature. Complete Step 4 after all features reviewed.

---

## Detailed Workflow

### STEP 1: Identify Remaining Features

**Purpose:** Determine which features need alignment review and in what order.

---

#### 1a. List All Remaining Features

**Actions:**
1. Open epic EPIC_README.md
2. Review epic checklist section
3. Identify features that have NOT completed Stage 5c:
   ```markdown
   Features remaining:
   - [ ] feature_02_player_rating_integration
   - [ ] feature_03_schedule_strength
   - [ ] feature_04_injury_risk_assessment
   ```

4. If NO remaining features:
   - Skip Stage 5d entirely
   - Proceed to Stage 5e (Testing Plan Update)
   - Then Stage 6 (Epic Final QC)

**Example:**
```markdown
## Just completed: feature_01_adp_integration

## Remaining features to review:
1. feature_02_player_rating_integration
2. feature_03_schedule_strength
3. feature_04_injury_risk_assessment
4. feature_05_bye_week_penalties

Total: 4 features to review
```

---

#### 1b. Determine Review Order

**Recommendation:** Review in dependency order (features that depend on just-completed feature FIRST)

**Why:** Dependent features are most likely to need updates

**Actions:**
1. Identify features that directly use just-completed feature's interfaces
2. Identify features that share data structures with just-completed feature
3. Prioritize those first
4. Then review remaining features in numerical order

**Example:**
```markdown
Just completed: feature_01_adp_integration
Created: ConfigManager.get_adp_multiplier() interface

Review order:
1. feature_02_player_rating_integration (uses similar ConfigManager pattern)
2. feature_03_schedule_strength (also uses ConfigManager)
3. feature_04_injury_risk_assessment (shares PlayerManager integration)
4. feature_05_bye_week_penalties (independent, but review for completeness)

Reasoning: Features 2-4 likely affected by ADP integration patterns
```

---

#### 1c. Create Review Checklist

**Purpose:** Track progress through alignment review

**Actions:**
1. Create simple checklist:
   ```markdown
   ## Stage 5d Alignment Review Progress

   - [ ] feature_02_player_rating_integration - Not started
   - [ ] feature_03_schedule_strength - Not started
   - [ ] feature_04_injury_risk_assessment - Not started
   - [ ] feature_05_bye_week_penalties - Not started
   ```

2. Update as you complete each feature review

---

### STEP 2: For Each Remaining Feature (Sequential Review)

**Purpose:** Compare each remaining feature's spec to actual implementation reality

**CRITICAL:** This is done ONCE per remaining feature. Work through them sequentially.

---

#### Step 2a: Read Feature Spec (Fresh Eyes)

**Actions:**
1. Open feature_XX_{name}_spec.md
2. Read it as if you've never seen it before
3. Pay attention to:
   - Interface assumptions (method signatures, parameters, return types)
   - Data structure assumptions (CSV format, JSON structure, object fields)
   - Integration assumptions (how feature will call other modules)
   - Algorithm assumptions (calculation approaches)
   - Configuration assumptions (keys in config file, default values)

**Mindset:** "Given what I now know from implementing {completed_feature}, are these assumptions still valid?"

---

#### Step 2b: Read Just-Completed Feature's Actual Code

**Actions:**
1. Open the ACTUAL code files from just-completed feature
2. Review key interfaces created:
   ```python
   # Example: If feature_01_adp_integration created:
   # ConfigManager.get_adp_multiplier(adp_value: float) -> Tuple[float, int]

   # Read ACTUAL implementation:
   def get_adp_multiplier(self, adp_value: float) -> Tuple[float, int]:
       """
       Calculate ADP multiplier based on draft position.

       Returns:
           Tuple[float, int]: (multiplier, rating_score)
       """
       # Actual implementation...
   ```

3. Note key insights from implementation:
   - Actual method signatures (not planned signatures)
   - Actual data structures used
   - Actual integration patterns
   - Actual configuration keys used
   - Actual error handling approaches
   - Actual logging patterns

---

#### Step 2c: Compare Spec Assumptions to Actual Implementation

**Purpose:** Identify where spec assumptions don't match reality

**Comparison Categories:**

**1. Interface Assumptions**
- Spec assumes: `ConfigManager.get_rating(player_id: int) -> float`
- Actual code: `ConfigManager.get_rating_multiplier(player_id: int) -> Tuple[float, int]`
- **Mismatch:** Method name different, return type different

**2. Data Structure Assumptions**
- Spec assumes: ADP data in `data/adp_rankings.csv` with columns `[player_name, adp]`
- Actual code: ADP data in `data/player_data/adp_data.csv` with columns `[name, position, team, adp_rank, adp_value]`
- **Mismatch:** File location different, column names different, additional columns

**3. Integration Pattern Assumptions**
- Spec assumes: Call ConfigManager directly from PlayerManager
- Actual code: ConfigManager accessed through DependencyInjector pattern
- **Mismatch:** Integration pattern different

**4. Configuration Assumptions**
- Spec assumes: Config key `player_rating_weights`
- Actual code: Config keys are namespaced: `scoring.player_rating.weights`
- **Mismatch:** Config key structure different

**5. Algorithm Assumptions**
- Spec assumes: Linear multiplier calculation
- Actual code: Exponential curve for top 10 picks, linear for rest
- **Mismatch:** Algorithm more complex than spec anticipated

---

#### Step 2d: Identify Misalignments and Needed Updates

**For each mismatch found, evaluate:**

**Question 1: Does this affect the remaining feature?**
- YES: Feature will need spec update
- NO: Note for awareness, but no update needed

**Question 2: How significant is the impact?**
- **Minor:** Small spec clarification (e.g., column name update)
- **Moderate:** Interface changes requiring TODO updates (e.g., method signature different)
- **Major:** Fundamental approach change (e.g., algorithm completely different)

**Question 3: What needs updating?**
- spec.md: Update algorithm description, interface details, etc.
- checklist.md: Update decisions, mark questions resolved, add new questions
- Both: Usually both need updating together

**Example - Identifying Misalignment:**
```markdown
## Review: feature_02_player_rating_integration

### Mismatch #1: ConfigManager interface
- **Spec assumption:** `ConfigManager.get_rating(player_id) -> float`
- **Actual implementation:** `ConfigManager.get_rating_multiplier(player_id) -> Tuple[float, int]`
- **Impact:** MODERATE - feature_02 spec needs method signature update
- **Significance:** 1-2 TODO task changes (update calls, handle tuple return)
- **Action:** Update spec.md section "Configuration Integration"

### Mismatch #2: Data file location
- **Spec assumption:** Rating data in `data/ratings.csv`
- **Actual implementation:** ADP used `data/player_data/adp_data.csv`
- **Impact:** MINOR - pattern established, feature_02 should follow
- **Significance:** Spec clarification only
- **Action:** Update spec.md file paths to match `data/player_data/` pattern

### Mismatch #3: Logging pattern
- **Spec assumption:** No specific logging mentioned
- **Actual implementation:** ADP used structured logging with context
- **Impact:** MINOR - good practice to follow
- **Significance:** Add logging to spec for consistency
- **Action:** Add "Logging Requirements" section to spec.md
```

---

#### Step 2e: Update Spec.md and Checklist.md

**Purpose:** Apply needed updates NOW (before implementation)

**Template for Spec Updates:**

1. **Add update note at top of relevant section:**
   ```markdown
   ## Configuration Integration

   **[UPDATED based on feature_01_adp_integration implementation - 2025-12-30]**

   The actual implementation of ADP integration revealed:
   - ConfigManager methods return Tuple[float, int] not just float
   - Second value is rating_score (0-100) for debugging
   - Methods are named `get_{metric}_multiplier` not `get_{metric}`

   Updated interface for player rating:
   ```python
   def get_rating_multiplier(self, player_id: int) -> Tuple[float, int]:
       """
       Calculate player rating multiplier.

       Args:
           player_id: Unique player identifier

       Returns:
           Tuple[float, int]: (multiplier, rating_score)
               - multiplier: float between 0.8-1.5
               - rating_score: int between 0-100 for debugging
       """
   ```

2. **Update algorithm descriptions if needed:**
   ```markdown
   ## Player Rating Calculation

   **[UPDATED based on feature_01_adp_integration - 2025-12-30]**

   Original approach assumed linear scaling. ADP implementation revealed
   that exponential curve works better for elite players. Adopting same
   pattern for player ratings:

   - Elite players (top 10%): Exponential curve
   - Average players (middle 80%): Linear scaling
   - Risky players (bottom 10%): Logarithmic penalty

   See ConfigManager.get_adp_multiplier() in league_helper/util/ConfigManager.py:234
   for reference implementation.
   ```

3. **Update data structure sections:**
   ```markdown
   ## Data Files

   **[UPDATED based on feature_01_adp_integration - 2025-12-30]**

   Player rating data should follow established pattern:
   - Location: `data/player_data/player_rating_data.csv` (not `data/ratings.csv`)
   - Columns: `[name, position, team, rating_rank, rating_value]`
   - Format: Follow same structure as adp_data.csv for consistency
   ```

4. **Update integration sections:**
   ```markdown
   ## Integration with PlayerManager

   **[UPDATED based on feature_01_adp_integration - 2025-12-30]**

   PlayerManager integration pattern established by ADP feature:

   ```python
   # In PlayerManager.calculate_total_score():
   rating_multiplier, rating_score = self.config.get_rating_multiplier(player.id)
   player.rating_multiplier = rating_multiplier  # Store for display
   player.rating_score = rating_score  # Store for debugging
   final_score *= rating_multiplier  # Apply to score
   ```

   Note: Store both values even though only multiplier affects score.
   Rating_score is useful for debugging and user transparency.
   ```

**Update Checklist.md:**

1. **Mark resolved questions:**
   ```markdown
   ## Configuration Questions
   - [x] What data format should be used? → **RESOLVED:** Follow adp_data.csv pattern
   - [x] What ConfigManager interface? → **RESOLVED:** get_rating_multiplier() returns Tuple
   ```

2. **Add new questions if implementation revealed unknowns:**
   ```markdown
   ## New Questions (from feature_01 alignment review)
   - [ ] Should rating_score (0-100) be displayed to user or just for debugging?
   - [ ] Should exponential curve coefficients match ADP or be different?
   ```

---

#### Step 2f: Mark Feature for Rework if Significant Changes

**Use "Significant Rework Criteria" (see section below)**

**If feature needs rework:**

1. **Add rework marker to spec.md:**
   ```markdown
   # Feature 02: Player Rating Integration

   **🚨 REQUIRES REWORK - Return to Stage 2 (Deep Dive)**

   **Reason:** ADP implementation revealed that player rating API has been deprecated.
   Original spec assumes API is available, but actual investigation shows API
   was shut down in 2024. Need to redesign approach using alternative data source.

   **Discovered during:** Stage 5d alignment review after feature_01 completion

   **Next steps:**
   1. Return to Stage 2 (Deep Dive)
   2. Research alternative player rating sources
   3. Update spec with new approach
   4. Get user approval before proceeding to implementation
   ```

2. **Update epic EPIC_README.md:**
   ```markdown
   ## Features Needing Rework

   **feature_02_player_rating_integration** - Return to Stage 2
   - Reason: Player rating API deprecated, need alternative source
   - Discovered: Stage 5d after feature_01
   - Impact: Requires fundamental redesign of rating integration approach
   ```

3. **Update Epic Checklist:**
   ```markdown
   **Stage 5 Progress:**
   - [x] feature_01_adp_integration (Stage 5c complete)
   - [ ] feature_02_player_rating_integration (REQUIRES REWORK - Stage 2)
   - [ ] feature_03_schedule_strength (pending Stage 5a)
   - [ ] feature_04_injury_risk_assessment (pending Stage 5a)
   ```

---

#### Step 2 Completion Per Feature

After completing steps 2a-2f for ONE feature:

1. **Update review checklist:**
   ```markdown
   ## Stage 5d Alignment Review Progress
   - [x] feature_02_player_rating_integration - COMPLETE (minor updates applied)
   - [ ] feature_03_schedule_strength - Not started
   - [ ] feature_04_injury_risk_assessment - Not started
   - [ ] feature_05_bye_week_penalties - Not started
   ```

2. **Commit spec/checklist changes:**
   ```bash
   git add feature-updates/epic_name/feature_02_player_rating_integration/
   git commit -m "Update feature_02 spec based on feature_01 implementation

   - Updated ConfigManager interface to return Tuple[float, int]
   - Updated data file location to data/player_data/ pattern
   - Added logging requirements for consistency
   - Updated integration pattern to match ADP implementation"
   ```

3. **Move to next remaining feature** (repeat Step 2 for next feature)

---

### STEP 3: Handle Features Needing Rework

**Purpose:** Properly route features that need significant changes back to appropriate stage

**This step runs AFTER reviewing all remaining features**

---

#### 3a. Review Significant Rework Criteria

**Use these criteria to determine which stage to return to:**

**Return to Stage 1 (Epic Planning):**
- [ ] Feature should be split into 2+ separate features
- [ ] Feature is no longer needed (requirements changed)
- [ ] Feature scope expanded so much it's now multiple features
- [ ] Feature revealed NEW features needed that weren't in original epic

**Example:** "Player rating integration discovered we need 3 separate features: rating_collection, rating_processing, rating_application"

---

**Return to Stage 2 (Deep Dive):**
- [ ] Spec assumptions fundamentally wrong
- [ ] Core approach needs complete redesign
- [ ] External dependency missing/changed (API deprecated, data source unavailable)
- [ ] Implementation revealed approach won't work

**Example:** "Player rating API is deprecated, need completely different source"

---

**Return to Stage 5a (TODO Creation):**
- [ ] Spec changes require >3 new TODO tasks
- [ ] Algorithm changes significantly (but core approach still valid)
- [ ] Interface changes affect multiple integration points
- [ ] Data structure changes require reworking TODO list

**Example:** "ConfigManager interface changed from returning float to Tuple, need to add 5 TODO tasks to handle tuple unpacking across all callsites"

---

**Minor Updates (Continue normally):**
- [ ] Spec clarifications requiring ≤3 TODO task adjustments
- [ ] No algorithm changes
- [ ] Interface updates are small (parameter rename, etc.)
- [ ] Just following established patterns from completed feature

**Example:** "Update data file path to match established pattern, add 2 TODO tasks for path changes"

---

#### 3b. Get User Approval for Major Rework

**If ANY feature needs to return to Stage 1 or 2:**

**DO NOT proceed automatically - ask user first**

**Template:**
```markdown
After reviewing remaining feature specs based on feature_01 implementation, I found:

## feature_02_player_rating_integration REQUIRES MAJOR REWORK

**Issue:** Player rating API (original data source) was deprecated in 2024.
Original spec assumed this API would be available.

**Impact:** Cannot implement as spec currently written

**Recommendation:** Return to Stage 2 (Deep Dive)
- Research alternative player rating sources
- Redesign integration approach
- Update spec with new approach
- Then proceed to Stage 5a with updated plan

**Options:**
1. Return to Stage 2 for feature_02 (recommended)
2. Remove feature_02 from epic entirely
3. Defer feature_02 to future epic

What would you like to do?
```

**Wait for user response before proceeding**

---

#### 3c. Update Epic Documentation

**Update EPIC_README.md:**

```markdown
## Current Status

**Last Updated:** 2025-12-30 16:00

**Completed Features:**
- [x] feature_01_adp_integration (Stage 5c complete)

**Features in Progress:**
- feature_02_player_rating_integration (RETURNED TO STAGE 2 - API deprecated)

**Pending Features:**
- feature_03_schedule_strength (Stage 5a ready)
- feature_04_injury_risk_assessment (Stage 5a ready)
- feature_05_bye_week_penalties (Stage 5a ready)

**Features Needing Rework:**
- feature_02_player_rating_integration:
  - Status: Returned to Stage 2 (Deep Dive)
  - Reason: Player rating API deprecated, need alternative source
  - User approved: 2025-12-30
  - Will resume after completing other features
```

---

### STEP 4: Final Verification

**Purpose:** Confirm all alignment work is complete before proceeding to Stage 5e

---

#### Final Verification Checklist

**All Remaining Features Reviewed:**
- [ ] Every remaining feature in review checklist marked complete
- [ ] No features skipped or missed
- [ ] Each feature's spec.md reviewed against actual implementation
- [ ] Each feature's checklist.md updated if needed

**Spec Updates Applied:**
- [ ] All identified misalignments documented
- [ ] All needed spec.md updates applied
- [ ] All needed checklist.md updates applied
- [ ] Update notes include "UPDATED based on {feature_name}" markers
- [ ] All spec updates committed to git

**Features Needing Rework Handled:**
- [ ] Significant rework criteria applied consistently
- [ ] Features marked for rework have clear markers in spec.md
- [ ] User approval obtained for any major rework (Stage 1 or 2 returns)
- [ ] Epic README updated with rework status

**Epic Documentation Updated:**
- [ ] EPIC_README.md reflects current status
- [ ] Epic checklist shows any features needing rework
- [ ] "Features Needing Rework" section exists if applicable
- [ ] Next steps are clear

**Git Status:**
- [ ] All spec/checklist updates committed
- [ ] Commit messages describe alignment updates
- [ ] Working directory clean

**README Agent Status:**
- [ ] Updated with Stage 5d completion
- [ ] Next action set to "Stage 5e: Testing Plan Update"

**If ALL boxes checked:** Ready to proceed to Stage 5e

**If ANY box unchecked:** Complete missing items before proceeding

---

### 🔄 Re-Reading Checkpoint

**STOP - Before declaring Stage 5d complete:**

1. Re-read "Critical Rules" section at top of this guide
2. Verify you compared to ACTUAL implementation (not plan)
3. Verify you updated specs PROACTIVELY (not just noted issues)
4. Verify ALL remaining features were reviewed (not just "related" ones)
5. Update README Agent Status:
   ```
   Guide Last Re-Read: {timestamp}
   Checkpoint: Stage 5d complete, all remaining specs aligned
   Current Phase: TESTING_PLAN_UPDATE (Stage 5e)
   Next Action: Read STAGE_5e_post_feature_testing_update_guide.md
   ```

---

## Significant Rework Criteria (Detailed)

**Purpose:** Clear decision tree for routing features that need changes

---

### Criteria Table

| Condition | Return To | Reason | Example |
|-----------|-----------|--------|---------|
| Feature should be split into 2+ features | **Stage 1** | Epic structure changes | "Player rating" became "rating_collection", "rating_processing", "rating_application" |
| Feature no longer needed | **Stage 1** | Epic scope changes | Implementation revealed feature is redundant with existing system |
| NEW feature discovered | **Stage 1** | Epic expansion | "Need authentication feature we didn't plan for" |
| Core approach fundamentally wrong | **Stage 2** | Requires redesign | "Player rating API deprecated, need different source" |
| Spec assumptions invalid | **Stage 2** | Research needed | "Assumed CSV format, but API returns JSON only" |
| External dependency missing | **Stage 2** | Alternative needed | "Required library no longer maintained" |
| Algorithm needs major change | **Stage 2** | Approach redesign | "Linear scaling won't work, need ML model" |
| >3 new TODO tasks needed | **Stage 5a** | TODO list rework | "Interface change affects 7 callsites" |
| Algorithm change (same approach) | **Stage 5a** | TODO updates | "Add caching layer, 4 new TODO tasks" |
| Interface signature changes | **Stage 5a** | Integration updates | "Method now returns Tuple not float, update callers" |
| ≤3 TODO adjustments | **Continue** | Minor updates | "Update file path, add 2 tasks" |
| Pattern following | **Continue** | Consistency | "Follow established ConfigManager pattern" |
| No algorithm changes | **Continue** | Clarification only | "Column name updated in spec" |

---

### Decision Tree

```
Did implementation reveal changes needed?
    │
    ├─ NO → Continue with feature (no rework needed)
    │
    └─ YES → Evaluate impact:
         │
         ├─ Should feature be split into multiple features?
         │   └─ YES → Return to Stage 1 (Epic Planning)
         │
         ├─ Is feature no longer needed?
         │   └─ YES → Return to Stage 1 (get user approval to remove)
         │
         ├─ Are spec assumptions fundamentally wrong?
         │   └─ YES → Return to Stage 2 (Deep Dive)
         │
         ├─ Is external dependency missing/changed?
         │   └─ YES → Return to Stage 2 (find alternative)
         │
         ├─ Does algorithm need complete redesign?
         │   └─ YES → Return to Stage 2 (rethink approach)
         │
         ├─ Will spec changes require >3 new TODO tasks?
         │   └─ YES → Return to Stage 5a (TODO Creation)
         │
         ├─ Did algorithm change significantly (but approach valid)?
         │   └─ YES → Return to Stage 5a (update TODO list)
         │
         └─ Minor updates (≤3 TODO tasks, no algorithm change)?
             └─ YES → Continue (update spec, proceed normally)
```

---

### Real-World Examples

**Example 1: Return to Stage 1**
```
Just completed: feature_01_adp_integration

Reviewing: feature_02_player_rating_integration

Finding: Rating integration actually needs 3 separate features:
  1. rating_data_collection (fetch from API)
  2. rating_calculation (compute ratings from stats)
  3. rating_integration (apply to scoring)

Original spec tried to do all 3 in one feature (too large, complex).

Decision: RETURN TO STAGE 1
- Split feature_02 into 3 features
- Update epic structure
- User approves split
- Continue with new feature breakdown
```

---

**Example 2: Return to Stage 2**
```
Just completed: feature_01_adp_integration

Reviewing: feature_03_schedule_strength

Finding: Spec assumes NFL schedule data available via API endpoint
Implementation check: API endpoint returns 404 (no longer exists)

Root cause: NFL changed API in 2025, old endpoint deprecated

Decision: RETURN TO STAGE 2
- Research alternative schedule data sources
- Identify web scraping vs paid API options
- Get user decision on approach
- Update spec with new source
- Then proceed to Stage 5a
```

---

**Example 3: Return to Stage 5a**
```
Just completed: feature_01_adp_integration

Reviewing: feature_04_injury_risk_assessment

Finding: Spec assumes ConfigManager.get_injury_penalty(status: str) -> float
Actual: ConfigManager methods return Tuple[float, int] (established by ADP)

Impact analysis:
- Need to update 7 callsites to handle tuple unpacking
- Need to add injury_score display in UI (new)
- Need to add injury_score to CSV output (new)
- Need to add injury_score to tests (new)
Total: 6 new TODO tasks

Decision: RETURN TO STAGE 5a
- Update spec with correct interface
- Recreate TODO list with 6 additional tasks
- Then proceed with implementation
```

---

**Example 4: Continue (Minor Updates)**
```
Just completed: feature_01_adp_integration

Reviewing: feature_05_bye_week_penalties

Finding: Spec has data file at `data/bye_weeks.csv`
Pattern: ADP used `data/player_data/adp_data.csv`
Update: Should be `data/player_data/bye_week_data.csv` for consistency

Impact analysis:
- File path change in 2 places (load and save)
- Column names stay same
- No algorithm changes
Total: 2 minor TODO adjustments

Decision: CONTINUE (Minor Updates)
- Update spec.md with correct file path
- Note in spec: "Following data/player_data/ pattern from feature_01"
- Proceed to Stage 5a normally
- Existing TODO list still mostly valid
```

---

## Completion Criteria

**Stage 5d is complete when ALL of the following are true:**

### All Features Reviewed
- [x] Every remaining (not-yet-implemented) feature reviewed
- [x] No features skipped
- [x] Review checklist 100% complete

### Comparisons Done
- [x] Each feature spec compared to ACTUAL implementation (not plan)
- [x] Actual code reviewed (not just assumptions)
- [x] Interfaces verified from source code
- [x] Data structures verified from actual files
- [x] Integration patterns verified from actual implementation

### Spec Updates Applied
- [x] All identified misalignments documented
- [x] All spec.md files updated proactively
- [x] All checklist.md files updated
- [x] Update notes include "UPDATED based on {feature}" markers
- [x] Changes explain WHY update was needed

### Rework Handled
- [x] Significant rework criteria applied to all features
- [x] Features needing rework clearly marked in spec.md
- [x] User approval obtained for major rework (Stage 1 or 2)
- [x] Epic README updated with rework status

### Documentation Updated
- [x] EPIC_README.md reflects current status
- [x] Epic checklist updated
- [x] "Features Needing Rework" section exists (if applicable)
- [x] Next steps clear for all features

### Git Status
- [x] All spec/checklist updates committed
- [x] Descriptive commit messages
- [x] Working directory clean

### README Agent Status
- [x] Updated to reflect Stage 5d completion
- [x] Next action set to "Read STAGE_5e_post_feature_testing_update_guide.md"

**If ALL criteria met:** Proceed to Stage 5e (Testing Plan Update)

**If ANY criteria not met:** Do NOT proceed until all are met

---

## Common Mistakes to Avoid

### Anti-Pattern 1: Reviewing Only "Related" Features

**Mistake:**
"Feature_01 was ADP integration, so I'll only review feature_02 (player ratings) since they're both scoring multipliers. Feature_03 (schedule strength) is unrelated, I'll skip it."

**Why it's wrong:** Implementation insights can affect unexpected features. Maybe ADP integration revealed ConfigManager patterns that ALL features should follow.

**Correct approach:** Review ALL remaining features, no exceptions. Takes 10 minutes per feature, prevents hours of rework.

---

### Anti-Pattern 2: Comparing to Plan Instead of Code

**Mistake:**
"According to the TODO list, feature_01 was supposed to use ConfigManager.get_adp(), so feature_02 should use ConfigManager.get_rating(). No update needed."

**Why it's wrong:** Plans change during implementation. Actual code might be different.

**Correct approach:** READ THE ACTUAL CODE. Don't assume implementation matches plan.

**Example:**
```python
# Plan said:
ConfigManager.get_adp(player_id) -> float

# Actual code:
ConfigManager.get_adp_multiplier(player_id) -> Tuple[float, int]

# If you compared to plan, you'd miss the signature difference
```

---

### Anti-Pattern 3: Noting Issues But Not Updating Specs

**Mistake:**
"I found that feature_02 spec assumes wrong interface. I'll just make a note in my head and fix it during implementation."

**Why it's wrong:** You'll forget, or next agent won't know. Spec becomes outdated.

**Correct approach:** UPDATE SPEC NOW. Add clear notes about what changed and why.

---

### Anti-Pattern 4: "Probably Fine" Assumptions

**Mistake:**
"Feature_02 spec mentions ConfigManager.get_rating(), feature_01 created get_adp_multiplier(). Probably similar pattern, probably fine."

**Why it's wrong:** "Probably" is not verification. Takes 30 seconds to check actual code.

**Correct approach:** Open the actual source file. Read the actual method signature. Verify, don't assume.

---

### Anti-Pattern 5: Not Getting User Approval for Major Rework

**Mistake:**
"Feature_02 needs to return to Stage 2 because API is deprecated. I'll just go back to Stage 2 and start researching alternatives."

**Why it's wrong:** Major rework decisions should involve user. Maybe they want to remove the feature entirely, or defer it, or have a preferred alternative.

**Correct approach:** Present finding to user, get approval for approach before proceeding.

---

### Anti-Pattern 6: Batch Updates Without Review

**Mistake:**
"I'll update all 4 feature specs at once, then commit everything together."

**Why it's wrong:** Easy to miss nuances when batch processing. Each feature deserves focused attention.

**Correct approach:** Review and update ONE feature at a time. Commit after each. Sequential, focused work.

---

### Anti-Pattern 7: Ignoring checklist.md

**Mistake:**
"I updated spec.md with new interface. Checklist.md doesn't matter, I'll skip it."

**Why it's wrong:** Checklist.md tracks decisions and questions. If you update spec, you should mark corresponding checklist items.

**Correct approach:** Update BOTH spec.md AND checklist.md for each feature.

---

### Anti-Pattern 8: Vague Update Notes

**Mistake:**
```markdown
## Configuration Integration

[Updated]

Use ConfigManager for ratings.
```

**Why it's wrong:** Doesn't say WHAT changed or WHY. Future agent won't understand.

**Correct approach:** Specific update notes:
```markdown
## Configuration Integration

**[UPDATED based on feature_01_adp_integration implementation - 2025-12-30]**

Changed interface from `get_rating() -> float` to `get_rating_multiplier() -> Tuple[float, int]`
to match pattern established by ADP integration. Second value is rating_score for debugging.

See ConfigManager.get_adp_multiplier() at league_helper/util/ConfigManager.py:234 for reference.
```

---

### Anti-Pattern 9: Skipping Git Commits

**Mistake:**
"I'll update all feature specs and commit once at the end of Stage 5d."

**Why it's wrong:** If something goes wrong, you lose all work. Can't track which feature caused issues.

**Correct approach:** Commit after EACH feature spec update. Atomic commits = better history.

---

### Anti-Pattern 10: Unclear Rework Marking

**Mistake:**
```markdown
# Feature 02: Player Rating Integration

Note: This might need updates.
```

**Why it's wrong:** "Might need updates" is vague. Does it need rework or not? Which stage?

**Correct approach:** Clear rework marking:
```markdown
# Feature 02: Player Rating Integration

**🚨 REQUIRES REWORK - Return to Stage 2 (Deep Dive)**

**Reason:** Player rating API deprecated in 2024, need alternative data source.

**Discovered during:** Stage 5d alignment review after feature_01 completion

**User approved:** 2025-12-30

**Next steps:** Research alternative sources, update spec, get user approval, then Stage 5a
```

---

## Real-World Examples

### Example 1: Interface Pattern Discovered During Implementation

**Just completed:** feature_01_adp_integration

**Reviewing:** feature_02_player_rating_integration, feature_03_schedule_strength, feature_04_injury_risk

**Finding:**

Original specs assumed each feature would call ConfigManager with simple method:
```python
# feature_02 spec:
rating = config.get_rating(player.id)

# feature_03 spec:
strength = config.get_schedule_strength(player.team)

# feature_04 spec:
risk = config.get_injury_risk(player.injury_status)
```

**Actual implementation in feature_01:**
```python
# Actual code in ConfigManager.py:
def get_adp_multiplier(self, adp_value: float) -> Tuple[float, int]:
    """
    Calculate ADP multiplier and rating score.

    Returns:
        Tuple[float, int]: (multiplier, rating_score)
            - multiplier: Applied to player score
            - rating_score: 0-100 for debugging/display
    """
    # Implementation...
```

**Insight:** ConfigManager methods return Tuple[multiplier, score] for transparency and debugging.

**Action for feature_02:**
```markdown
## Configuration Integration

**[UPDATED based on feature_01_adp_integration implementation - 2025-12-30]**

ConfigManager methods follow pattern of returning Tuple[float, int] where:
- First value: multiplier to apply to score
- Second value: 0-100 rating for debugging/transparency

Updated interface:
```python
def get_rating_multiplier(self, player_id: int) -> Tuple[float, int]:
    """
    Calculate player rating multiplier.

    Returns:
        Tuple[float, int]: (rating_multiplier, rating_score)
    """
```

Integration in PlayerManager:
```python
rating_multiplier, rating_score = self.config.get_rating_multiplier(player.id)
player.rating_multiplier = rating_multiplier  # For scoring
player.rating_score = rating_score  # For display/debugging
final_score *= rating_multiplier
```

See feature_01 implementation in ConfigManager.py:234 for pattern reference.
```

**Result:**
- feature_02: Minor update (continue to Stage 5a normally)
- feature_03: Minor update (continue to Stage 5a normally)
- feature_04: Minor update (continue to Stage 5a normally)
- All 3 features now aligned with established pattern
- Saves hours of rework during implementation

---

### Example 2: Data Source Unavailable - Major Rework Needed

**Just completed:** feature_01_adp_integration (used ESPN API)

**Reviewing:** feature_03_schedule_strength

**Original spec assumption:**
```markdown
## Data Source

Schedule strength data will be fetched from NFL Official Stats API:
- Endpoint: https://api.nfl.com/stats/schedule
- Authentication: API key from user config
- Format: JSON with team schedules and opponent rankings
```

**Verification during alignment review:**
```bash
# Test API endpoint
curl https://api.nfl.com/stats/schedule
# Result: 404 Not Found

# Research: API was deprecated in 2024
# NFL now requires paid subscription for official stats
```

**Impact:**
- Original approach not viable
- Need alternative data source
- Spec assumptions fundamentally wrong

**Decision:** Return to Stage 2 (Deep Dive)

**User communication:**
```markdown
After reviewing feature_03 spec based on feature_01 implementation, I discovered:

## feature_03_schedule_strength REQUIRES MAJOR REWORK

**Issue:** NFL Official Stats API (spec's assumed data source) was deprecated in 2024.
Current endpoint returns 404. NFL now requires paid subscription ($500/month) for official data.

**Impact:** Cannot implement as spec currently written

**Recommendation:** Return to Stage 2 (Deep Dive) to research alternatives:

**Option 1:** Use ESPN API (same source as feature_01 uses for ADP data)
- Pros: Free, accessible, already integrated
- Cons: Less detailed than NFL official stats

**Option 2:** Use Pro Football Reference web scraping
- Pros: Comprehensive data, free
- Cons: Fragile (HTML changes break scraper), legally grey

**Option 3:** Use paid API subscription
- Pros: Official data, reliable
- Cons: $500/month cost

What would you like to do?
1. Return to Stage 2 to research ESPN API option (recommended)
2. Return to Stage 2 to evaluate web scraping
3. Defer feature_03 until budget available for paid API
4. Remove feature_03 from epic entirely
```

**User response:** "Go with Option 1, use ESPN API"

**Action:**
1. Mark feature_03 spec with rework status
2. Update epic README showing feature_03 returned to Stage 2
3. Continue reviewing feature_04 (don't let rework block other reviews)
4. After completing Stage 5d for all features, return to feature_03 Stage 2

---

### Example 3: Minor Updates Applied Proactively

**Just completed:** feature_01_adp_integration

**Reviewing:** feature_05_bye_week_penalties

**Original spec:**
```markdown
## Data Files

Bye week data stored in:
- Location: `data/bye_weeks.csv`
- Columns: `[team, bye_week]`
- Format: CSV with header row

## Configuration

Bye week penalty stored in:
- Config key: `penalties.bye_week`
- Type: float (negative value)
- Default: -5.0
```

**Actual implementation from feature_01:**
```python
# File location pattern established:
ADP_DATA_FILE = data_folder / "player_data" / "adp_data.csv"

# Config key pattern established:
self.config['scoring']['adp']['multiplier_curve']
```

**Comparison:**
- File location: Spec has `data/bye_weeks.csv`, pattern is `data/player_data/`
- Config key: Spec has `penalties.bye_week`, pattern is `scoring.{feature}.{setting}`

**Impact:** MINOR - just following established patterns for consistency

**Updates applied:**
```markdown
## Data Files

**[UPDATED based on feature_01_adp_integration implementation - 2025-12-30]**

Following established pattern from feature_01, bye week data stored in:
- Location: `data/player_data/bye_week_data.csv` (not `data/bye_weeks.csv`)
- Columns: `[team, bye_week]`
- Format: CSV with header row

Rationale: All player-related data in `data/player_data/` subdirectory for organization.

## Configuration

**[UPDATED based on feature_01_adp_integration implementation - 2025-12-30]**

Following established pattern from feature_01, bye week configuration:
- Config key: `scoring.bye_week.penalty` (not `penalties.bye_week`)
- Type: float (negative value)
- Default: -5.0

Rationale: All scoring-related settings under `scoring` namespace for consistency.
```

**Checklist.md updates:**
```markdown
## Configuration Questions
- [x] What config key structure? → **RESOLVED:** Follow `scoring.{feature}.{setting}` pattern from feature_01
- [x] Where to store data files? → **RESOLVED:** Use `data/player_data/` pattern from feature_01
```

**Result:**
- feature_05: Minor updates, continue to Stage 5a normally
- Spec now aligned with established patterns
- Prevents "why is this different?" questions during implementation

**Commit:**
```bash
git commit -m "Update feature_05 spec to follow feature_01 patterns

- Data file location: data/player_data/bye_week_data.csv
- Config key: scoring.bye_week.penalty
- Ensures consistency across epic features"
```

---

## README Agent Status Update Requirements

**Update README Agent Status at these points:**

### At Start of Stage 5d
```markdown
**Current Phase:** CROSS_FEATURE_ALIGNMENT
**Current Guide:** STAGE_5d_post_feature_alignment_guide.md
**Guide Last Read:** 2025-12-30 16:00
**Critical Rules:** "Compare to ACTUAL implementation", "Update specs proactively", "Review ALL remaining features"
**Next Action:** Identify remaining features and create review checklist
**Completed Feature:** feature_01_adp_integration (just completed Stage 5c)
```

### During Review (after each feature)
```markdown
**Current Phase:** CROSS_FEATURE_ALIGNMENT
**Current Guide:** STAGE_5d_post_feature_alignment_guide.md
**Guide Last Read:** 2025-12-30 16:00
**Progress:** Reviewed 2/4 remaining features
**Completed Reviews:**
- feature_02_player_rating_integration (minor updates applied)
- feature_03_schedule_strength (REQUIRES REWORK - Stage 2)
**Next Action:** Review feature_04_injury_risk_assessment spec
```

### At Completion of Stage 5d
```markdown
**Current Phase:** TESTING_PLAN_UPDATE (Stage 5e)
**Previous Guide:** STAGE_5d_post_feature_alignment_guide.md (COMPLETE)
**Current Guide:** STAGE_5e_post_feature_testing_update_guide.md (NOT YET READ)
**Guide Last Read:** {Not read yet}
**Critical Rules:** {To be determined after reading Stage 5e guide}
**Next Action:** Read STAGE_5e_post_feature_testing_update_guide.md and use phase transition prompt
**Stage 5d Summary:**
- Reviewed 4 remaining features
- Applied minor updates to features 2, 4, 5
- Marked feature 3 for Stage 2 rework (user approved)
- All remaining specs now aligned with feature_01 implementation
**Stage 5d Completion:** 2025-12-30 16:45
```

---

## Prerequisites for Next Stage

**Before transitioning to Stage 5e (Testing Plan Update), verify:**

### Completion Verification
- [ ] All Stage 5d completion criteria met (see Completion Criteria section)
- [ ] All remaining features reviewed
- [ ] All needed spec updates applied
- [ ] Features needing rework properly marked
- [ ] User approval obtained for major rework

### Files Updated
- [ ] All affected spec.md files updated
- [ ] All affected checklist.md files updated
- [ ] EPIC_README.md updated with current status
- [ ] Git commits describe alignment updates

### Documentation Clear
- [ ] "Features Needing Rework" section exists (if applicable)
- [ ] Next steps clear for all features
- [ ] Update notes include reasons and references

### README Agent Status
- [ ] Updated to reflect Stage 5d completion
- [ ] Next action set to "Read STAGE_5e_post_feature_testing_update_guide.md"

**If ALL verified:** Ready for Stage 5e

**Stage 5e Preview:**
- Review epic_smoke_test_plan.md
- Update test scenarios based on ACTUAL implementation of just-completed feature
- Add integration points discovered during implementation
- Keep testing plan current as epic evolves

**Next step:** Read STAGE_5e_post_feature_testing_update_guide.md and use phase transition prompt

---

## Summary

**Stage 5d ensures remaining feature specs align with implementation reality through:**

1. **Comprehensive Review** - ALL remaining features reviewed (not just "related" ones)
2. **Actual Implementation Comparison** - Compare specs to ACTUAL code (not plans)
3. **Proactive Updates** - Update specs NOW (before implementation) to reflect reality
4. **Significant Rework Identification** - Clear criteria for routing features back to appropriate stage
5. **User Approval for Major Changes** - Get sign-off before major rework

**Critical protocols:**
- Review ALL remaining features sequentially
- Compare to ACTUAL implementation (read the code)
- Update specs proactively (don't defer)
- Use clear rework criteria (Stage 1, 2, or 5a)
- Get user approval for major changes

**Success criteria:**
- All remaining features reviewed
- All needed spec updates applied
- Features needing rework properly marked and routed
- Epic documentation current
- Ready for Stage 5e (Testing Plan Update)

**Why this matters:** Plans change during implementation. Code reveals insights specs couldn't predict. Stage 5d keeps remaining features aligned with reality, preventing costly rework during implementation.

---

*End of STAGE_5d_post_feature_alignment_guide.md*
