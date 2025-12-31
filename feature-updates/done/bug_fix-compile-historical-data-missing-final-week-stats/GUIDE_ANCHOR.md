# GUIDE ANCHOR - Session Resumption Instructions

**Epic:** bug_fix-compile-historical-data-missing-final-week-stats
**Created:** 2025-12-31
**Purpose:** Help agents resume work after session compaction/context loss

---

## 🚨 RESUMPTION PROTOCOL (READ THIS FIRST)

**If you're reading this after session compaction or starting fresh:**

1. **Read EPIC_README.md Agent Status section**
   - Check "Current Stage" and "Current Step"
   - Check "Next Action"
   - Check "Blockers"

2. **Read the current guide (listed in Agent Status)**
   - Full guide, not summary
   - Re-read critical rules section
   - Understand where you are in the workflow

3. **Continue from "Next Action" in Agent Status**
   - Do NOT restart from beginning
   - Do NOT skip ahead
   - Follow the exact next step listed

4. **Update Agent Status after reading this**
   - Update "Guide Last Read" timestamp
   - Add note: "RE-READ after compaction/resumption"

---

## Stage Workflow Reference

```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC
```

**Stage 5 Detail:**
```
5a: TODO Creation (24 iterations + audits)
  ↓
5b: Implementation (phase-by-phase)
  ↓
5c: Post-Implementation (smoke + QC + PR review)
  ↓
5d: Cross-Feature Alignment (update other specs)
  ↓
5e: Epic Testing Plan Update
```

---

## Guide Locations

**All guides in:** `feature-updates/guides_v2/`

**Stage 1:** `STAGE_1_epic_planning_guide.md`
**Stage 2:** `STAGE_2_feature_deep_dive_guide.md`
**Stage 3:** `STAGE_3_cross_feature_sanity_check_guide.md`
**Stage 4:** `STAGE_4_epic_testing_strategy_guide.md`

**Stage 5a (TODO Creation):**
- Round 1: `STAGE_5aa_round1_guide.md` (iterations 1-7 + 4a)
- Round 2: `STAGE_5ab_round2_guide.md` (iterations 8-16)
- Round 3: `STAGE_5ac_round3_guide.md` (iterations 17-24 + 23a)

**Stage 5b:** `STAGE_5b_implementation_execution_guide.md`

**Stage 5c (Post-Implementation):**
- Phase 1: `STAGE_5ca_smoke_testing_guide.md` (3 parts)
- Phase 2: `STAGE_5cb_qc_rounds_guide.md` (QC 1, 2, 3)
- Phase 3: `STAGE_5cc_final_review_guide.md` (PR review + lessons)

**Stage 5d:** `STAGE_5d_post_feature_alignment_guide.md`
**Stage 5e:** `STAGE_5e_post_feature_testing_update_guide.md`
**Stage 6:** `STAGE_6_epic_final_qc_guide.md`
**Stage 7:** `STAGE_7_epic_cleanup_guide.md`

**Bug Fix:** `STAGE_5_bug_fix_workflow_guide.md`

---

## Phase Transition Prompts

**ALWAYS use prompts from:** `feature-updates/guides_v2/prompts_reference_v2.md`

**Before transitioning stages:**
1. Find the appropriate prompt in prompts_reference_v2.md
2. Speak the prompt out loud (acknowledge requirements)
3. Update Agent Status
4. THEN proceed with new stage

---

## Epic File Structure

```
bug_fix-compile-historical-data-missing-final-week-stats/
├── EPIC_README.md          ← MAIN STATUS FILE (read this first)
├── GUIDE_ANCHOR.md         ← This file
├── notes.txt               ← Original bug description
├── epic_smoke_test_plan.md ← Epic testing (evolves: Stage 1 → 4 → 5e)
├── epic_lessons_learned.md ← Cross-feature insights
├── research/               ← Shared research documents
│   └── README.md
├── feature_01_week_18_data_folder_creation/
│   ├── README.md           ← Feature status (check Agent Status)
│   ├── spec.md             ← PRIMARY specification
│   ├── checklist.md        ← Resolved vs pending decisions
│   ├── todo.md             ← Implementation tasks (Stage 5a)
│   ├── questions.md        ← Questions for user (Stage 5a, if needed)
│   ├── implementation_checklist.md  ← Spec verification (Stage 5b)
│   ├── code_changes.md     ← Change documentation (Stage 5b)
│   └── lessons_learned.md  ← Feature insights
└── feature_02_simulation_data_flow_validation/
    └── (same structure as feature_01)
```

---

## Quick Status Check

**To understand current state:**

1. Read `EPIC_README.md` → Agent Status section
2. Read current feature's `README.md` → Agent Status section
3. Check Epic Progress Tracker in EPIC_README.md
4. Identify which guide to read next

**Common scenarios:**

- **"Agent Status says Stage 2"** → Read feature's spec.md and checklist.md
- **"Agent Status says Stage 5a"** → Check which iteration (1-24) in feature's README
- **"Agent Status says Stage 5b"** → Check which phase in todo.md
- **"Agent Status says Stage 5c"** → Check which part/round in feature's README
- **"Agent Status says Stage 6"** → Check epic_smoke_test_plan.md execution

---

## Critical Rules to Remember

1. **ALWAYS read the guide** before starting any stage/phase
2. **Update Agent Status** after every major step
3. **Use phase transition prompts** from prompts_reference_v2.md
4. **Verify against spec.md** constantly during implementation
5. **24 iterations are mandatory** in Stage 5a (no skipping)
6. **QC Restart Protocol** applies in Stage 5c if issues found
7. **Update epic_smoke_test_plan.md** in Stage 5e after each feature

---

## Need Help?

**If confused about:**
- **Where you are:** Read EPIC_README.md Agent Status
- **What to do next:** Read the current guide (full guide)
- **Why a step is needed:** Check guide's "Why this matters" sections
- **How to do a step:** Follow guide's step-by-step instructions

**Remember:** Guides are authoritative. If unsure, re-read the guide.

---

**Last Updated:** 2025-12-31
**Epic Status:** Stage 1 - Epic Planning (in progress)
