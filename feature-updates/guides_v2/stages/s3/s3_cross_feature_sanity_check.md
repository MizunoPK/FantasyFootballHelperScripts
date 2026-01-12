# S3: Cross-Feature Sanity Check Guide

🚨 **MANDATORY READING PROTOCOL**

**Before starting this guide:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update epic EPIC_README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check epic EPIC_README.md Agent Status for current phase
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Quick Start

**What is this stage?**
Cross-Feature Sanity Check is where you systematically compare all feature specs to identify conflicts, resolve inconsistencies, and get user sign-off on the complete epic plan before proceeding to implementation.

**When do you use this guide?**
- ALL features have completed S2 (Feature Deep Dives)
- All feature specs are documented
- Ready to validate epic-wide consistency

**Key Outputs:**
- ✅ Feature comparison matrix created (systematic pairwise comparison)
- ✅ All conflicts identified and resolved
- ✅ Specs updated to resolve conflicts
- ✅ User sign-off obtained on complete epic plan
- ✅ Ready for S4 (Epic Testing Strategy)

**Time Estimate:**
30-60 minutes for entire epic (scales with number of features)

**Exit Condition:**
S3 is complete when all feature specs are conflict-free, user has explicitly approved the complete plan, and approval is documented in EPIC_README.md

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL features must complete S2 before starting S3
   - Check epic EPIC_README.md Feature Tracking table
   - Every feature must show "[x]" in "S2 Complete"

2. ⚠️ Compare ALL features systematically (not just some)
   - Use comparison matrix
   - Check every category for every feature pair

3. ⚠️ Document ALL conflicts found (even if seem minor)
   - Small conflicts become big bugs
   - Create conflict report in epic/research/

4. ⚠️ Resolve conflicts BEFORE getting user sign-off
   - Do NOT present unresolved conflicts to user
   - Update affected specs to resolve conflicts

5. ⚠️ User sign-off is MANDATORY
   - Present complete plan
   - User must explicitly approve
   - Document approval in epic EPIC_README.md

6. ⚠️ Cannot proceed to S4 without user approval
   - Mark as blocker in Agent Status if waiting

7. ⚠️ If user requests changes, implement and RE-RUN sanity check
   - User changes might create NEW conflicts
   - Verify alignment after changes

8. ⚠️ Update epic EPIC_README.md Epic Completion Checklist
   - Mark S3 items complete
   - Document user sign-off date
```

---

## Prerequisites Checklist

**Verify BEFORE starting S3:**

□ ALL features have completed S2 - verified in epic EPIC_README.md Feature Tracking table
□ Every feature has:
  - Complete spec.md with all sections filled
  - All checklist.md items resolved (no open questions)
  - Per-feature alignment check performed (Phase 5 of S2)
□ Epic EPIC_README.md shows:
  - Every feature with "[x]" in "S2 Complete" column
  - No features with "Not started" or "In progress" status
□ No blockers or waiting states in any feature README.md

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with S3
- Return to S2 for incomplete features
- Update Agent Status with blocker

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    STAGE 3 WORKFLOW                          │
└──────────────────────────────────────────────────────────────┘

Step 1: Prepare Comparison Matrix
   ├─ List all features
   ├─ List comparison categories
   └─ Create comparison template

Step 2: Systematic Comparison
   ├─ Compare features pairwise across categories:
   │  ├─ Data Structures
   │  ├─ Interfaces & Dependencies
   │  ├─ File Locations & Naming
   │  ├─ Configuration Keys
   │  ├─ Algorithms & Logic
   │  └─ Testing Assumptions
   └─ Document conflicts in comparison matrix

Step 3: Conflict Resolution
   ├─ For EACH conflict:
   │  ├─ Determine correct approach
   │  ├─ Update affected feature specs
   │  └─ Document resolution
   └─ Verify no new conflicts created by resolutions

Step 4: Create Final Plan Summary
   ├─ Summarize all features
   ├─ Document dependencies
   ├─ Recommended implementation order
   └─ Risk assessment

Step 5: User Sign-Off
   ├─ Present plan to user
   ├─ WAIT for explicit approval
   ├─ If changes requested: implement and re-run sanity check
   └─ Document approval in epic EPIC_README.md

Step 6: Mark S3 Complete
   ├─ Update epic EPIC_README.md
   └─ Transition to S4
```

