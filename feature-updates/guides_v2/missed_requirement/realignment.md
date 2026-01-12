# PHASE 3 & 4: Realignment (Stage 3 & 4) and Resume

**Purpose:** Re-align ALL features and update epic test plan, then resume paused work

**When to Use:** After PHASE 2 complete, feature spec created/updated

**Previous Phase:** PHASE 2 (Planning) - See `missed_requirement/planning.md`

**Next Phase:** Resume previous work OR proceed to new/updated feature implementation (when its turn comes)

---

## Overview

**PHASE 3 & 4 ensures epic coherence after adding/updating a feature:**

- **Stage 3:** Cross-feature sanity check (ALL features)
- **Stage 4:** Update epic testing strategy
- **Resume:** Return to paused work
- **Later:** Implement new/updated feature in sequence

---

## PHASE 3: Stage 3 - Cross-Feature Sanity Check

### Critical: Re-align ALL Features

**🚨 FIRST ACTION:** Use "Starting Stage 3" prompt from `prompts/stage_3_prompts.md`

**READ:** `stages/s3/s3_cross_feature_sanity_check.md`

**IMPORTANT:** Don't just check the new/updated feature - check ALL feature pairs

---

### Step 1: Systematic Pairwise Comparison

**Process:**

1. **New/updated feature vs ALL other features:**
   - New/updated feature vs feature_01
   - New/updated feature vs feature_02
   - New/updated feature vs feature_03
   - New/updated feature vs feature_04

2. **ALL other feature pairs** (may reveal issues):
   - feature_01 vs feature_02
   - feature_01 vs feature_03
   - feature_02 vs feature_03
   - Etc.

**For each pair, check:**
- Interface overlaps
- Data structure conflicts
- Duplicate functionality
- Integration dependencies
- Shared resources

---

### Step 2: Identify Conflicts

**Common conflict types:**

**Interface conflicts:**
```markdown
Issue: feature_02 and feature_05 both define PlayerData class
Resolution: Create shared PlayerData in utils, both features use it
```

**Data structure conflicts:**
```markdown
Issue: feature_03 expects player_id as string, feature_05 uses integer
Resolution: Standardize on integer across all features
```

**Duplicate functionality:**
```markdown
Issue: feature_04 has CSV export, now adding to feature_03
Resolution: Extract CSV export to shared utility, both features use it
```

**Integration dependencies:**
```markdown
Issue: feature_05 needs data from feature_02's projection API
Resolution: Document integration point, add to both specs
```

---

### Step 3: Resolve Conflicts

**For each conflict found:**

1. **Determine resolution approach:**
   - Update one feature's spec
   - Update both features' specs
   - Create shared utility
   - Refactor integration point

2. **Update affected feature specs:**
   - Document changes in spec.md
   - Update checklist.md with decision
   - Note why change was needed

3. **Get user approval for changes:**
   ```markdown
   During Stage 3 alignment, I found a conflict:

   **Conflict:** {description}

   **Proposed Resolution:**
   {what needs to change}

   **Affected Features:**
   - feature_{XX}: {change needed}
   - feature_{YY}: {change needed}

   Approve this resolution? {User confirms}
   ```

---

### Step 4: User Sign-Off on Complete Aligned Plan

**After all conflicts resolved:**

```markdown
Stage 3 cross-feature sanity check complete.

**Features checked:** {count} features, {count} pairwise comparisons
**Conflicts found:** {count}
**Conflicts resolved:** {count}

**Changes made:**
- feature_{XX}: {changes}
- feature_{YY}: {changes}

**All features are now aligned and ready for implementation.**

Proceed to Stage 4 (Epic Testing Strategy update)? {User confirms}
```

---

## PHASE 4: Stage 4 - Epic Testing Strategy Update

### Update epic_smoke_test_plan.md

**🚨 FIRST ACTION:** Use "Starting Stage 4" prompt from `prompts/stage_4_prompts.md`

**READ:** `stages/s4/s4_epic_testing_strategy.md`

---

### Step 1: Add Scenarios for New/Updated Feature

**Questions to answer:**
- How does it integrate with other features?
- What epic-level workflows involve it?
- What should be tested in Stage 6?
- What are the integration points?

**Add test scenarios:**

```markdown
## Epic Integration Test: Player Scoring with Injury Status

**Features involved:**
- feature_02 (projection_system)
- feature_05 (injury_tracking) ← NEW

**Scenario:**
1. Load player with injury status = "Questionable"
2. Generate projection (should reduce projected points)
3. Verify score reflects injury adjustment

**Expected:** Projection accounts for injury status
**Success criteria:** Injured player projection < healthy projection

**Data to verify:**
- Injury status field populated
- Projection reduction applied correctly
- Score calculation uses adjusted projection
```

---

### Step 2: Update Existing Scenarios

**Review existing test scenarios:**
- Do they need updates due to new/updated feature?
- New cross-feature workflows to test?
- Data flow changes?

