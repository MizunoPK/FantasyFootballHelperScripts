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

## Table of Contents

1. [Overview](#overview)
2. [Critical Rules](#critical-rules)
3. [Prerequisites Checklist](#prerequisites-checklist)
4. [Parallel Work Sync Verification (If Applicable)](#parallel-work-sync-verification-if-applicable)
5. [Workflow Overview](#workflow-overview)
6. [Step 1: Prepare Comparison Matrix](#step-1-prepare-comparison-matrix)
7. [Step 2: Systematic Comparison](#step-2-systematic-comparison)
8. [Step 4: Create Final Plan Summary](#step-4-create-final-plan-summary)
9. [Step 6: Mark S3 Complete](#step-6-mark-s3-complete)
10. [Exit Criteria](#exit-criteria)
11. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
12. [Real-World Example](#real-world-example)
13. [Prerequisites for S4](#prerequisites-for-s4)
14. [S3 Complete Checklist](#s3-complete-checklist)
15. [Next Stage](#next-stage)

---

## Overview

**What is this guide?**
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

**FOR DEPENDENCY GROUP EPICS:**

S3 runs ONCE PER ROUND (not just once at end):

- **Round 1 S3:** Validate Group 1 features against each other
- **Round 2 S3:** Validate Group 2 features against ALL Group 1 features
- **Round 3 S3:** Validate Group 3 features against ALL Groups 1-2 features

**Scope expands per round** - Each round validates new features against ALL prior features.

---

## Critical Rules

```text
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



## 🔄 Parallel Work Sync Verification (If Applicable)

**Skip this section if S2 was done sequentially (single agent)**

**If S2 was done in parallel mode (Primary + Secondaries):**

The Primary agent MUST verify all secondary agents completed S2 before proceeding.

**Complete sync verification protocol:**
- **File:** [s3_parallel_work_sync.md](s3_parallel_work_sync.md)
- **File Size:** ~217 lines
- **Time:** 15-20 minutes

**What's covered:**
- Step 0.1: Check completion messages from secondary agents
- Step 0.2: Verify STATUS files show COMPLETE
- Step 0.3: Verify checkpoint files not stale
- Step 0.4: Verify feature specs complete
- Step 0.5: Document sync verification
- Step 0.6: Notify secondary agents

**After completing parallel sync verification (if applicable):**
- ✅ All secondary agents verified complete
- ✅ All feature specs ready for comparison
- ✅ Sync verification documented
- ✅ Secondary agents notified

**Proceed to:** Step 1 (Prepare Comparison Matrix)

---
---

## Workflow Overview

```text
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

```text
Features to compare:
1. feature_01_adp_integration
2. feature_02_injury_assessment
3. feature_03_schedule_analysis
4. feature_04_recommendation_updates
```

### Step 1.2: Create Comparison Template

**Copy the template to create:** `epic/research/SANITY_CHECK_{DATE}.md`

**Template file:** `feature-updates/guides_v2/templates/cross_feature_sanity_check_template.md`

The template contains:
- 6 comparison matrix categories (Data Structures, Interfaces, File Locations, Config Keys, Algorithms, Testing)
- Placeholder sections for Conflicts Identified and Resolutions Applied
- Will be populated during Step 2 and Step 3

---

## Step 2: Systematic Comparison

**For EACH comparison category, compare ALL features pairwise:**

### Comparison Process

For each category below:
1. Extract relevant info from each feature spec.md
2. Fill comparison matrix
3. Check for conflicts
4. Document any conflicts found

---

### Category 1: Data Structures

**What to compare:**
- Fields added to existing objects
- Field names and data types
- Potential name collisions

**Example comparison:**

| Feature | Data Added | Field Names | Data Types | Conflicts? |
|---------|-----------|-------------|------------|------------|
| Feature 1 (ADP) | adp_value, adp_multiplier | adp_value, adp_multiplier | Optional[int], float | ❌ None |
| Feature 2 (Injury) | injury_status, injury_multiplier | injury_status, injury_multiplier | str, float | ❌ None |
| Feature 3 (Schedule) | schedule_strength | schedule_strength | float | ❌ None |
| Feature 4 (Integration) | (uses existing fields) | N/A | N/A | ❌ None |

**Conflict checks:**
- ❌ Duplicate field names?
- ❌ Conflicting types for same field?
- ❌ Incompatible data formats?

---

### Category 2: Interfaces & Dependencies

**What to compare:**
- Methods called from other modules
- Expected return types
- Parameter assumptions

**Example conflict detection:**

```markdown
Feature 1 expects: `load_players() -> List[FantasyPlayer]`
Feature 2 expects: `load_players() -> List[FantasyPlayer]`
✅ MATCH - No conflict

Feature 4 expects: `calculate_total_score()` includes ALL multipliers
But spec only shows: `score = base * adp * injury`
⚠️ CONFLICT: Missing schedule_strength multiplier
```

---

### Category 3: File Locations & Naming

**What to compare:**
- File paths created by each feature
- Directory structure consistency
- Naming convention alignment

**Example:**
- Feature 1: `data/rankings/adp.csv` (subdirectory)
- Feature 2: `data/injury_reports.csv` (root)
- Feature 3: `data/rankings/schedule_strength.csv` (subdirectory)

⚠️ CONFLICT: Feature 2 inconsistent with subdirectory structure

---

### Category 4: Configuration Keys

**What to compare:**
- Config keys added by each feature
- Key name collisions
- Config file locations

**Check for conflicts:**
- Same key name used differently
- Keys that should be shared but aren't

---

### Category 5: Algorithms & Logic

**What to compare:**
- Algorithm approach (multiplicative vs additive)
- Order dependencies
- Score calculation logic

**Common conflicts:**
- Integration feature missing a data source
- Conflicting assumptions about calculation order
- Incompatible score modification strategies

---

### Category 6: Testing Assumptions

**What to compare:**
- Test data requirements
- Mock dependencies
- Integration test assumptions

---

### Step 2.6: Document All Conflicts

**After systematic comparison, compile conflict list:**

```markdown
## Summary: Conflicts Identified

**Total Conflicts Found:** {N}

### Conflict 1: {Name}
- **Category:** {Category}
- **Issue:** {Description}
- **Severity:** HIGH/MEDIUM/LOW
- **Affects:** {Feature(s)}

[Continue for each conflict...]

**No conflicts found in:**
- {List categories with no conflicts}
```


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

```
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
```markdown

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

### Step 3.2: Verify Resolutions Don't Create New Conflicts (Iterative Validation Loop)

**Clean Loop Definition:**

A "clean loop" means ZERO issues found of ANY severity level:
- HIGH severity: Must resolve ✓
- MEDIUM severity: Must resolve ✓
- **LOW severity: Must resolve** ✓ (NOT deferrable)

**Zero Tolerance Standard:**
- S3 is the LAST checkpoint before implementation
- ALL issues must be resolved (no severity-based deferrals)
- "Clean enough" is not clean
- LOW severity issues compound over time
- "Acceptable" issues become technical debt

**Examples of LOW severity that still require resolution:**
- Documentation formatting inconsistencies
- Argument naming inconsistencies across features
- Missing cross-reference sections in specs
- Unclear wording that could be misinterpreted

**Exit Condition:**
3 consecutive loops with ZERO issues (any severity) = Step 3 complete

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

| Feature | Purpose | Dependencies | Risk | Est. Items |
|---------|---------|--------------|------|------------|
| Feature 1: {Name} | {Purpose} | None | {RISK} | ~{N} |
| Feature 2: {Name} | {Purpose} | None | {RISK} | ~{N} |
| Feature 3: {Name} | {Purpose} | None | {RISK} | ~{N} |
| Feature 4: {Name} | {Purpose} | Features 1-3 | {RISK} | ~{N} |

**Risk Levels:**
- HIGH: Complex integration, multiple dependencies
- MEDIUM: External data, matching logic
- LOW: Straightforward data loading

---

## Implementation Order

**Recommended sequence:**
1. Implement independent features in parallel (Features 1-3)
2. Implement integration feature (Feature 4) after dependencies complete

**Dependency diagram:**
```
Feature 1 ──────┐
                 ├──> Feature 4
Feature 2 ───────┤
                 │
Feature 3 ───────┘
```

---

## Sanity Check Results

**Cross-feature comparison complete:**
- ✅ Data structures aligned
- ✅ Interfaces verified
- ✅ File locations standardized
- ✅ Configuration keys unique
- ✅ Algorithms coordinated

**Conflicts found and resolved:** {N}
- {Brief list of conflicts}

**Ready for implementation:** YES

---

## Next Steps After Approval

1. **S4:** Update epic testing strategy
2. **S5:** Implement features sequentially
3. **S9:** Epic-level final QC
4. **S10:** Epic cleanup and completion

**Estimated timeline:** {N} features × {Y} hours = {Z} hours
```


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
- User testing (S10) caught it: 6 files instead of 108 files
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
**Current Guide:** stages/s3/s3_cross_feature_sanity_check.md
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
```text
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
**Current Guide:** stages/s4/s4_epic_testing_strategy.md
**Guide Last Read:** NOT YET (will read when starting S4)

**Progress:** S3 complete, user approved plan
**Next Action:** Read stages/s4/s4_epic_testing_strategy.md and begin epic testing strategy update
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

Following `stages/s4/s4_epic_testing_strategy.md` to update epic_smoke_test_plan.md with specific test scenarios and integration points.
```

---

## Exit Criteria

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

```text
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

**Systematic Comparison Results:**

| Category | Findings |
|----------|----------|
| Data Structures | ✅ No conflicts - all features add unique fields |
| Interfaces | ✅ Method signatures match across features |
| File Locations | ⚠️ CONFLICT: Feature 2 uses root instead of subdirectory |
| Config Keys | ✅ No duplicates - all threshold keys distinct |
| Algorithms | ⚠️ CONFLICT: Feature 4 missing schedule_strength multiplier |
| Testing | ✅ Compatible test assumptions |

**Conflicts Found:** 2
1. **Multiplier Order** (HIGH): Feature 4 algorithm incomplete
2. **File Location** (LOW): Feature 2 inconsistent directory structure

**Resolutions:**
1. Updated Feature 4 spec to include all multipliers
2. Standardized Feature 2 file location to use subdirectory

**Result:** All conflicts resolved, user approved plan, ready for S4


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

**Next Guide:** `stages/s4/s4_epic_testing_strategy.md`

---

## Next Stage

**After completing S3:**

📖 **READ:** `stages/s4/s4_epic_testing_strategy.md`
🎯 **GOAL:** Update epic_smoke_test_plan.md based on detailed feature specs
⏱️ **ESTIMATE:** 30-45 minutes

**S4 will:**
- Review initial test plan (created in S1)
- Add specific test scenarios based on feature specs
- Identify integration points between features
- Define epic success criteria with actual implementation knowledge

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting S4.

---

*End of stages/s3/s3_cross_feature_sanity_check.md*