---

## Step 1: Prepare Comparison Matrix

### Step 1.1: List All Features

From epic EPIC_README.md Feature Tracking table:

```
Features to compare:
1. feature_01_adp_integration
2. feature_02_injury_assessment
3. feature_03_schedule_analysis
4. feature_04_recommendation_updates
```

### Step 1.2: Create Comparison Template

Create `epic/research/SANITY_CHECK_{DATE}.md`:

```markdown
# Cross-Feature Sanity Check

**Date:** {YYYY-MM-DD}
**Epic:** {epic_name}
**Features Compared:** {N} features

---

## Comparison Matrix

### Category 1: Data Structures

| Feature | Data Added | Field Names | Data Types | Conflicts? |
|---------|-----------|-------------|------------|------------|
| Feature 1 | | | | |
| Feature 2 | | | | |
| Feature 3 | | | | |
| Feature 4 | | | | |

### Category 2: Interfaces & Dependencies

| Feature | Depends On | Calls Methods | Return Types Expected | Conflicts? |
|---------|-----------|---------------|----------------------|------------|
| Feature 1 | | | | |
| Feature 2 | | | | |
| Feature 3 | | | | |
| Feature 4 | | | | |

### Category 3: File Locations & Naming

| Feature | Creates Files | File Locations | Naming Conventions | Conflicts? |
|---------|--------------|----------------|-------------------|------------|
| Feature 1 | | | | |
| Feature 2 | | | | |
| Feature 3 | | | | |
| Feature 4 | | | | |

### Category 4: Configuration Keys

| Feature | Config Keys Added | Config File | Key Conflicts? | Conflicts? |
|---------|------------------|-------------|----------------|------------|
| Feature 1 | | | | |
| Feature 2 | | | | |
| Feature 3 | | | | |
| Feature 4 | | | | |

### Category 5: Algorithms & Logic

| Feature | Algorithm Type | Multiplier/Score Impact | Order Dependencies | Conflicts? |
|---------|---------------|------------------------|-------------------|------------|
| Feature 1 | | | | |
| Feature 2 | | | | |
| Feature 3 | | | | |
| Feature 4 | | | | |

### Category 6: Testing Assumptions

| Feature | Test Data Needs | Mock Dependencies | Integration Points | Conflicts? |
|---------|----------------|-------------------|-------------------|------------|
| Feature 1 | | | | |
| Feature 2 | | | | |
| Feature 3 | | | | |
| Feature 4 | | | | |

---

## Conflicts Identified

{Will populate during Step 2}

---

## Resolutions Applied

{Will populate during Step 3}
```

---

## Step 2: Systematic Comparison

### Step 2.1: Compare Data Structures

**For EACH feature, read spec.md and extract:**

**Feature 1 (ADP Integration):**
```
Data Added:
- FantasyPlayer.adp_value: Optional[int]
- FantasyPlayer.adp_multiplier: float

Field Names: adp_value, adp_multiplier
Data Types: Optional[int], float
```

**Feature 2 (Injury Assessment):**
```
Data Added:
- FantasyPlayer.injury_status: str
- FantasyPlayer.injury_multiplier: float

Field Names: injury_status, injury_multiplier
Data Types: str, float
```

**Fill comparison matrix:**

| Feature | Data Added | Field Names | Data Types | Conflicts? |
|---------|-----------|-------------|------------|------------|
| Feature 1 | adp_value, adp_multiplier | adp_value, adp_multiplier | Optional[int], float | ❌ None |
| Feature 2 | injury_status, injury_multiplier | injury_status, injury_multiplier | str, float | ❌ None |
| Feature 3 | schedule_strength: float | schedule_strength | float | ❌ None |
| Feature 4 | (uses existing fields) | N/A | N/A | ❌ None |