**Update scenarios as needed:**

```markdown
## Epic Integration Test: Draft Recommendations (UPDATED)

**Features involved:**
- feature_01 (adp_integration)
- feature_02 (projection_system)
- feature_05 (injury_tracking) ← ADDED

**Scenario:**
1. Load players with ADP data
2. Load injury status for each player ← NEW STEP
3. Generate projections (accounting for injuries) ← UPDATED
4. Generate draft recommendations

**Expected:** Recommendations account for both ADP and injury status
**Success criteria:** Injured high-ADP player ranked lower than healthy equivalent
```

---

### Step 3: Identify Integration Points

**Document integration points:**

```markdown
## Integration Points

**feature_02 → feature_05:**
- feature_02 calls feature_05.get_injury_status(player_id)
- Returns: {"status": "Healthy|Questionable|Out", "impact_factor": 0.0-1.0}

**feature_05 → feature_02:**
- None (feature_05 doesn't call feature_02)

**Shared Data:**
- player_id (integer, standardized across all features)
- PlayerData class (utils/FantasyPlayer.py)
```

---

## PHASE 5: Resume Previous Work

### Step 1: Mark Planning Complete

**Update EPIC_README.md:**

```markdown
## Missed Requirement Tracking

| # | Requirement | Action | Priority | Status | Created | Implemented | Notes |
|---|-------------|--------|----------|--------|---------|-------------|-------|
| 1 | Player injury tracking | New feature_05 | High | PLANNING COMPLETE | 2026-01-04 | Not yet | Ready for implementation (after feature_02) |

## Current Status

**Last Updated:** {YYYY-MM-DD HH:MM}

**Planning Complete:**
- feature_05_injury_tracking spec created (Stage 2 ✅)
- All features re-aligned (Stage 3 ✅)
- Epic test plan updated (Stage 4 ✅)

**Resuming Work:**
- feature_02_projection_system: Resuming Stage 5b Phase 3
  - Resume from: {Exact step where paused}
  - Next action: {Continue implementation}
```

---

### Step 2: Verify No Spec Changes Affect Paused Feature

**Check:**
- Did Stage 3 alignment change paused feature's spec?
- Does new/updated feature change interfaces paused feature uses?
- Do integration points affect paused feature?

---

#### If paused feature's spec WAS changed:

**Inform user:**

```markdown
I've completed planning for the missed requirement (Stages 2/3/4 complete).

During Stage 3 alignment, feature_02's spec was updated:
- Added integration point: Call feature_05.get_injury_status()
- Updated PlayerData class reference (now uses shared utility)
- Updated projection calculation to account for injury impact

Before resuming implementation, should I:
1. Update feature_02's implementation_plan.md to reflect spec changes
2. Continue with current implementation_plan.md (spec changes are minor/will handle during implementation)

What would you like to do?
```

**If user says update implementation_plan.md:**
- Re-run relevant parts of Stage 5a for affected tasks
- Update implementation plan
- Document changes
- Then resume

---

#### If paused feature's spec was NOT changed:

**Inform user:**

```markdown
Planning complete for missed requirement.

Stages completed:
- Stage 2: feature_05 spec created ✅
- Stage 3: All features aligned ✅
- Stage 4: Epic test plan updated ✅

feature_02's spec remains unchanged. Resuming implementation at Stage 5b Phase 3.
```

---

### Step 3: Resume from Saved State

**Read paused feature's README.md:**

```markdown
## Agent Status (PAUSED - Missed Requirement Handling)

**Resume Instructions:**
When planning complete:
1. Verify this feature's spec still valid after alignment ← DID THIS
2. Resume at: Stage 5b Phase 3 ← RESUME HERE
3. Context: Implementing projection calculation logic ← CONTEXT
```

**Update paused feature's README Agent Status:**

```markdown
## Agent Status (RESUMED)

**Last Updated:** {YYYY-MM-DD HH:MM}

**Current Phase:** IMPLEMENTATION_EXECUTION (Resumed)
**Current Guide:** stages/s5/s5_p4_execution.md

**Resumed After:** Missed requirement planning complete
- feature_05_injury_tracking spec created and aligned
- Stages 2/3/4 complete for feature_05
- feature_02 spec verified (unchanged/updated)

**Current Stage:** Stage 5b (Implementation Execution)
**Next Action:** Continue Phase 3 - Projection calculation logic

**Critical Rules from Guide:**
- Keep spec.md visible during implementation
- Continuous verification against spec
- Mini-QC checkpoints
- 100% test pass required
```

**Continue where you left off**

---

### Step 4: New/Updated Feature Implementation (Later)

**Important:** Don't implement new/updated feature yet!

**Implementation happens later when its turn comes in sequence:**

