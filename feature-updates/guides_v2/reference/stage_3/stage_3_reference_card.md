# STAGE 3: Cross-Feature Sanity Check - Quick Reference Card

**Purpose:** One-page summary for systematic feature comparison and conflict resolution
**Use Case:** Quick lookup when validating epic-wide consistency before implementation
**Total Time:** 30-60 minutes (scales with feature count)

---

## Workflow Overview

```text
STEP 1: Prepare Comparison Matrix (10 min)
    ├─ List all features
    ├─ List comparison categories (6 categories)
    └─ Create comparison template in epic/research/SANITY_CHECK_{DATE}.md
    ↓
STEP 2: Systematic Comparison (15-30 min)
    ├─ Compare features pairwise across 6 categories:
    │   ├─ Data Structures (field names, types, overlaps)
    │   ├─ Interfaces & Dependencies (method calls, return types)
    │   ├─ File Locations & Naming (file paths, naming conflicts)
    │   ├─ Configuration Keys (config file overlaps)
    │   ├─ Algorithms & Logic (scoring impacts, dependencies)
    │   └─ Testing Assumptions (test data, mocks, integration)
    └─ Document ALL conflicts found
    ↓
STEP 3: Conflict Resolution (10-20 min)
    ├─ For EACH conflict:
    │   ├─ Determine correct approach
    │   ├─ Update affected feature specs
    │   └─ Document resolution in sanity check file
    └─ Verify no new conflicts created
    ↓
STEP 4: Create Final Plan Summary (5-10 min)
    ├─ Summarize all features
    ├─ Document dependencies
    ├─ Recommended implementation order
    └─ Risk assessment
    ↓
STEP 5: User Sign-Off (10-15 min) ← MANDATORY GATE
    ├─ Present complete plan to user
    ├─ WAIT for explicit approval
    ├─ If changes requested: implement and re-run sanity check
    └─ Document approval in epic EPIC_README.md
    ↓
STEP 6: Mark Complete (2 min)
    ├─ Update epic EPIC_README.md (S3 complete)
    └─ Transition to S4
```

---

## Step Summary Table

| Step | Duration | Key Activities | Outputs | Gate? |
|------|----------|----------------|---------|-------|
| 1 | 10 min | Prepare comparison matrix template | SANITY_CHECK_{DATE}.md | No |
| 2 | 15-30 min | Pairwise comparison across 6 categories | Conflicts documented | No |
| 3 | 10-20 min | Resolve conflicts, update specs | Updated specs | No |
| 4 | 5-10 min | Create final plan summary | Plan summary | No |
| 5 | 10-15 min | Present to user, wait for approval | User sign-off | ✅ YES |
| 6 | 2 min | Mark complete, transition | EPIC_README updated | No |

---

## Comparison Categories (6 Required)

### Category 1: Data Structures
**Check:**
- Field names (duplicates? conflicts?)
- Data types (mismatches?)
- Data added to files (overlapping columns?)

**Example Conflict:** Feature 1 adds `player_adp` as integer, Feature 2 adds `player_adp` as string

### Category 2: Interfaces & Dependencies
**Check:**
- Which features depend on others?
- Method calls between features
- Return types expected vs actual

**Example Conflict:** Feature 3 expects `get_projection()` to return dict, but Feature 2 returns list

### Category 3: File Locations & Naming
**Check:**
- File creation locations
- File naming conventions
- Paths to same files

**Example Conflict:** Feature 1 creates `data/projections.csv`, Feature 4 expects `data/player_projections.csv`

### Category 4: Configuration Keys
**Check:**
- Config keys added by each feature
- Config file locations
- Key name conflicts

**Example Conflict:** Both Feature 2 and Feature 3 add `THRESHOLD` key to same config file

### Category 5: Algorithms & Logic
**Check:**
- Algorithm types (scoring, ranking, filtering)
- Multiplier/score impacts (do they stack correctly?)
- Order dependencies (does order matter?)

**Example Conflict:** Feature 2 multiplies score by injury factor, Feature 3 multiplies by matchup factor - order matters

### Category 6: Testing Assumptions
**Check:**
- Test data needs
- Mock dependencies
- Integration test assumptions

**Example Conflict:** Feature 1 tests assume player data exists, Feature 2 tests assume empty player data

---

## Mandatory Gate

### Gate: User Sign-Off on Complete Plan (Step 5)
**Location:** stages/s3/s3_cross_feature_sanity_check.md Step 5
**What it checks:**
- User reviews complete epic plan (all features, all dependencies)
- User explicitly approves proceeding to implementation
- Approval documented

**Pass Criteria:** User says "approved" or "looks good" or equivalent confirmation
**If FAIL:** User requests changes → implement changes → re-run sanity check → get new approval

**Why mandatory:**
- Last chance to catch scope issues before coding
- User validates understanding of epic
- Prevents building wrong thing

---

## Decision Points

### Decision 1: Conflict Resolution Approach (Step 3)
**When:** Conflict found between features
**Options:**
- Update Feature A spec (if Feature A is wrong)
- Update Feature B spec (if Feature B is wrong)
- Update BOTH specs (if both need adjustment)
- Extract to shared utility (if both features need same thing)

**How to decide:**
- Which spec is closer to epic intent?
- Which approach minimizes changes?
- Ask user if unclear

### Decision 2: Implementation Order (Step 4)
**When:** Creating final plan summary
**Options:**
- Dependency order (features with no dependencies first)
- Risk order (riskiest features first)
- Value order (highest value features first)

**How to decide:**
- Default: Dependency order (safest)
- If high uncertainty: Risk order (fail fast)
- User can override with value order