**Check for conflicts:**
- ❌ Duplicate field names? NO
- ❌ Conflicting types for same field? NO
- ❌ Incompatible data formats? NO

**Result:** No data structure conflicts

### Step 2.2: Compare Interfaces & Dependencies

**For EACH feature, extract:**

**Feature 1:**
```
Depends On: ConfigManager.get_adp_multiplier(adp: int) -> Tuple[float, int]
Calls Methods:
- PlayerManager.load_players()
- csv_utils.read_csv_with_validation()
Return Types Expected:
- load_players() returns List[FantasyPlayer]
- get_adp_multiplier() returns Tuple[float, int]
```

**Feature 2:**
```
Depends On: ConfigManager.get_injury_penalty(status: str) -> float
Calls Methods:
- PlayerManager.load_players()
- PlayerManager.calculate_total_score()
Return Types Expected:
- load_players() returns List[FantasyPlayer]
- calculate_total_score() returns float
```

**Fill comparison matrix and check:**

**CONFLICT FOUND:**

Feature 1 expects: `load_players() -> List[FantasyPlayer]`
Feature 2 expects: `load_players() -> List[FantasyPlayer]`
✅ MATCH - No conflict

Feature 4 expects: `calculate_total_score() -> float`
But also calls it AFTER Features 1, 2, 3 add multipliers
⚠️ **POTENTIAL CONFLICT:** Order of multiplier application

**Document conflict:**

```markdown
## Conflicts Identified

### Conflict 1: Multiplier Application Order

**Category:** Algorithms & Logic

**Issue:**
- Feature 1: Adds adp_multiplier to scoring
- Feature 2: Adds injury_multiplier to scoring
- Feature 3: Adds schedule_strength multiplier to scoring
- Feature 4: Integrates all multipliers but unclear ORDER

**Current Algorithm (Feature 4 spec):**
```
total_score = base_score * adp_multiplier * injury_multiplier
```

**Problem:** Missing schedule_strength multiplier

**Impact:** Feature 3's contribution will be ignored

**Resolution Needed:** Update Feature 4 spec to include ALL multipliers
```

### Step 2.3: Compare File Locations

**Feature 1:** Creates `data/rankings/adp.csv`
**Feature 2:** Creates `data/injury_reports.csv`
**Feature 3:** Creates `data/rankings/schedule_strength.csv`

**CONFLICT FOUND:**

Feature 1: `data/rankings/adp.csv`
Feature 3: `data/rankings/schedule_strength.csv`
✅ Both in `data/rankings/` - CONSISTENT

Feature 2: `data/injury_reports.csv`
❌ In `data/` root, not `data/rankings/`

**Question:** Should all ranking/data files be in `data/` or subdirectories?

**Resolution:** Standardize location

```markdown
### Conflict 2: File Location Inconsistency

**Category:** File Locations & Naming

**Issue:**
- Feature 1: data/rankings/adp.csv (subdirectory)
- Feature 2: data/injury_reports.csv (root)
- Feature 3: data/rankings/schedule_strength.csv (subdirectory)

**Inconsistency:** Feature 2 not using subdirectory

**Resolution:** Move Feature 2 file to subdirectory
- Update Feature 2 spec: `data/player_info/injury_reports.csv`
- Reasoning: Group related data types (rankings/ vs player_info/)
```

### Step 2.4: Compare Configuration Keys

**Feature 1:** Adds config keys:
- `adp_multiplier_ranges` (dict)
- `adp_threshold` (int)

**Feature 2:** Adds config keys:
- `injury_penalty_factors` (dict)
- `injury_severity_threshold` (int)

**Feature 3:** Adds config keys:
- `schedule_strength_weight` (float)
- `schedule_threshold` (int)

**CONFLICT FOUND:**

Feature 1: `adp_threshold`
Feature 2: `injury_severity_threshold`
Feature 3: `schedule_threshold`

