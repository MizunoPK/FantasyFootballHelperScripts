# Guide Anchor: improve_configurability_of_scripts

**Purpose:** Help agents resume work correctly after session compaction or context window limits

**Created:** 2026-01-28
**Last Updated:** 2026-01-28

---

## 🚨 CRITICAL: If You're Resuming Work

**ALWAYS check EPIC_README.md Agent Status section FIRST**

The Agent Status contains:
- Current stage and phase
- Current guide name
- Guide last read timestamp
- Next action to take
- Current blockers

**Then:**
1. Use Read tool to load the ENTIRE guide listed in Agent Status
2. Use the "Resuming In-Progress Epic" prompt from `prompts_reference_v2.md`
3. Continue from the "Next Action" specified in Agent Status

---

## Workflow Reference

```
┌──────────────────────────────────────────────────────────────┐
│                   10-STAGE EPIC WORKFLOW                      │
└──────────────────────────────────────────────────────────────┘

S1: Epic Planning
   └─> Create epic folder, feature breakdown, epic ticket

S2: Feature Deep Dive (loop per feature - 9 features total)
   └─> Research, spec, checklist for each feature

S3: Cross-Feature Sanity Check
   └─> Pairwise comparison, resolve conflicts

S4: Epic Testing Strategy
   └─> Update epic_smoke_test_plan.md

S5-S8: Feature Loop (repeat per feature - 9 features)
   ├─> S5: Implementation Planning (28 iterations)
   ├─> S6: Implementation Execution
   ├─> S7: Implementation Testing & Review
   └─> S8: Post-Feature Alignment (S8.P1 + S8.P2)

S9: Epic Final QC
   └─> Epic smoke testing, QC rounds, user testing

S10: Epic Cleanup
   └─> Unit tests, guide updates, PR creation
```

---

## Current Epic State

**Epic:** improve_configurability_of_scripts
**Features:** 9
- Feature 01: player_fetcher
- Feature 02: schedule_fetcher
- Feature 03: game_data_fetcher
- Feature 04: historical_compiler
- Feature 05: win_rate_simulation
- Feature 06: accuracy_simulation
- Feature 07: league_helper
- Feature 08: integration_test_framework
- Feature 09: documentation

**Epic Folder:** `feature-updates/KAI-7-improve_configurability_of_scripts/`

**Implementation Order:** Features 01-09 (simple to complex scripts)

---

## Key Files by Stage

### S1 Files (Epic Planning)
- `EPIC_README.md` - Primary epic tracking (Agent Status here!)
- `EPIC_TICKET.md` - User-validated epic outcomes
- `epic_smoke_test_plan.md` - Test plan (initial, updates in S4/S8.P2)
- `epic_lessons_learned.md` - Cross-feature insights
- `feature_XX_{name}/README.md` - Feature tracking (Agent Status per feature)

### S2 Files (Feature Deep Dive)
- `feature_XX_{name}/spec.md` - PRIMARY specification
- `feature_XX_{name}/checklist.md` - Questions and decisions
- `feature_XX_{name}/lessons_learned.md` - Feature insights

### S5 Files (Implementation Planning)
- `feature_XX_{name}/implementation_plan.md` - Build guide (~400 lines)

### S6 Files (Implementation Execution)
- `feature_XX_{name}/implementation_checklist.md` - Progress tracker

---

## Finding the Right Guide

**If current stage is S1:** `stages/s1/s1_epic_planning.md`

**If current stage is S2:** Check feature README for phase
- S2.P1 (Research): `stages/s2/s2_p1_research.md`
- S2.P2 (Specification): `stages/s2/s2_p2_specification.md`
- S2.P3 (Refinement): `stages/s2/s2_p3_refinement.md`

**If current stage is S3:** `stages/s3/s3_cross_feature_sanity_check.md`

**If current stage is S4:** `stages/s4/s4_epic_testing_strategy.md`

**If current stage is S5:** Check feature README for round/part
- Round 1: `stages/s5/s5_p1_planning_round1.md`
- Round 2: `stages/s5/s5_p2_planning_round2.md`
- Round 3 Part 1: `stages/s5/s5_p3_i1_preparation.md`
- Round 3 Part 2: `stages/s5/s5_p3_i2_gates_part1.md` or `s5_p3_i3_gates_part2.md`

**If current stage is S6:** `stages/s6/s6_execution.md`

**If current stage is S7:** Check feature README for phase
- S7.P1: `stages/s7/s7_p1_smoke_testing.md`
- S7.P2: `stages/s7/s7_p2_qc_rounds.md`
- S7.P3: `stages/s7/s7_p3_final_review.md`

**If current stage is S8:** Check which phase
- S8.P1: `stages/s8/s8_p1_cross_feature_alignment.md`
- S8.P2: `stages/s8/s8_p2_epic_testing_update.md`

**If current stage is S9:** `stages/s9/s9_epic_final_qc.md`

**If current stage is S10:** `stages/s10/s10_epic_cleanup.md`

---

## Emergency Recovery

**If you're completely lost:**
1. Read `EPIC_README.md` Agent Status section
2. Read current feature's `README.md` Agent Status section (if in S2-S8)
3. Use Read tool to load the guide listed in Agent Status
4. Use "Resuming In-Progress Epic" prompt
5. Continue from "Next Action"

**If files seem inconsistent with conversation summary:**
- TRUST THE FILES (not the summary)
- Files are source of truth
- Conversation summaries can be outdated

---

**Remember:** Agent Status in README files survives session compaction. Always check it first!
