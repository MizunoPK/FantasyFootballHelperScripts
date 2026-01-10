# GUIDE_ANCHOR: Resumption Instructions

**Purpose:** Provides resumption instructions after session compaction

**Epic:** add_k_dst_ranking_metrics_support
**Created:** 2026-01-08

---

## How to Resume This Epic After Session Compaction

**CRITICAL:** If you're an agent resuming this epic after session compaction, follow these steps:

### Step 1: Read EPIC_README.md Agent Status FIRST
```
Location: feature-updates/KAI-5-add_k_dst_ranking_metrics_support/EPIC_README.md
Check: "Agent Status" section at top
```

**Agent Status tells you:**
- Current Stage (e.g., "Stage 2 - Feature Deep Dive")
- Current Guide (e.g., "stages/stage_2/phase_0_research.md")
- Current Step (e.g., "Phase 2 - Research Task 3")
- Next Action (exact next task to perform)
- Blockers (if any)

### Step 2: Read the Current Guide
```
Use Read tool to load the ENTIRE guide listed in Agent Status
Do NOT work from memory or summaries
```

**Why:** Guides contain critical requirements that conversation summaries miss

### Step 3: Use the Resumption Prompt
```
Location: feature-updates/guides_v2/prompts_reference_v2.md
Section: "Resuming In-Progress Epic"
```

**The prompt requires you to:**
- Acknowledge you read EPIC_README.md Agent Status
- Acknowledge you read the current guide
- List critical rules from current guide
- Verify prerequisites for current step
- Update Agent Status with new timestamp

### Step 4: Continue from "Next Action"
```
Execute the exact task listed in "Next Action" field
Do NOT restart the workflow
Do NOT skip to a different step
```

---

## Epic Workflow Reference

```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC
```

**Stage 5 Detail (Per Feature):**
```
5a → 5b → 5c → 5d → 5e
↓     ↓     ↓     ↓     ↓
TODO  Impl  QC    Align  Test Plan
```

---

## Quick Stage Identification

**If Agent Status says:**
- **Stage 1** → Read: `stages/stage_1/epic_planning.md`
- **Stage 2** → Read: `stages/stage_2/phase_0_research.md` (or phase_2_specification.md or phase_3_refinement.md)
- **Stage 3** → Read: `stages/stage_3/cross_feature_sanity_check.md`
- **Stage 4** → Read: `stages/stage_4/epic_testing_strategy.md`
- **Stage 5a** → Read: `stages/stage_5/round1_todo_creation.md` (or round2 or round3)
- **Stage 5b** → Read: `stages/stage_5/implementation_execution.md`
- **Stage 5c** → Read: `stages/stage_5/smoke_testing.md` (or qc_rounds.md or final_review.md)
- **Stage 5d** → Read: `stages/stage_5/post_feature_alignment.md`
- **Stage 5e** → Read: `stages/stage_5/post_feature_testing_update.md`
- **Stage 6** → Read: `stages/stage_6/epic_final_qc.md`
- **Stage 7** → Read: `stages/stage_7/epic_cleanup.md`

---

## Common Resumption Mistakes

**❌ WRONG:** "I'll just continue where I think we left off"
- **Why wrong:** Agent Status might say something different
- **✅ CORRECT:** Read EPIC_README.md Agent Status first

**❌ WRONG:** "I remember the requirements, I'll skip reading the guide"
- **Why wrong:** Guides have mandatory steps that summaries miss
- **✅ CORRECT:** Use Read tool to load ENTIRE current guide

**❌ WRONG:** "Let me restart from the beginning of this stage"
- **Why wrong:** Wastes work already completed
- **✅ CORRECT:** Continue from exact "Next Action" in Agent Status

**❌ WRONG:** "I'll update Agent Status after I finish the work"
- **Why wrong:** Work gets lost if session compacts again
- **✅ CORRECT:** Update Agent Status IMMEDIATELY after reading guide

---

## Feature-Specific Resumption

**If resuming during feature implementation (Stage 5):**

1. Check **feature README.md** Agent Status (not just epic EPIC_README.md)
2. Feature README has more detailed status for Stage 5 work
3. Use feature's "Next Action" to resume exact step

**Feature folder:** `feature_01_add_k_dst_ranking_metrics_support/`
**Feature README:** `feature_01_add_k_dst_ranking_metrics_support/README.md`

---

## Emergency: Can't Find Current State

**If Agent Status is unclear or missing:**

1. Check most recent file modification times:
   ```bash
   ls -lt feature-updates/KAI-5-add_k_dst_ranking_metrics_support/feature_01*/
   ```

2. Check most recently modified guide:
   ```bash
   grep "Guide Last Read" feature-updates/KAI-5-add_k_dst_ranking_metrics_support/EPIC_README.md
   ```

3. Check git commit history:
   ```bash
   git log --oneline -5
   ```

4. **If still unclear:** Ask user where we left off

---

**Remember:** EPIC_README.md Agent Status is the source of truth for resumption. Always read it first.