All add `*_threshold` keys. Are they the same type of threshold?

**Review specs:**
- Feature 1: `adp_threshold` = ADP rank cutoff (int 1-500)
- Feature 2: `injury_severity_threshold` = Severity rating (int 1-10)
- Feature 3: `schedule_threshold` = Opponent strength cutoff (int 1-32)

✅ Different thresholds for different purposes - No conflict

### Step 2.5: Compare Algorithms

**Extract algorithm summaries from each spec:**

**Feature 1 Algorithm:**
```
1. Load ADP data
2. Match player to ADP ranking
3. Calculate multiplier based on ADP value
4. Apply: score *= adp_multiplier
```

**Feature 2 Algorithm:**
```
1. Load injury data
2. Assess injury severity
3. Calculate penalty multiplier
4. Apply: score *= injury_multiplier
```

**Feature 4 Algorithm (Integration):**
```
1. Get base score
2. Apply ADP multiplier
3. Apply injury multiplier
4. Return total score
```

**CONFLICT (already identified):** Feature 4 missing schedule_strength multiplier

### Step 2.6: Document All Conflicts

After systematic comparison, compile full conflict list:

```markdown
## Summary: Conflicts Identified

**Total Conflicts Found:** 2

1. **Multiplier Application Order** (Category: Algorithms)
   - Feature 4 missing schedule_strength multiplier
   - Severity: HIGH
   - Affects: Feature 4

2. **File Location Inconsistency** (Category: File Locations)
   - Feature 2 not using subdirectory structure
   - Severity: LOW
   - Affects: Feature 2

**No conflicts found in:**
- Data Structures
- Interfaces & Dependencies (method signatures match)
- Configuration Keys (no duplicates or conflicts)
- Testing Assumptions
```

---

## Step 3: Conflict Resolution

### Step 3.1: Resolve Each Conflict

**For Conflict 1: Multiplier Application Order**

**Determine correct approach:**
- Feature 4 must apply ALL multipliers (from Features 1, 2, 3)
- Order doesn't matter for multiplication (commutative)
- Should be explicit about all sources

**Update Feature 4 spec.md:**

```markdown
## Algorithm: Comprehensive Score Calculation

**Includes multipliers from ALL features:**

```python
def calculate_total_score(player: FantasyPlayer) -> float:
    # Base score from projected points
    base_score = player.projected_points

    # Apply ALL multipliers from features 1-3
    score = base_score
    score *= player.adp_multiplier          # Feature 1: ADP Integration
    score *= player.injury_multiplier       # Feature 2: Injury Assessment
    score *= player.schedule_strength      # Feature 3: Schedule Analysis

    # Additional existing multipliers
    score *= player.team_quality_multiplier
    score *= player.matchup_multiplier

    return score
```

**Updated:** Feature 4 spec.md now includes all three new multipliers
```

**For Conflict 2: File Location Inconsistency**

**Determine correct approach:**
- Standardize on subdirectory structure
- Group related files: rankings/ vs player_info/

**Update Feature 2 spec.md:**

```markdown
## Data Sources

**Injury Data:**
- Source: Manual CSV file (`data/player_info/injury_reports.csv`)
- Updated from: `data/injury_reports.csv` (root) → CHANGED to subdirectory for consistency
- Format: Name,Position,InjuryStatus,Severity
```

### Step 3.2: Verify Resolutions Don't Create New Conflicts

**After updating specs, check:**

□ Feature 4 now references all multipliers - verified
□ Feature 2 file location doesn't conflict with other features - verified
□ No new conflicts introduced by changes - verified

**Document resolutions:**

