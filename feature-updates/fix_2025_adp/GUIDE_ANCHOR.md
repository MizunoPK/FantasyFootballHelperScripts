# Guide Anchor: fix_2025_adp Epic

**Purpose:** Resumption instructions after session compaction

---

## 🚨 MANDATORY: Read This First After Session Compaction

**If you're resuming work on this epic after session compaction:**

1. **READ EPIC_README.md "Agent Status" section**
   - Current Stage
   - Current Step
   - Current Guide
   - Next Action

2. **READ the Current Guide listed in Agent Status**
   - Use Read tool to load ENTIRE guide
   - Don't skim or summarize
   - Full guide reading prevents missing critical steps

3. **Continue from "Next Action"**
   - Don't restart workflow
   - Don't skip to different stage
   - Follow exactly what Agent Status says

---

## Workflow Reference

```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC
```

**Stage 5 Per-Feature Workflow:**
```
5a (TODO) → 5b (Impl) → 5c (QC) → 5d (Align) → 5e (Test Plan)
```

---

## Current Epic Status

**Check EPIC_README.md for:**
- Which features are complete
- Which feature is currently being worked on
- Current stage and phase
- Blockers (if any)

**Check feature README.md for feature-specific status:**
- feature_01_csv_data_loading/README.md
- feature_02_player_matching_update/README.md

---

## Guide Locations

**All guides in:** `feature-updates/guides_v2/`

**Stage guides:**
- STAGE_1_epic_planning_guide.md
- STAGE_2_feature_deep_dive_guide.md
- STAGE_3_cross_feature_sanity_check_guide.md
- STAGE_4_epic_testing_strategy_guide.md
- STAGE_5aa_round1_guide.md
- STAGE_5ab_round2_guide.md
- STAGE_5ac_round3_guide.md
- STAGE_5b_implementation_execution_guide.md
- STAGE_5ca_smoke_testing_guide.md
- STAGE_5cb_qc_rounds_guide.md
- STAGE_5cc_final_review_guide.md
- STAGE_5d_post_feature_alignment_guide.md
- STAGE_5e_post_feature_testing_update_guide.md
- STAGE_6_epic_final_qc_guide.md
- STAGE_7_epic_cleanup_guide.md

**Supporting files:**
- prompts_reference_v2.md (MANDATORY phase transition prompts)
- templates_v2.md (file templates)
- EPIC_WORKFLOW_USAGE.md (complete usage guide)

---

## Phase Transition Protocol

**MANDATORY when starting ANY new stage/phase:**

1. Read `prompts_reference_v2.md` for the transition prompt
2. Use the exact prompt to acknowledge guide requirements
3. Update EPIC_README.md Agent Status before proceeding

**Example:**
```
Starting Stage 2?
→ Read prompts_reference_v2.md "Starting Stage 2" section
→ Use that prompt to acknowledge requirements
→ Update Agent Status in EPIC_README.md
```

---

## Quick Checks

**Before doing ANYTHING, verify:**

□ Read EPIC_README.md Agent Status (know where you are)
□ Read Current Guide (know what to do)
□ Check for blockers (know what's preventing progress)
□ Update Agent Status after completing steps (keep status current)

**If uncertain:**
- Read EPIC_README.md first
- Read current guide second
- Don't guess or skip steps
- Follow guide exactly as written

---

**Last Updated:** 2025-12-31
**Epic Created:** 2025-12-31
**Total Features:** 2
