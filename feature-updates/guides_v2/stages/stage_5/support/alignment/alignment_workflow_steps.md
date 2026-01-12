# Stage 5d: Cross-Feature Alignment - Detailed Workflow Steps

**Purpose:** Step-by-step process for reviewing remaining features and updating specs based on actual implementation
**Prerequisites:** Stage 5d overview read from post_feature_alignment.md
**Main Guide:** `stages/stage_5/post_feature_alignment.md`

---

## Overview

This reference provides the detailed workflow for Stage 5d (Cross-Feature Alignment). After completing a feature, you review ALL remaining (not-yet-implemented) feature specs to ensure they align with the ACTUAL implementation (not just the plan).

**Key Principle:** Compare to ACTUAL implementation, not the plan.

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
- **Significance:** 1-2 implementation task changes (update calls, handle tuple return)
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

**Use "Significant Rework Criteria" (see rework_criteria_examples.md)**

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

**Return to Stage 5a (Implementation Planning):**
- [ ] Spec changes require >3 new implementation tasks
- [ ] Algorithm changes significantly (but core approach still valid)
- [ ] Interface changes affect multiple integration points
- [ ] Data structure changes require reworking implementation plan

**Example:** "ConfigManager interface changed from returning float to Tuple, need to add 5 implementation tasks to handle tuple unpacking across all callsites"

---

**Minor Updates (Continue normally):**
- [ ] Spec clarifications requiring ≤3 implementation task adjustments
- [ ] No algorithm changes
- [ ] Interface updates are small (parameter rename, etc.)
- [ ] Just following established patterns from completed feature

**Example:** "Update data file path to match established pattern, add 2 implementation tasks for path changes"

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

1. Re-read "Critical Rules" section at top of main guide
2. Verify you compared to ACTUAL implementation (not plan)
3. Verify you updated specs PROACTIVELY (not just noted issues)
4. Verify ALL remaining features were reviewed (not just "related" ones)
5. Update README Agent Status:
   ```
   Guide Last Re-Read: {timestamp}
   Checkpoint: Stage 5d complete, all remaining specs aligned
   Current Phase: TESTING_PLAN_UPDATE (Stage 5e)
   Next Action: Read stages/stage_5/post_feature_testing_update.md
   ```

---

**END OF ALIGNMENT WORKFLOW STEPS**