```markdown
## Resolutions Applied

### Resolution 1: Multiplier Application Order

**Conflict:** Feature 4 missing schedule_strength multiplier
**Action:** Updated Feature 4 spec.md algorithm section
**Changes:**
- Added `score *= player.schedule_strength` to calculation
- Documented all multiplier sources in code comments
- Verified algorithm includes Features 1, 2, 3 contributions

**Files Updated:**
- feature_04_recommendation_updates/spec.md (Algorithm section, lines 45-65)

**Verification:** ✅ Algorithm now includes all multipliers

---

### Resolution 2: File Location Standardization

**Conflict:** Feature 2 using root data/ instead of subdirectory
**Action:** Updated Feature 2 spec.md file location
**Changes:**
- Changed path: data/injury_reports.csv → data/player_info/injury_reports.csv
- Reasoning: Group player-related data separately from rankings

**Files Updated:**
- feature_02_injury_assessment/spec.md (Data Sources section, lines 23-28)

**Verification:** ✅ All features now use subdirectory structure
```

### Step 3.3: Update epic/research/SANITY_CHECK_{DATE}.md

Mark conflicts as resolved:

```markdown
## Final Status

**Conflicts Identified:** 2
**Conflicts Resolved:** 2
**Unresolved Conflicts:** 0

✅ **All features aligned and conflict-free**

**Ready for user sign-off**
```

---

## Step 4: Create Final Plan Summary

Create presentation for user in epic EPIC_README.md or separate document:

```markdown
# Epic Implementation Plan - Ready for Approval

**Epic:** {epic_name}
**Date:** {YYYY-MM-DD}
**Status:** All features planned, sanity check complete

---

## Feature Summary

### Feature 1: ADP Integration
**Purpose:** Integrate Average Draft Position data into player scoring
**Scope:** Load ADP data, calculate multiplier, apply to scores
**Dependencies:** None (foundation)
**Risk:** MEDIUM
**Estimate:** ~30 implementation items

### Feature 2: Injury Risk Assessment
**Purpose:** Evaluate player injury risk and apply penalty
**Scope:** Load injury data, assess severity, calculate penalty multiplier
**Dependencies:** None (parallel to Feature 1)
**Risk:** LOW
**Estimate:** ~25 implementation items

### Feature 3: Schedule Strength Analysis
**Purpose:** Analyze upcoming opponent strength for roster decisions
**Scope:** Load schedule data, calculate opponent strength, apply multiplier
**Dependencies:** None (parallel to Features 1, 2)
**Risk:** LOW
**Estimate:** ~20 implementation items

### Feature 4: Recommendation Engine Updates
**Purpose:** Integrate all new data sources into draft recommendations
**Scope:** Update scoring algorithm, integrate Features 1-3, comprehensive testing
**Dependencies:** Features 1, 2, 3 (must complete first)
**Risk:** HIGH (integration complexity)
**Estimate:** ~35 implementation items

---

## Implementation Order

**Recommended sequence:**

1. **Phase 1:** Implement Features 1, 2, 3 in parallel
   - All three are independent (no dependencies)
   - Can be developed simultaneously
   - Each can be tested in isolation

2. **Phase 2:** Implement Feature 4
   - Depends on Features 1, 2, 3 being complete
   - Integrates all new data sources
   - Requires integration testing with all features

---

## Dependencies Diagram

```
Feature 1 (ADP) ──────┐
                      ├──> Feature 4 (Integration)
Feature 2 (Injury) ───┤
                      │
Feature 3 (Schedule) ─┘
```

---

## Risk Assessment

**HIGH Risk:**
- Feature 4 (Integration) - Complex, depends on others

**MEDIUM Risk:**
- Feature 1 (ADP) - External data source, matching logic

**LOW Risk:**
- Feature 2 (Injury) - Straightforward data loading
- Feature 3 (Schedule) - Similar to existing features

**Mitigation:**
- Implement low-risk features first (build confidence)
- Test each feature independently before integration
- Feature 4 will have comprehensive integration tests

---

## Sanity Check Results

**Cross-feature comparison complete:**
- ✅ All data structures aligned
- ✅ All interfaces verified
- ✅ All file locations standardized
- ✅ All configuration keys unique
- ✅ All algorithms coordinated

**Conflicts found and resolved:** 2
- Multiplier application order (Feature 4)
- File location inconsistency (Feature 2)

**Ready for implementation:** YES

---

## Next Steps After Approval

1. **S4:** Update epic testing strategy based on this plan
2. **S5:** Implement features sequentially (1, 2, 3, then 4)
3. **S6:** Epic-level final QC
4. **S7:** Epic cleanup and completion

**Estimated total timeline:** {X} features × {Y} hours = {Z} hours
```

