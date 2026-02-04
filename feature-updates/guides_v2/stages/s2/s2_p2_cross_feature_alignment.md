# S2.P2: Cross-Feature Alignment Check (Primary Agent Only)

🚨 **MANDATORY READING PROTOCOL**

**Before starting this phase:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Verify ALL features in group completed S2.P1 (Gate 3 passed for each)
3. Update epic EPIC_README.md Agent Status with guide name + timestamp

**This phase is PRIMARY AGENT ONLY - Secondary agents wait**

---

## Quick Start

**Purpose:** Pairwise comparison of all features in group (and previous groups) with Consistency Loop validation

**When:** After entire group completes S2.P1

**Time:** 20-60 minutes (depending on feature count)

**Key Outputs:**
- Updated spec.md files (if conflicts resolved)
- `epic/research/S2_P2_COMPARISON_MATRIX_GROUP_{N}.md` (audit trail)
- Conflict resolution notes

---

## Prerequisites

□ All features in current group completed S2.P1
□ All features have user-approved spec.md (Gate 3 passed)
□ If parallel mode: All secondary agents reported completion

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed to S2.P2
- Complete missing features first

---

## Steps

### Step 0: Sync Verification (If Parallel Mode) (5-10 min)

**Only if parallel work mode enabled:**

- Verify all features in group completed S2.P1:
  - Check completion messages from secondary agents
  - Verify STATUS files show READY_FOR_SYNC = true
  - Verify checkpoints show WAITING_FOR_SYNC (not stale)
  - Check for stale agents (checkpoint >60 min old → escalate)
- See: `parallel_work/s2_parallel_protocol.md` → Sync Point 1
- **If any agent missing/stale:** STOP, send status check, wait for response
- **Cannot proceed without all agents synced**

### Step 1: Verify Group Completion (5 min)

- Check all features in current group completed S2.P1
- Verify all STATUS files show READY_FOR_SYNC = true
- If parallel mode: Verify all secondary agents reported completion

### Step 2: Pairwise Comparison (20-40 min)

**For each pair of features in scope:**
- Current group features vs each other
- Current group features vs ALL previous group features

**Check for:**
- Naming conflicts (same name, different meaning)
- Approach conflicts (contradictory implementations)
- Data structure conflicts (incompatible formats)
- Integration dependencies
- Pattern inconsistencies

**Document conflicts in comparison matrix**

### Step 2.5: Save Comparison Results (5 min)

Create `epic/research/S2_P2_COMPARISON_MATRIX_GROUP_{N}.md`

```markdown
# S2.P2 Comparison Matrix - Group {N}

**Date:** {YYYY-MM-DD}
**Group:** {N}
**Features Compared:** {list features}

## Pairwise Comparison Matrix

| Feature A | Feature B | Conflicts Found | Severity | Resolution |
|-----------|-----------|-----------------|----------|------------|
| F1 | F2 | None | - | - |
| F1 | F3 | Naming conflict: "session" | MEDIUM | Renamed F1 to "user_session", F3 to "game_session" |
| F2 | F3 | None | - | - |

## Conflicts Summary

**Total Pairs Checked:** {N}
**Conflicts Found:** {N}
**High Severity:** {N}
**Medium Severity:** {N}
**Low Severity:** {N}

## Resolutions Applied

### Conflict 1: {Description}
- **Features:** F1, F3
- **Type:** Naming conflict
- **Issue:** Both used "session" for different purposes
- **Resolution:** Renamed F1 to "user_session", F3 to "game_session"
- **Files Updated:** feature_01_name/spec.md, feature_03_name/spec.md

[Continue for each conflict...]

---

**Audit Trail:** This file provides evidence that cross-feature alignment check was performed and all conflicts were resolved before proceeding to S3.
```

**Rationale:** Audit trail for cross-feature decisions, helps with future debugging

### Step 3: Conflict Resolution (10-20 min)

For each conflict found:
- Update affected feature spec.md files
- Document resolution approach
- Note dependencies in EPIC_README.md

### Step 4: Consistency Loop Validation (15-30 min)

**Reference:** `reference/consistency_loop_alignment.md`

- **Round 1:** Pairwise comparison in feature order (F1 vs F2, F2 vs F3, etc.)
- **Round 2:** Pairwise comparison in reverse order (different patterns)
- **Round 3:** Random pair spot-checks, thematic clustering
- **Exit:** 3 consecutive clean rounds (no conflicts)
- **Zero Tolerance:** ALL issues (HIGH/MEDIUM/LOW) must be resolved

**Outputs:**
- Updated spec.md files (if conflicts resolved)
- `epic/research/S2_P2_COMPARISON_MATRIX_GROUP_{N}.md`
- Conflict resolution notes (in comparison matrix file)

---

## Group-Based Looping

**S2.P2 runs MULTIPLE TIMES in parallel mode:**

- After Group 1 completes S2.P1 → Run S2.P2 on Group 1 features only
- After Group 2 completes S2.P1 → Run S2.P2 on Group 2 + ALL Group 1 features
- After Group 3 completes S2.P1 → Run S2.P2 on Group 3 + ALL Groups 1-2 features
- Scope expands each iteration (cumulative alignment check)

**After S2.P2:**
- If more groups remain → Loop back to S2.P1 with next group
- If all groups done → Proceed to S3

---

## Parallel Work Compatibility

**S2.P1 (all 3 iterations) can be parallelized:**
- Multiple agents work on different features simultaneously
- Each agent executes S2.P1.I1, I2, I3 for their feature(s)
- Existing parallel work protocols apply

**S2.P2 is PRIMARY AGENT ONLY:**
- Only Primary runs S2.P2 after each group completes S2.P1
- Secondary agents wait at end of S2.P1.I3

**No changes to parallel infrastructure needed** - existing protocols work with new structure.

---

## Completion Criteria

**S2.P2 complete when ALL true:**

□ All pairwise comparisons performed
□ All conflicts identified and resolved
□ Consistency Loop passed (3 consecutive clean rounds)
□ Comparison matrix created and saved
□ All spec.md files updated (if conflicts resolved)
□ Epic EPIC_README.md updated with S2.P2 completion

---

## Next Stage

**After S2.P2 complete:**

- If more groups remain → Loop back to S2.P1 for next group
- If all groups complete → Proceed to S3

📖 **READ:** `stages/s3/s3_epic_planning_approval.md` (when all groups done)

---

*End of s2_p2_cross_feature_alignment.md*