**Example - Medium Priority:**
```
Sequence:
1. feature_01 ✅ COMPLETE
2. feature_02 🔄 RESUMED (continue now)
3. feature_05 ◻️ NOT STARTED (implement after feature_02 completes)
4. feature_03 ◻️ NOT STARTED
5. feature_04 ◻️ NOT STARTED

Current action: Complete feature_02 (Stage 5b → 5c → 5d → 5e)
After feature_02: Implement feature_05 (Stage 5a → 5b → 5c → 5d → 5e)
```

**Example - High Priority:**
```
Sequence (high priority inserted):
1. feature_01 ✅ COMPLETE
2. feature_05 ◻️ NOT STARTED (implement immediately - blocks feature_02)
3. feature_02 🔄 PAUSED (resume after feature_05 completes)
4. feature_03 ◻️ NOT STARTED
5. feature_04 ◻️ NOT STARTED

Current action: Implement feature_05 (Stage 5a → 5b → 5c → 5d → 5e)
After feature_05: Resume and complete feature_02
```

**When new/updated feature's turn comes:**
- Run full Stage 5 (5a → 5b → 5c → 5d → 5e)
- Same rigor as all features
- No shortcuts

---

## Completion Criteria

**PHASE 3 & 4 complete when:**

**Stage 3 (Cross-Feature Sanity Check):**
- [x] All feature pairs compared systematically
- [x] All conflicts identified
- [x] All conflicts resolved
- [x] Affected specs updated
- [x] User approved conflict resolutions
- [x] User signed off on complete aligned plan

**Stage 4 (Epic Testing Strategy):**
- [x] epic_smoke_test_plan.md updated
- [x] New scenarios added for new/updated feature
- [x] Existing scenarios updated if needed
- [x] Integration points documented
- [x] Epic test coverage complete

**Resume:**
- [x] EPIC_README.md updated (planning complete)
- [x] Paused feature spec verified (changed or unchanged)
- [x] If changed: User decision on implementation_plan.md update
- [x] Paused feature README updated (resumed status)
- [x] Work resumed at correct point

---

## Common Scenarios

### Scenario 1: New Feature - No Conflicts Found

**Actions:**
1. Run Stage 3 pairwise comparison
2. No conflicts found
3. User signs off
4. Update epic test plan (Stage 4)
5. Resume paused work
6. New feature implemented later in sequence

---

### Scenario 2: New Feature - Minor Conflicts

**Actions:**
1. Run Stage 3 pairwise comparison
2. Find minor conflicts (e.g., naming inconsistency)
3. Resolve conflicts (update specs)
4. User approves resolutions
5. Update epic test plan (Stage 4)
6. Resume paused work (spec unchanged)
7. New feature implemented later

---

### Scenario 3: New Feature - Major Conflicts

**Actions:**
1. Run Stage 3 pairwise comparison
2. Find major conflicts (e.g., duplicate functionality)
3. Resolve conflicts (extract to shared utility)
4. Update multiple feature specs
5. User approves resolutions
6. Update epic test plan (Stage 4)
7. Resume paused work (spec WAS changed)
8. User decides: Update implementation_plan.md or handle during implementation
9. New feature implemented later

---

### Scenario 4: Update Unstarted Feature

**Actions:**
1. Run Stage 3 pairwise comparison
2. Check updated feature vs all others
3. Resolve any conflicts
4. Update epic test plan (Stage 4)
5. Resume paused work (if any)
6. Updated feature implemented later (in its original sequence position)

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Only Check New/Updated Feature

**Mistake:** "I'll just check the new feature vs others, skip other pairs"

**Why wrong:** New feature may reveal conflicts between existing features

**Correct:** Check ALL feature pairs systematically

---

### ❌ Anti-Pattern 2: Skip Stage 4

**Mistake:** "Epic test plan doesn't need updates for small feature"

**Why wrong:** Even small features need epic-level test coverage

**Correct:** Always update epic_smoke_test_plan.md

---

### ❌ Anti-Pattern 3: Implementing Immediately

**Mistake:** After planning, immediately implement new feature before resuming paused work

**Why wrong:** Breaks sequence, paused work left incomplete

**Correct:** Resume paused work, implement new/updated feature when its turn comes

---

### ❌ Anti-Pattern 4: Not Checking Paused Feature's Spec

**Mistake:** Resume without checking if paused feature's spec changed

**Why wrong:** May be implementing against outdated spec

**Correct:** Always verify paused feature's spec after Stage 3

---

## Next Steps

**After completing PHASE 3 & 4 (Realignment and Resume):**

✅ Stage 3 complete (all features aligned)
✅ Stage 4 complete (epic test plan updated)
✅ Paused feature spec verified
✅ Work resumed OR ready to resume

**Next:**
- If work was paused: Continue paused feature implementation
- If work was not paused: Continue current feature implementation
- Later: When new/updated feature's turn comes, implement through full Stage 5

**Special Case:**
- If discovered during Stage 6/7: See `missed_requirement/stage_6_7_special.md`

---

**END OF PHASE 3 & 4 GUIDE**