---

## Step 5: User Sign-Off

### Step 5.1: Verify Acceptance Criteria (PRE-CHECK - MANDATORY)

**CRITICAL:** Before presenting plan, verify ALL features have user-approved acceptance criteria:

```markdown
**Acceptance Criteria Pre-Check:**

For EACH feature, verify:
□ Feature spec.md contains "Acceptance Criteria (USER MUST APPROVE)" section
□ Files Modified section lists EXACT paths and counts
□ Data Structures section shows expected formats
□ Behavior Changes section shows expected values
□ Deliverables section lists what will be created
□ User approval checkbox is marked [x]
□ Approval timestamp is documented

If ANY feature missing acceptance criteria or user approval:
❌ STOP - Return to S2 Phase 6 for that feature
❌ Do NOT present plan without ALL acceptance criteria approved
```

**Why This Matters:** Prevents presenting implementation plan with wrong scope. User must approve WHAT will be built (acceptance criteria) before approving HOW to build it (implementation plan).

**Real-World Example (Epic: fix_2025_adp):**
- S3 user sign-off obtained WITHOUT acceptance criteria review
- Epic implemented 102+ hours targeting WRONG FOLDER
- User testing (S7) caught it: 6 files instead of 108 files
- Lesson: Acceptance criteria approval prevents wrong implementations

---

### Step 5.2: Present Plan to User

```markdown
✅ **S3 (Cross-Feature Sanity Check) Complete**

I've completed a systematic comparison of all {N} features and created a comprehensive implementation plan.

**Acceptance Criteria Verification:**
- ✅ All {N} features have user-approved acceptance criteria
- ✅ Total scope: {X} files to be modified across {Y} folders
- ✅ All data structures and deliverables approved

**Sanity Check Results:**
- Compared all features across 6 categories
- Found and resolved {M} conflicts
- All features now aligned and conflict-free

**Implementation Plan:**
- {N} features total
- Recommended implementation order: {order}
- Dependencies mapped
- Risk assessment complete

**Full plan available in:**
- epic EPIC_README.md (updated with plan summary)
- epic/research/SANITY_CHECK_{DATE}.md (detailed analysis)
- Each feature spec.md (user-approved acceptance criteria)

**Please review the plan and let me know:**
1. Do you approve this feature breakdown and implementation order?
2. Are there any changes you'd like to make?
3. Are you ready to proceed to S4 (Epic Testing Strategy)?

⚠️ **Waiting for your approval before proceeding to S4.**
```

### Step 5.3: WAIT for User Response

**Update Agent Status:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** SANITY_CHECK
**Current Step:** Waiting for user approval of implementation plan
**Current Guide:** stages/s_3/cross_feature_sanity_check.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- User sign-off is MANDATORY
- Cannot proceed to S4 without approval

**Progress:** Sanity check complete, plan presented
**Next Action:** Wait for user approval
**Blockers:** Waiting for user sign-off on implementation plan
```

### Step 5.3: Handle User Response

**If user approves:**
```markdown
**User approved plan on {date}**

Proceeding to S4 (Epic Testing Strategy).
```

**If user requests changes:**
1. Document changes requested
2. Update affected feature specs
3. RE-RUN sanity check (conflicts may have been introduced)
4. Present updated plan
5. Wait for approval again

**Example:**
```
User requested: "Combine Features 2 and 3 into one feature"