### Decision 3: Re-Run Sanity Check? (Step 5)
**When:** User requests changes to plan
**Options:**
- Re-run full sanity check (if changes affect multiple features)
- Spot-check affected features only (if change isolated to one feature)

**How to decide:**
- If change affects dependencies → Full re-run
- If change adds/removes features → Full re-run
- If change updates single feature spec → Spot-check

---

## Critical Rules Summary

- ✅ ALL features must complete S2 before S3
- ✅ Compare ALL features systematically (not just some)
- ✅ Document ALL conflicts found (even minor ones)
- ✅ Resolve conflicts BEFORE user sign-off
- ✅ User sign-off is MANDATORY (cannot skip)
- ✅ Cannot proceed to S4 without user approval
- ✅ If user requests changes, implement and RE-RUN sanity check
- ✅ Update epic EPIC_README.md Epic Completion Checklist

---

## Common Pitfalls

### ❌ Pitfall 1: Skipping Categories
**Problem:** "I'll just check data structures, that's the main conflict area"
**Impact:** Interface conflicts, file naming conflicts slip through to S5
**Solution:** Check ALL 6 categories systematically

### ❌ Pitfall 2: Not Documenting Minor Conflicts
**Problem:** "This field name difference is small, not worth documenting"
**Impact:** Small conflicts become bugs in S7 QC
**Solution:** Document ALL conflicts, even if seem trivial

### ❌ Pitfall 3: Presenting Unresolved Conflicts to User
**Problem:** "Let the user decide between these conflicting approaches"
**Impact:** User doesn't have enough context, makes arbitrary decision
**Solution:** Resolve conflicts FIRST, THEN get user sign-off on resolved plan

### ❌ Pitfall 4: Assuming User Approval
**Problem:** "The plan looks good, I'll skip user sign-off"
**Impact:** Implement wrong thing, rework in S7 or user testing
**Solution:** ALWAYS get explicit user approval (mandatory gate)

### ❌ Pitfall 5: Not Re-Running After User Changes
**Problem:** "User just changed one feature, no need to re-check"
**Impact:** User change creates NEW conflicts with other features
**Solution:** If user requests changes, re-run sanity check (at least spot-check)

### ❌ Pitfall 6: Comparing Features to Incomplete Features
**Problem:** Comparing Feature 3 spec to Feature 2 (still in S2)
**Impact:** Feature 2 changes after comparison, conflicts appear later
**Solution:** Wait until ALL features complete S2

---

## Quick Checklist: "Am I Ready for Next Step?"

**Before Step 1:**
- [ ] ALL features completed S2
- [ ] All feature specs are complete
- [ ] All checklist.md items resolved
- [ ] Epic EPIC_README.md Feature Tracking shows all "[x]" for S2

**Step 1 → Step 2:**
- [ ] SANITY_CHECK_{DATE}.md created
- [ ] Comparison matrix template prepared
- [ ] All 6 categories listed

**Step 2 → Step 3:**
- [ ] All feature pairs compared across ALL 6 categories
- [ ] All conflicts documented in matrix
- [ ] Have complete conflict list

**Step 3 → Step 4:**
- [ ] ALL conflicts resolved
- [ ] Affected feature specs updated
- [ ] No new conflicts created by resolutions

**Step 4 → Step 5:**
- [ ] Final plan summary created
- [ ] Dependencies documented
- [ ] Implementation order recommended
- [ ] Risk assessment complete

**Step 5 → Step 6:**
- [ ] Complete plan presented to user
- [ ] User explicitly approved plan
- [ ] Approval documented in epic EPIC_README.md
- [ ] If user requested changes: Changes implemented and sanity check re-run

**Step 6 → S4:**
- [ ] S3 marked complete in EPIC_README.md
- [ ] Agent Status updated (next: S4)

---

## File Outputs

**Step 1:**
- `epic/research/SANITY_CHECK_{DATE}.md` (comparison matrix template)

**Step 2:**
- SANITY_CHECK_{DATE}.md (populated with conflicts)

**Step 3:**
- Updated feature specs (conflict resolutions)
- SANITY_CHECK_{DATE}.md (resolutions documented)

**Step 4:**
- Final plan summary in SANITY_CHECK_{DATE}.md

**Step 5:**
- Epic EPIC_README.md (user sign-off documented)

---

## Scaling with Feature Count

### 2-3 Features (Simple Epic)
- Time: 30 minutes
- Comparisons: 3-6 feature pairs
- Conflicts: Usually 0-2

### 4-5 Features (Medium Epic)
- Time: 45 minutes
- Comparisons: 10-15 feature pairs
- Conflicts: Usually 2-5

### 6+ Features (Complex Epic)
- Time: 60+ minutes
- Comparisons: 15+ feature pairs
- Conflicts: Usually 5+
- Consider: Breaking epic into sub-epics

---

## When to Use Which Guide

| Current Activity | Guide to Read |
|------------------|---------------|
| Starting cross-feature sanity check | stages/s3/s3_cross_feature_sanity_check.md |
| Need comparison examples | stages/s3/s3_cross_feature_sanity_check.md (examples section) |
| Conflict resolution patterns | stages/s3/s3_cross_feature_sanity_check.md (Step 3) |

---

## Exit Conditions

**S3 is complete when:**
- [ ] All features compared across all 6 categories
- [ ] All conflicts identified and documented
- [ ] All conflicts resolved (specs updated)
- [ ] Final plan summary created
- [ ] User explicitly approved complete plan
- [ ] Approval documented in epic EPIC_README.md
- [ ] EPIC_README.md shows S3 complete
- [ ] Ready to start S4 (Epic Testing Strategy)

**Next Stage:** S4 (Epic Testing Strategy)

---

**Last Updated:** 2026-01-04