Actions:
1. Merge Feature 2 and 3 specs into new Feature 2
2. Update Feature Tracking table (now 3 features instead of 4)
3. Re-run sanity check (verify Feature 4 dependencies updated)
4. Update implementation plan
5. Present updated plan for approval
```

---

## Step 6: Mark S3 Complete

### Step 6.1: Update epic EPIC_README.md

**Epic Completion Checklist:**

```markdown
**S3 - Cross-Feature Sanity Check:**
- [x] All specs compared systematically
- [x] Conflicts resolved (2 found, 2 resolved)
- [x] User sign-off obtained ({date})
```

**Agent Status:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** TESTING_STRATEGY
**Current Step:** Ready to begin S4
**Current Guide:** stages/s_4/epic_testing_strategy.md
**Guide Last Read:** NOT YET (will read when starting S4)

**Progress:** S3 complete, user approved plan
**Next Action:** Read stages/s_4/epic_testing_strategy.md and begin epic testing strategy update
**Blockers:** None

**User Sign-Off:** Obtained on {YYYY-MM-DD}
```

### Step 6.2: Announce Transition

```markdown
✅ **S3 (Cross-Feature Sanity Check) Complete**

**Sanity check results:**
- {N} features compared systematically
- {M} conflicts found and resolved
- User approval obtained on {date}

**Implementation plan approved:**
- {N} features ready for implementation
- Dependencies mapped
- Risk assessment complete

**Next: S4 (Epic Testing Strategy)**

I'll now transition to S4 to update the epic testing strategy based on our detailed plan.

Following `stages/s_4/epic_testing_strategy.md` to update epic_smoke_test_plan.md with specific test scenarios and integration points.
```

---

## Completion Criteria

**S3 is complete when ALL of these are true:**

□ Systematic comparison performed:
  - All features compared across all 6 categories
  - Comparison matrix filled out completely
  - All conflicts documented
□ All conflicts resolved:
  - Each conflict has resolution documented
  - Affected specs updated
  - No new conflicts created by resolutions
□ Sanity check report created:
  - epic/research/SANITY_CHECK_{DATE}.md exists
  - Contains comparison matrix
  - Contains conflict resolutions
  - Marked as "conflict-free" at end
□ Implementation plan created and presented to user
□ User approval obtained:
  - User explicitly approved plan
  - Approval date documented in epic EPIC_README.md
  - Any requested changes implemented
□ Epic EPIC_README.md updated:
  - Epic Completion Checklist: S3 items checked
  - Agent Status: Phase = TESTING_STRATEGY, ready for S4
  - User sign-off date documented

**If any item unchecked:**
- ❌ S3 is NOT complete
- ❌ Do NOT proceed to S4
- Complete missing items first

---

## Common Mistakes to Avoid

```
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "Feature 1 and 2 look similar, I'll skip comparing them"
   ✅ STOP - Compare ALL features systematically

❌ "This conflict seems minor, I'll ignore it"
   ✅ STOP - Document ALL conflicts, even minor ones

❌ "I'll resolve conflicts and tell user after"
   ✅ STOP - Resolve FIRST, then get approval

❌ "User is busy, I'll assume they approve"
   ✅ STOP - Must get explicit approval

❌ "I found 1 conflict, that's probably all"
   ✅ STOP - Complete full systematic comparison

❌ "I'll update specs after user approves"
   ✅ STOP - Specs must be conflict-free BEFORE approval

❌ "Let me start S4 while waiting for approval"
   ✅ STOP - Cannot proceed without approval

❌ "One feature isn't done with S2 yet, but I'll start S3"
   ✅ STOP - ALL features must complete S2 first
```

---

## Real-World Example

**Epic:** Improve Draft Helper (4 features)

**Step 1: Comparison Matrix Created**
- Listed all 4 features
- Created 6-category comparison template

**Step 2: Systematic Comparison**

**Category: Data Structures**
- Feature 1: Adds adp_value, adp_multiplier to FantasyPlayer
- Feature 2: Adds injury_status, injury_multiplier to FantasyPlayer
- Feature 3: Adds schedule_strength to FantasyPlayer
- Feature 4: Uses all above fields
- ✅ No conflicts

**Category: Algorithms**
- Feature 1: score *= adp_multiplier
- Feature 2: score *= injury_multiplier
- Feature 3: score *= schedule_strength
- Feature 4: score = base * adp * injury (MISSING schedule_strength)
- ⚠️ CONFLICT FOUND

**Category: File Locations**
- Feature 1: data/rankings/adp.csv
- Feature 2: data/injury_reports.csv (no subdirectory)
- Feature 3: data/rankings/schedule.csv
- ⚠️ CONFLICT FOUND (inconsistent directories)

**Step 3: Conflict Resolution**
1. Updated Feature 4 algorithm to include all multipliers
2. Updated Feature 2 file location to use subdirectory
3. Verified no new conflicts

**Step 4: Plan Summary**
- Created implementation plan
- Documented dependencies
- Risk assessment

**Step 5: User Sign-Off**
- Presented plan
- User approved
- Documented approval

**Result:** Ready for S4

---

## README Agent Status Update Requirements

**Update epic EPIC_README.md Agent Status at these points:**

1. ⚡ After completing comparison matrix (Step 1)
2. ⚡ After completing systematic comparison (Step 2)
3. ⚡ After resolving all conflicts (Step 3)
4. ⚡ After creating plan summary (Step 4)
5. ⚡ When waiting for user approval (Step 5 - mark blocker)
6. ⚡ After user approves (Step 5 - clear blocker, proceed to Step 6)
7. ⚡ After marking S3 complete (Step 6)

---

## Prerequisites for S4

**Before transitioning to S4, verify:**

□ S3 completion criteria ALL met
□ User approval obtained and documented
□ Epic EPIC_README.md shows:
  - Epic Completion Checklist: S3 items checked
  - Agent Status: Phase = TESTING_STRATEGY
  - User sign-off date documented
□ All conflicts resolved (sanity check report shows 0 unresolved)

**If any prerequisite fails:**
- ❌ Do NOT transition to S4
- Complete missing prerequisites

---

## S3 Complete Checklist

**S3 is COMPLETE when ALL of these are true:**

### Prerequisites Verified
- [ ] ALL features completed S2 (verified in EPIC_README.md)
- [ ] ALL features have user-approved acceptance criteria (mandatory pre-check)

### Comparison Work
- [ ] Feature pair comparison matrix created
- [ ] Systematic pairwise comparison complete (ALL pairs compared)
- [ ] All conflicts identified and documented in sanity check report

### Conflict Resolution
- [ ] All conflicts resolved (or documented as intentional differences)
- [ ] Conflicting features updated with resolutions
- [ ] Epic EPIC_README.md updated with resolution details
- [ ] Sanity check report shows 0 unresolved conflicts

### User Approval
- [ ] Complete plan presented to user for sign-off
- [ ] User sign-off obtained on entire epic plan
- [ ] Sign-off timestamp documented in EPIC_README.md

### Epic-Level Updates
- [ ] EPIC_README.md Agent Status updated: "S3 Complete"
- [ ] EPIC_README.md Epic Completion Checklist: S3 marked [x]
- [ ] All feature specs are aligned and conflict-free
- [ ] No blockers or waiting states

**If ANY item unchecked → S3 NOT complete**

**Critical Verification:**
- Zero unresolved conflicts (if intentional differences exist, documented)
- User approved complete plan (not just individual features)
- ALL features compared (not just some)

**When ALL items checked:**
✅ S3 COMPLETE
→ Proceed to S4 (Epic Testing Strategy)

**Next Guide:** `stages/s_4/epic_testing_strategy.md`

---

## Next Stage

**After completing S3:**

📖 **READ:** `stages/s_4/epic_testing_strategy.md`
🎯 **GOAL:** Update epic_smoke_test_plan.md based on detailed feature specs
⏱️ **ESTIMATE:** 30-45 minutes

**S4 will:**
- Review initial test plan (created in S1)
- Add specific test scenarios based on feature specs
- Identify integration points between features
- Define epic success criteria with actual implementation knowledge

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting S4.

---

*End of stages/s_3/cross_feature_sanity_check.md*
